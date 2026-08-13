"""A1-1 과제: 메모리 기반 Python 콘솔 프롬프트 관리자."""

from __future__ import annotations

from copy import deepcopy
from typing import TypedDict


class Prompt(TypedDict):
    """프롬프트 한 건의 데이터 구조."""

    title: str
    content: str
    category: str
    favorite: bool


CATEGORIES = (
    "텍스트 생성",
    "이미지 생성",
    "영상 생성",
    "페르소나",
    "자동화",
    "기타",
)

DEFAULT_PROMPTS: list[Prompt] = [
    {
        "title": "블로그 초안 작성",
        "content": "당신은 친절한 콘텐츠 마케터입니다. 주제를 바탕으로 독자가 이해하기 쉬운 블로그 초안을 작성하세요.",
        "category": "텍스트 생성",
        "favorite": True,
    },
    {
        "title": "따뜻한 책방 포스터",
        "content": "비 오는 오후의 독립 서점을 홍보하는 따뜻한 분위기의 포스터를 제작하세요. 수채화 질감과 부드러운 조명을 사용합니다.",
        "category": "이미지 생성",
        "favorite": False,
    },
    {
        "title": "학습 코치 페르소나",
        "content": "당신은 초보 학습자의 목표를 작은 단계로 나누고 격려하는 학습 코치입니다. 쉬운 한국어로 답변하세요.",
        "category": "페르소나",
        "favorite": False,
    },
]

MENU_OPTIONS = {
    "1": "전체 프롬프트 목록 보기",
    "8": "종료",
}


def create_initial_prompts() -> list[Prompt]:
    """기본 프롬프트를 복사해 실행별 독립 목록을 생성한다."""

    return deepcopy(DEFAULT_PROMPTS)


def show_prompt_list(prompts: list[Prompt], heading: str = "전체 프롬프트 목록") -> None:
    """프롬프트 목록을 번호, 제목, 카테고리, 즐겨찾기 표시와 함께 출력한다."""

    print(f"\n[ {heading} ]")
    if not prompts:
        print("저장된 프롬프트가 없습니다.")
        return

    for number, prompt in enumerate(prompts, start=1):
        favorite_mark = "⭐" if prompt["favorite"] else "-"
        print(
            f"{number}. {prompt['title']} | 카테고리: {prompt['category']} | "
            f"즐겨찾기: {favorite_mark}"
        )


def show_menu() -> None:
    """현재 제공하는 콘솔 메뉴를 출력한다."""

    print("\n" + "=" * 42)
    print("       Python 콘솔 프롬프트 관리자")
    print("=" * 42)
    for number, label in MENU_OPTIONS.items():
        print(f"{number}. {label}")


def get_menu_choice() -> str:
    """유효한 메뉴 번호가 입력될 때까지 재입력받는다."""

    while True:
        choice = input("메뉴 번호를 입력하세요: ").strip()
        if choice in MENU_OPTIONS:
            return choice
        print("잘못된 메뉴 번호입니다. 표시된 번호를 입력하세요.")


def main() -> None:
    """메뉴를 반복 출력하고 종료 선택을 처리한다."""

    prompts = create_initial_prompts()
    print("프롬프트 관리자에 오신 것을 환영합니다.")
    while True:
        show_menu()
        choice = get_menu_choice()
        if choice == "1":
            show_prompt_list(prompts)
        elif choice == "8":
            print("프롬프트 관리자를 종료합니다. 안녕히 가세요.")
            break


if __name__ == "__main__":
    main()
