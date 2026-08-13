#!/usr/bin/env python3
"""LLM과 Kakao Local API를 결합한 CLI 기반 국내 여행 추천 프로그램."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv
from openai import APIConnectionError, APIStatusError, OpenAI

BASE_DIR = Path(__file__).resolve().parent
RESULTS_DIR = BASE_DIR / "results"
KAKAO_KEYWORD_URL = "https://dapi.kakao.com/v2/local/search/keyword.json"
TIMEOUT_SECONDS = 20

RECOMMENDATION_SCHEMA: dict[str, Any] = {
    "type": "json_schema",
    "json_schema": {
        "name": "travel_recommendation",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "recommended_city": {"type": "string"},
                "weather": {"type": "string"},
                "events": {"type": "array", "items": {"type": "string"}},
                "reason": {"type": "string"},
            },
            "required": ["recommended_city", "weather", "events", "reason"],
            "additionalProperties": False,
        },
    },
}


class PlannerError(RuntimeError):
    """사용자에게 안내할 수 있는 예외를 나타낸다."""


def parse_args() -> argparse.Namespace:
    """명령줄 인수를 검증하여 반환한다."""
    parser = argparse.ArgumentParser(
        description="LLM과 Kakao Local API로 국내 여행 추천 리포트를 생성합니다.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-date",
        "--date",
        dest="travel_date",
        required=True,
        metavar="YYYY-MM-DD",
        help="여행 날짜",
    )
    args = parser.parse_args()
    try:
        datetime.strptime(args.travel_date, "%Y-%m-%d")
    except ValueError:
        parser.error("-date/--date는 YYYY-MM-DD 형식의 실제 날짜여야 합니다.")
    return args


def redact_secrets(message: str) -> str:
    """오류 메시지에서 현재 환경의 비밀값을 제거한다."""
    safe = str(message)
    for variable in ("OPENAI_API_KEY", "KAKAO_REST_API_KEY"):
        secret = os.getenv(variable)
        if secret:
            safe = safe.replace(secret, "[REDACTED]")
    return re.sub(r"sk-[A-Za-z0-9_-]+", "[REDACTED]", safe)


def add_error(errors: list[dict[str, str]], step: str, error_type: str, message: str) -> None:
    """비밀값을 제거한 오류 요약을 결과 데이터에 추가한다."""
    errors.append({"step": step, "type": error_type, "message": redact_secrets(message)[:300]})


def validate_recommendation(data: Any) -> dict[str, Any]:
    """LLM 응답이 다음 API 호출에 사용할 최소 스키마를 만족하는지 검사한다."""
    if not isinstance(data, dict):
        raise ValueError("추천 결과의 최상위 형식이 객체가 아닙니다.")
    required_types = {
        "recommended_city": str,
        "weather": str,
        "events": list,
        "reason": str,
    }
    for key, expected_type in required_types.items():
        if key not in data or not isinstance(data[key], expected_type):
            raise ValueError(f"필수 키 또는 타입이 올바르지 않습니다: {key}")
    if not data["recommended_city"].strip() or not data["weather"].strip() or not data["reason"].strip():
        raise ValueError("문자열 필수 값이 비어 있습니다.")
    if not all(isinstance(event, str) for event in data["events"]):
        raise ValueError("events의 모든 항목은 문자열이어야 합니다.")
    return data


def build_openai_client() -> OpenAI:
    """환경변수로부터 OpenAI 호환 클라이언트를 생성한다."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise PlannerError(
            "OPENAI_API_KEY가 설정되지 않았습니다. .env에 OPENAI_API_KEY를 설정하거나 "
            "macOS/Linux에서 export OPENAI_API_KEY='YOUR_KEY'를 실행한 뒤 다시 시도하세요."
        )
    base_url = os.getenv("OPENAI_API_BASE")
    return OpenAI(api_key=api_key, base_url=base_url or None)


