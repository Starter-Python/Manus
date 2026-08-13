"""온기록의 Vercel Python Serverless Function.

디자인 원칙: AI는 회복 루틴의 '정답'이 아니라 사용자가 조정할 수 있는 짧은 초안을 만든다.
보안 원칙: API 키는 OPENAI_API_KEY 환경 변수에서만 읽으며, HTTP 응답·로그에 노출하지 않는다.
"""

from __future__ import annotations

import json
import os
import re
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from typing import Any

from openai import APIConnectionError, APIStatusError, AuthenticationError, OpenAI, RateLimitError


MAX_NOTE_LENGTH = 200
ALLOWED_MINUTES = {"5", "15", "30"}


def safe_text(value: Any, limit: int = 200) -> str:
    """입력 크기를 제한하고 제어 문자를 제거한다."""
    if not isinstance(value, str):
        return ""
    return re.sub(r"[\x00-\x1f\x7f]", " ", value).strip()[:limit]


def parse_routine(raw: str) -> dict[str, Any]:
    """모델 출력에서 JSON 객체만 추출하고 최소 형식을 보장한다."""
    match = re.search(r"\{.*\}", raw, flags=re.DOTALL)
    if not match:
        raise ValueError("AI 결과를 읽을 수 없습니다.")

    data = json.loads(match.group(0))
    steps = data.get("steps", [])
    if not isinstance(steps, list):
        steps = []

    cleaned_steps = [safe_text(step, 160) for step in steps if safe_text(step, 160)][:3]
    if len(cleaned_steps) < 3:
        raise ValueError("AI 결과의 단계가 충분하지 않습니다.")

    return {
        "kicker": safe_text(data.get("kicker"), 50) or "오늘의 작은 계획",
        "title": safe_text(data.get("title"), 90) or "당신의 회복 루틴",
        "opening": safe_text(data.get("opening"), 260) or "지금 가능한 만큼만 시작해 보세요.",
        "steps": cleaned_steps,
        "note": safe_text(data.get("note"), 220) or "가장 쉬운 단계 하나만 골라도 충분합니다.",
    }


def build_prompt(feeling: str, minutes: str, focus: str, note: str) -> str:
    """서비스 목적에 맞는 짧고 안전한 JSON 응답을 요청한다."""
    optional_note = note if note else "(사용자가 추가 문장을 남기지 않았습니다.)"
    return f"""
당신은 한국어 웰니스 서비스 '온기록'의 루틴 편집 도우미입니다.
사용자가 오늘 바로 해볼 수 있는, 부담이 낮은 일상 회복 루틴의 초안을 작성합니다.
의료적 진단, 치료, 약물 조언, 확정적 심리 판단은 하지 마세요. 위기·자해·타해가 언급되면
다른 루틴을 제시하지 말고 가까운 사람·지역의 응급 서비스·전문 도움에 즉시 연락하도록 부드럽고 명확하게 안내하세요.

사용자 상태: {feeling}
확보 시간: {minutes}분
원하는 감각: {focus}
사용자 메모: {optional_note}

규칙:
1. 총 {minutes}분 안에 가능한 3단계로 구성하고, 각 단계에 대략적인 시간 또는 행동의 크기를 포함하세요.
2. 지나치게 낙관적이거나 훈계하는 말투를 피하고, 선택과 조정의 여지를 남기세요.
3. 결과는 한국어로만 작성하고, 마크다운이나 코드 블록 없이 아래 JSON 객체 하나만 반환하세요.
4. JSON 키는 kicker, title, opening, steps, note를 정확히 사용하세요. steps는 정확히 3개 문자열의 배열이어야 합니다.

응답 예시 형식:
{{"kicker":"15분의 정리","title":"머릿속을 비우는 짧은 틈","opening":"지금의 복잡함을 해결하려 하지 않고, 잠시 분리해 봅니다.","steps":["1분 — ...","10분 — ...","4분 — ..."],"note":"..."}}
"""


class handler(BaseHTTPRequestHandler):
    """POST /api/recommend 요청을 받아 OpenAI Responses API를 호출한다."""

    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler interface
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Allow", "POST, OPTIONS")
        self.end_headers()

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler interface
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length <= 0 or content_length > 4096:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "요청 내용을 확인해 주세요."})
            return

        try:
            payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "입력 형식을 읽을 수 없습니다."})
            return

        feeling = safe_text(payload.get("feeling"), 80)
        minutes = safe_text(payload.get("minutes"), 8)
        focus = safe_text(payload.get("focus"), 80)
        note = safe_text(payload.get("note"), MAX_NOTE_LENGTH)

        if not feeling or minutes not in ALLOWED_MINUTES or not focus:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": "현재 상태, 시간, 원하는 감각을 모두 입력해 주세요."})
            return

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            self._send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"error": "AI 기능 설정이 아직 완료되지 않았습니다. 관리자에게 환경 변수 설정을 요청해 주세요."})
            return

        try:
            client = OpenAI(api_key=api_key, timeout=10.0, max_retries=1)
            response = client.responses.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
                input=build_prompt(feeling, minutes, focus, note),
            )
            self._send_json(HTTPStatus.OK, parse_routine(response.output_text))
        except AuthenticationError:
            self._send_json(HTTPStatus.SERVICE_UNAVAILABLE, {"error": "AI 기능 인증 설정을 확인해 주세요."})
        except RateLimitError:
            self._send_json(HTTPStatus.TOO_MANY_REQUESTS, {"error": "요청이 잠시 많습니다. 잠깐 후 다시 시도해 주세요."})
        except APIConnectionError:
            self._send_json(HTTPStatus.BAD_GATEWAY, {"error": "AI 서비스와 연결하지 못했습니다. 잠시 후 다시 시도해 주세요."})
        except APIStatusError:
            self._send_json(HTTPStatus.BAD_GATEWAY, {"error": "AI 서비스가 응답하지 않습니다. 잠시 후 다시 시도해 주세요."})
        except (ValueError, json.JSONDecodeError):
            self._send_json(HTTPStatus.BAD_GATEWAY, {"error": "루틴 결과를 정리하지 못했습니다. 다시 시도해 주세요."})
        except Exception:  # 내부 세부 정보와 키를 응답에 노출하지 않는다.
            self._send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "예기치 못한 문제가 발생했습니다. 잠시 후 다시 시도해 주세요."})

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler interface
        self._send_json(HTTPStatus.METHOD_NOT_ALLOWED, {"error": "POST 요청만 사용할 수 있습니다."})

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        """민감한 요청 본문이나 API 키가 로그에 남지 않도록 기본 로그를 비활성화한다."""
        return
