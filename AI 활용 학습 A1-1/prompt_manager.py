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
    "1": "프롬프트 추가",
    "2": "전체 프롬프트 목록 보기",
    "3": "카테고리별 조회",
    "4": "프롬프트 검색",
    "5": "프롬프트 상세 보기",
    "6": "즐겨찾기 추가/해제",
    "7": "즐겨찾기 목록 보기",
    "8": "종료",
}


def create_initial_prompts() -> list[Prompt]:
    """기본 프롬프트를 복사해 실행별 독립 목록을 생성한다."""

    return deepcopy(DEFAULT_PROMPTS)


def get_non_empty_input(label: str) -> str:
    """공백이 아닌 값이 입력될 때까지 사용자의 입력을 받는다."""

    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print(f"{label}은(는) 비워둘 수 없습니다. 다시 입력하세요.")


def is_valid_prompt_number(value: str, prompts: list[Prompt]) -> bool:
    """입력값이 현재 목록 범위의 프롬프트 번호인지 판별한다."""

    return value.isdigit() and 1 <= int(value) <= len(prompts)


def get_prompt_index(prompts: list[Prompt]) -> int | None:
    """유효한 프롬프트 번호를 0부터 시작하는 목록 위치로 변환한다."""

    if not prompts:
        print("저장된 프롬프트가 없습니다.")
        return None

    while True:
        value = input("프롬프트 번호를 입력하세요: ").strip()
        if is_valid_prompt_number(value, prompts):
            return int(value) - 1
        print("잘못된 프롬프트 번호입니다. 목록의 번호를 입력하세요.")


def choose_category() -> str:
    """기본 카테고리를 선택하거나 새 카테고리를 직접 입력하도록 한다."""

    print("카테고리를 선택하세요.")
    for number, category in enumerate(CATEGORIES, start=1):
        print(f"{number}. {category}")
    print("0. 직접 입력")

    while True:
        choice = input("카테고리 번호를 입력하세요: ").strip()
        if choice == "0":
            return get_non_empty_input("직접 입력할 카테고리")
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        print("잘못된 카테고리 번호입니다. 다시 입력하세요.")


def add_prompt(prompts: list[Prompt]) -> None:
    """제목, 내용, 카테고리를 입력받아 즐겨찾기 해제 상태로 새 프롬프트를 추가한다."""

    print("\n[ 새 프롬프트 추가 ]")
    title = get_non_empty_input("제목")
    content = get_non_empty_input("내용")
    category = choose_category()
    prompts.append(
        {
            "title": title,
            "content": content,
            "category": category,
            "favorite": False,
        }
    )
    print(f"'{title}' 프롬프트가 추가되었습니다.")


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


def get_view_categories(prompts: list[Prompt]) -> list[str]:
    """기본 카테고리와 직접 추가된 카테고리를 중복 없이 반환한다."""

    custom_categories = sorted(
        {prompt["category"] for prompt in prompts if prompt["category"] not in CATEGORIES}
    )
    return [*CATEGORIES, *custom_categories]


def select_category_to_view(prompts: list[Prompt]) -> str:
    """조회할 카테고리를 선택받는다."""

    categories = get_view_categories(prompts)
    print("조회할 카테고리를 선택하세요.")
    for number, category in enumerate(categories, start=1):
        print(f"{number}. {category}")

    while True:
        choice = input("카테고리 번호를 입력하세요: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            return categories[int(choice) - 1]
        print("잘못된 카테고리 번호입니다. 다시 입력하세요.")


def show_prompts_by_category(prompts: list[Prompt]) -> None:
    """선택한 카테고리에 속한 프롬프트만 출력한다."""

    category = select_category_to_view(prompts)
    filtered_prompts = [prompt for prompt in prompts if prompt["category"] == category]
    show_prompt_list(filtered_prompts, f"{category} 프롬프트")


def find_prompts(prompts: list[Prompt], keyword: str) -> list[Prompt]:
    """제목 또는 내용에 키워드가 포함된 프롬프트를 반환한다."""

    normalized_keyword = keyword.casefold()
    return [
        prompt
        for prompt in prompts
        if normalized_keyword in prompt["title"].casefold()
        or normalized_keyword in prompt["content"].casefold()
    ]


def search_prompts(prompts: list[Prompt]) -> None:
    """키워드를 입력받아 제목 또는 내용에서 일치하는 프롬프트를 출력한다."""

    keyword = get_non_empty_input("검색 키워드")
    show_prompt_list(find_prompts(prompts, keyword), f"'{keyword}' 검색 결과")


def show_prompt_detail(prompts: list[Prompt]) -> None:
    """선택한 프롬프트의 모든 핵심 정보를 출력한다."""

    print("\n[ 프롬프트 상세 보기 ]")
    index = get_prompt_index(prompts)
    if index is None:
        return

    prompt = prompts[index]
    favorite_status = "⭐ 즐겨찾기" if prompt["favorite"] else "- 즐겨찾기 아님"
    print(f"제목: {prompt['title']}")
    print(f"카테고리: {prompt['category']}")
    print(f"즐겨찾기: {favorite_status}")
    print("내용:")
    print(prompt["content"])


def toggle_favorite(prompts: list[Prompt]) -> None:
    """선택한 프롬프트의 즐겨찾기 상태를 추가 또는 해제한다."""

    print("\n[ 즐겨찾기 추가/해제 ]")
    index = get_prompt_index(prompts)
    if index is None:
        return

    prompt = prompts[index]
    prompt["favorite"] = not prompt["favorite"]
    action = "추가" if prompt["favorite"] else "해제"
    print(f"'{prompt['title']}' 프롬프트를 즐겨찾기에서 {action}했습니다.")


def show_favorites(prompts: list[Prompt]) -> None:
    """즐겨찾기된 프롬프트만 모아 출력한다."""

    favorite_prompts = [prompt for prompt in prompts if prompt["favorite"]]
    show_prompt_list(favorite_prompts, "즐겨찾기 프롬프트")


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
            add_prompt(prompts)
        elif choice == "2":
            show_prompt_list(prompts)
        elif choice == "3":
            show_prompts_by_category(prompts)
        elif choice == "4":
            search_prompts(prompts)
        elif choice == "5":
            show_prompt_detail(prompts)
        elif choice == "6":
            toggle_favorite(prompts)
        elif choice == "7":
            show_favorites(prompts)
        elif choice == "8":
            print("프롬프트 관리자를 종료합니다. 안녕히 가세요.")
            break


if __name__ == "__main__":
    main()