def create_recommendation(client: OpenAI, travel_date: str, errors: list[dict[str, str]]) -> dict[str, Any]:
    """날짜에 대한 구조화된 1차 여행 추천을 생성하고, 파싱 실패 시 한 번만 재시도한다."""
    model = os.getenv("OPENAI_MODEL", "gpt-5-mini")
    initial_prompt = f"""
여행 날짜는 {travel_date}입니다. 국내 여행지 한 곳을 추천하세요.
정확한 실시간 예보나 확정 행사 정보가 아니라, 해당 시기의 일반적인 경향과 후보를 제시하면 됩니다.
반드시 다음 JSON 스키마에 맞는 한국어 값만 반환하세요.
recommended_city는 도시 또는 지역명 문자열, weather는 일반적 날씨 요약 문자열,
events는 행사·축제 후보 문자열의 배열(1~3개), reason은 추천 근거 2~4문장 문자열입니다.
""".strip()
    repair_prompt = """
직전 응답은 JSON 파싱 또는 필수 키 검증에 실패했습니다.
설명·코드블록 없이, recommended_city, weather, events, reason 네 키만 가진 유효한 JSON 객체를 다시 반환하세요.
""".strip()

    for attempt in range(2):
        try:
            messages = [
                {"role": "system", "content": "당신은 구조화된 한국 국내 여행 추천 데이터를 생성하는 도우미입니다."},
                {"role": "user", "content": initial_prompt if attempt == 0 else repair_prompt},
            ]
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                response_format=RECOMMENDATION_SCHEMA,
                max_completion_tokens=700,
            )
            content = response.choices[0].message.content or ""
            return validate_recommendation(json.loads(content))
        except (json.JSONDecodeError, ValueError, IndexError, TypeError) as exc:
            if attempt == 0:
                print("  - LLM JSON 검증 실패: 형식을 보정하여 1회 재시도합니다.")
                continue
            add_error(errors, "recommendation", "JSON_PARSE_ERROR", str(exc))
            raise PlannerError("LLM 추천 JSON을 생성하지 못했습니다. 잠시 후 다시 시도하세요.") from exc
        except APIConnectionError as exc:
            add_error(errors, "recommendation", "NETWORK_ERROR", str(exc))
            raise PlannerError("LLM API 네트워크 연결에 실패했습니다. 연결 상태를 확인하세요.") from exc
        except APIStatusError as exc:
            status = getattr(exc, "status_code", "unknown")
            error_type = "AUTH_OR_QUOTA_ERROR" if status in (401, 403, 429) else "API_STATUS_ERROR"
            add_error(errors, "recommendation", error_type, f"HTTP {status}")
            raise PlannerError(f"LLM API 요청에 실패했습니다(HTTP {status}). 키와 쿼터를 확인하세요.") from exc

    raise PlannerError("LLM 추천 생성 재시도 한도를 초과했습니다.")


def normalize_place(place: dict[str, Any]) -> dict[str, Any]:
    """Kakao 응답을 과제에서 요구한 공통 장소 스키마로 변환한다."""
    def number_or_none(value: Any) -> float | None:
        try:
            return float(value) if value not in (None, "") else None
        except (TypeError, ValueError):
            return None

    return {
        "name": str(place.get("place_name", "")),
        "address": str(place.get("road_address_name") or place.get("address_name") or ""),
        "category": str(place.get("category_name", "")),
        "url": str(place.get("place_url", "")),
        "x": number_or_none(place.get("x")),
        "y": number_or_none(place.get("y")),
    }


