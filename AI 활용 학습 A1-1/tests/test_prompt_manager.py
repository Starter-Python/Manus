"""A1-1 프롬프트 관리자의 데이터 처리와 콘솔 메뉴 흐름을 검증한다."""

from contextlib import redirect_stdout
from io import StringIO
import unittest
from unittest.mock import patch

from prompt_manager import (
    CATEGORIES,
    UserInputCancelled,
    add_prompt,
    create_initial_prompts,
    filter_prompts_by_category,
    find_duplicate_prompt,
    find_prompts,
    format_prompt_summary,
    get_favorite_prompts,
    get_view_categories,
    is_valid_prompt_number,
    main,
    normalize_prompt_text,
    read_user_input,
    run_menu_loop,
)


class PromptManagerTest(unittest.TestCase):
    """기본 데이터, 중복 검증, 필터, 검색, 콘솔 실행 흐름을 확인한다."""

    def test_initial_prompts_have_ten_required_records(self) -> None:
        prompts = create_initial_prompts()

        self.assertEqual(len(prompts), 10)
        self.assertTrue(set(CATEGORIES).issubset({prompt["category"] for prompt in prompts}))
        for prompt in prompts:
            self.assertEqual(
                set(prompt),
                {"title", "content", "category", "favorite"},
            )
            self.assertIn(prompt["category"], CATEGORIES)
            self.assertIsInstance(prompt["favorite"], bool)

    def test_initial_prompts_are_independent_between_runs(self) -> None:
        first_run = create_initial_prompts()
        second_run = create_initial_prompts()

        first_run[0]["favorite"] = False
        first_run.append(
            {
                "title": "임시 프롬프트",
                "content": "테스트용 데이터",
                "category": "기타",
                "favorite": False,
            }
        )

        self.assertTrue(second_run[0]["favorite"])
        self.assertEqual(len(second_run), 10)

    def test_prompt_number_validation(self) -> None:
        prompts = create_initial_prompts()

        self.assertTrue(is_valid_prompt_number("1", prompts))
        self.assertTrue(is_valid_prompt_number("10", prompts))
        self.assertFalse(is_valid_prompt_number("0", prompts))
        self.assertFalse(is_valid_prompt_number("-1", prompts))
        self.assertFalse(is_valid_prompt_number("1.5", prompts))
        self.assertFalse(is_valid_prompt_number("abc", prompts))
        self.assertFalse(is_valid_prompt_number("11", prompts))

    def test_view_categories_include_custom_categories(self) -> None:
        prompts = create_initial_prompts()
        prompts.append(
            {
                "title": "업무 보고 자동화",
                "content": "매일 업무 보고를 정리하세요.",
                "category": "업무",
                "favorite": False,
            }
        )

        self.assertEqual(get_view_categories(prompts), [*CATEGORIES, "업무"])

    def test_find_prompts_searches_title_and_content(self) -> None:
        prompts = create_initial_prompts()

        self.assertEqual([prompt["title"] for prompt in find_prompts(prompts, "학습")], ["학습 코치 페르소나"])
        self.assertEqual([prompt["title"] for prompt in find_prompts(prompts, "수채화")], ["따뜻한 책방 포스터"])
        self.assertEqual(find_prompts(prompts, "존재하지않음"), [])

    def test_category_filter_and_favorite_filter(self) -> None:
        prompts = create_initial_prompts()

        image_prompts = filter_prompts_by_category(prompts, "이미지 생성")
        favorites = get_favorite_prompts(prompts)

        self.assertEqual(
            [prompt["title"] for prompt in image_prompts],
            ["따뜻한 책방 포스터", "친환경 제품 상세 이미지"],
        )
        self.assertEqual(
            [prompt["title"] for prompt in favorites],
            ["블로그 초안 작성", "15초 릴스 스토리보드"],
        )

    def test_prompt_summary_contains_required_information(self) -> None:
        prompt = create_initial_prompts()[0]

        summary = format_prompt_summary(1, prompt)

        self.assertIn("1. 블로그 초안 작성", summary)
        self.assertIn("카테고리: 텍스트 생성", summary)
        self.assertIn("즐겨찾기: ⭐", summary)

    def test_duplicate_prompt_ignores_case_and_extra_spaces(self) -> None:
        prompts = create_initial_prompts()
        original = prompts[0]

        duplicate = find_duplicate_prompt(
            prompts,
            "  블로그   초안 작성  ",
            f"  {original['content']}  ",
        )

        self.assertEqual(normalize_prompt_text(" AI   Prompt "), "ai prompt")
        self.assertIsNotNone(duplicate)
        self.assertEqual(duplicate["title"], "블로그 초안 작성")
        self.assertIsNone(find_duplicate_prompt(prompts, "블로그 초안 작성", "다른 내용"))

    def test_add_prompt_blocks_duplicate_without_changing_list(self) -> None:
        prompts = create_initial_prompts()
        original = prompts[0]
        output = StringIO()

        with patch(
            "builtins.input",
            side_effect=[f"  {original['title']}  ", f"  {original['content']}  "],
        ):
            with redirect_stdout(output):
                add_prompt(prompts)

        self.assertEqual(len(prompts), 10)
        self.assertIn("동일한 프롬프트가 이미 존재합니다", output.getvalue())

    def test_menu_two_and_three_show_expected_lists(self) -> None:
        output = StringIO()
        with patch("builtins.input", side_effect=["2", "3", "1", "8"]):
            with redirect_stdout(output):
                run_menu_loop(create_initial_prompts())

        result = output.getvalue()
        self.assertIn("[ 전체 프롬프트 목록 ]", result)
        self.assertIn("1. 블로그 초안 작성", result)
        self.assertIn("10. 주간 회고 질문", result)
        self.assertIn("[ 텍스트 생성 프롬프트 ]", result)
        self.assertIn("프롬프트 관리자를 종료합니다.", result)

    def test_noninteractive_execution_shows_terminal_help(self) -> None:
        output = StringIO()
        with patch("prompt_manager.is_interactive_terminal", return_value=False):
            with redirect_stdout(output):
                main()

        result = output.getvalue()
        self.assertIn("실행 환경 안내", result)
        self.assertIn("통합 터미널", result)

    def test_eof_input_is_handled_as_cancelled_input(self) -> None:
        with patch("builtins.input", side_effect=EOFError):
            with self.assertRaises(UserInputCancelled):
                read_user_input("메뉴 번호를 입력하세요: ")


if __name__ == "__main__":
    unittest.main()