def search_restaurants(city: str, errors: list[dict[str, str]]) -> list[dict[str, Any]]:
    """Kakao Local 키워드 API를 호출하고, 실패 시 빈 목록을 반환하여 다음 단계를 지속한다."""
    kakao_key = os.getenv("KAKAO_REST_API_KEY")
    query = f"{city} 맛집"
    if not kakao_key:
        add_error(
            errors,
            "place_search",
            "MISSING_API_KEY",
            "KAKAO_REST_API_KEY가 없어 장소 검색을 건너뛰었습니다. .env에 키를 설정하세요.",
        )
        print("  - KAKAO_REST_API_KEY 미설정: 맛집을 '데이터 없음'으로 처리하고 계속합니다.")
        return []

    try:
        response = requests.get(
            KAKAO_KEYWORD_URL,
            headers={"Authorization": f"KakaoAK {kakao_key}"},
            params={"query": query, "size": 5},
            timeout=TIMEOUT_SECONDS,
        )
        if response.status_code in (401, 403):
            add_error(errors, "place_search", "AUTH_ERROR", f"HTTP {response.status_code}")
            print(f"  - 장소 검색 인증 실패(HTTP {response.status_code}): 데이터 없음으로 계속합니다.")
            return []
        if response.status_code == 429:
            add_error(errors, "place_search", "QUOTA_ERROR", "HTTP 429")
            print("  - 장소 검색 쿼터 제한(HTTP 429): 데이터 없음으로 계속합니다.")
            return []
        response.raise_for_status()
        payload = response.json()
        documents = payload.get("documents", [])
        if not isinstance(documents, list):
            raise ValueError("Kakao 응답의 documents 형식이 목록이 아닙니다.")
        places = [normalize_place(item) for item in documents[:5] if isinstance(item, dict)]
        if not places:
            add_error(errors, "place_search", "EMPTY_RESULT", f"0 results for query={query}")
            print("  - 검색 결과 0건: 데이터 없음으로 계속합니다.")
        return places
    except requests.Timeout:
        add_error(errors, "place_search", "NETWORK_TIMEOUT", f"timeout after {TIMEOUT_SECONDS} seconds")
        print("  - 장소 검색 시간 초과: 데이터 없음으로 계속합니다.")
    except requests.RequestException as exc:
        add_error(errors, "place_search", "NETWORK_OR_HTTP_ERROR", str(exc))
        print("  - 장소 검색 요청 실패: 데이터 없음으로 계속합니다.")
    except (ValueError, json.JSONDecodeError) as exc:
        add_error(errors, "place_search", "RESPONSE_PARSE_ERROR", str(exc))
        print("  - 장소 검색 응답 파싱 실패: 데이터 없음으로 계속합니다.")
    return []


def fallback_report(travel_date: str, recommendation: dict[str, Any], places: list[dict[str, Any]], errors: list[dict[str, str]]) -> str:
    """최종 LLM 호출이 실패한 경우에도 결과 파일을 남기기 위한 최소 리포트이다."""
    restaurants = "\n".join(
        f"- **{place['name']}** — {place['address']}" for place in places
    ) or "- 데이터 없음 (장소 검색 결과가 없거나 API 호출에 실패했습니다.)"
    events = "\n".join(f"- {event}" for event in recommendation["events"]) or "- 데이터 없음"
    error_text = "\n".join(
        f"- [{item['step']}/{item['type']}] {item['message']}" for item in errors
    ) or "- 없음"
    return f"""# {travel_date} 국내 여행 추천 리포트

> 최종 LLM 리포트 생성에 실패해, 확보한 원본 데이터로 만든 대체 리포트입니다.

## 추천 지역

**{recommendation['recommended_city']}**

## 추천 이유

{recommendation['reason']}

## 날씨 요약

{recommendation['weather']}

## 행사/축제

{events}

## 맛집 추천

{restaurants}

## 1일 일정 제안

오전에는 대표 관광지와 산책 코스를 둘러보고, 오후에는 지역 문화 공간 또는 카페를 방문합니다. 저녁에는 위 맛집 목록을 확인해 식사하고 야간 산책으로 하루를 마무리합니다.

## 오류 요약(errors)

{error_text}
"""


def create_report(
    client: OpenAI,
    travel_date: str,
    recommendation: dict[str, Any],
    places: list[dict[str, Any]],
    errors: list[dict[str, str]],
) -> str:
    """구조화된 추천·장소 데이터를 기반으로 최종 Markdown 리포트를 생성한다."""
    model = os.getenv("OPENAI_MODEL", "gpt-5-mini")
    source_data = json.dumps(
        {"recommendation": recommendation, "restaurants": places, "errors": errors},
        ensure_ascii=False,
        indent=2,
    )
    prompt = f"""
다음은 {travel_date} 국내 여행 추천을 위한 구조화된 입력 데이터입니다.
이 데이터만 근거로 자연스러운 한국어 Markdown 여행 리포트를 작성하세요.

{source_data}

반드시 다음 제목을 모두 포함하세요.
1. 추천 지역
2. 추천 이유
3. 날씨 요약
4. 행사/축제
5. 맛집 추천
6. 1일 일정 제안
7. 오류 요약(errors)
맛집 목록이 비어 있으면 맛집 추천 섹션에 정확히 '데이터 없음'이라고 적으세요.
행사 후보는 확정 정보처럼 단정하지 말고 '후보'임을 밝혀 주세요.
""".strip()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "당신은 제공된 데이터에만 근거해 Markdown 여행 리포트를 쓰는 도우미입니다."},
                {"role": "user", "content": prompt},
            ],
            max_completion_tokens=1400,
        )
        report = response.choices[0].message.content or ""
        if not report.strip():
            raise ValueError("빈 리포트가 반환되었습니다.")
        return f"# {travel_date} 국내 여행 추천 리포트\n\n{report.lstrip('# ').strip()}\n"
    except (APIConnectionError, APIStatusError, ValueError, IndexError, TypeError) as exc:
        add_error(errors, "report_generation", "LLM_REPORT_ERROR", str(exc))
        print("  - 최종 리포트 LLM 생성 실패: 대체 Markdown 리포트를 저장합니다.")
        return fallback_report(travel_date, recommendation, places, errors)


def write_results(travel_date: str, recommendation: dict[str, Any], places: list[dict[str, Any]], errors: list[dict[str, str]], report: str) -> tuple[Path, Path]:
    """원본 JSON과 최종 Markdown 리포트를 날짜 기준 파일명으로 저장한다."""
    RESULTS_DIR.mkdir(exist_ok=True)
    json_path = RESULTS_DIR / f"{travel_date}_travel_data.json"
    report_path = RESULTS_DIR / f"{travel_date}_travel_plan.md"
    raw_data = {
        "travel_date": travel_date,
        "recommendation": recommendation,
        "restaurants": places,
        "errors": errors,
    }
    json_path.write_text(json.dumps(raw_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(report, encoding="utf-8")
    return json_path, report_path


def main() -> int:
    """프로그램의 실행 순서를 제어한다."""
    args = parse_args()
    load_dotenv(BASE_DIR / ".env")
    errors: list[dict[str, str]] = []

    try:
        client = build_openai_client()
        print("[1/3] 1차 추천 생성 중(LLM)...")
        recommendation = create_recommendation(client, args.travel_date, errors)
        print(f"  - recommended_city: {recommendation['recommended_city']}")

        print("[2/3] 맛집 검색 중(Kakao Local API)...")
        places = search_restaurants(recommendation["recommended_city"], errors)
        print(f"  - 맛집 {len(places)}곳 검색 완료")

        print("[3/3] 최종 리포트 생성 중(LLM)...")
        report = create_report(client, args.travel_date, recommendation, places, errors)
        json_path, report_path = write_results(args.travel_date, recommendation, places, errors, report)
        print("  - 리포트 생성 완료")
        print(f"완료! {report_path.relative_to(BASE_DIR)} 및 {json_path.relative_to(BASE_DIR)}를 확인하세요.")
        return 0
    except PlannerError as exc:
        print(f"오류: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
