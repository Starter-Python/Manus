"""A1-1 프롬프트 관리자의 데이터 처리와 콘솔 메뉴 흐름을 검증한다."""

from contextlib import redirect_stdout
from io import StringIO
import unittest
from unittest.mock import patch

from prompt_manager import (
    CATEGORIES,
    UserInputCancelled,
    create_initial_prompts,
    filter_prompts_by_category,
    find_prompts,
    format_prompt_summary,
    get_favorite_prompts,
    get_view_categories,
    is_valid_prompt_number,
    main,
    read_user_input,
    run_menu_loop,
)


class PromptManagerTest(unittest.TestCase):
    """기본 데이터, 필터, 검색, 콘솔 실행 흐름을 확인한다."""

    def test_initial_prompts_have_required_fields(self) -> None:
        prompts = create_initial_prompts()

        self.assertGreaterEqual(len(prompts), 3)
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
        self.assertEqual(len(second_run), 3)

    def test_prompt_number_validation(self) -> None:
        prompts = create_initial_prompts()

        self.assertTrue(is_valid_prompt_number("1", prompts))
        self.assertTrue(is_valid_prompt_number(str(len(prompts)), prompts))
        self.assertFalse(is_valid_prompt_number("0", prompts))
        self.assertFalse(is_valid_prompt_number("-1", prompts))
        self.assertFalse(is_valid_prompt_number("1.5", prompts))
        self.assertFalse(is_valid_prompt_number("abc", prompts))
        self.assertFalse(is_valid_prompt_number(str(len(prompts) + 1), prompts))

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

        self.assertEqual([prompt["title"] for prompt in image_prompts], ["따뜻한 책방 포스터"])
        self.assertEqual([prompt["title"] for prompt in favorites], ["블로그 초안 작성"])

    def test_prompt_summary_contains_required_information(self) -> None:
        prompt = create_initial_prompts()[0]

        summary = format_prompt_summary(1, prompt)

        self.assertIn("1. 블로그 초안 작성", summary)
        self.assertIn("카테고리: 텍스트 생성", summary)
        self.assertIn("즐겨찾기: ⭐", summary)

    def test_menu_two_and_three_show_expected_lists(self) -> None:
        output = StringIO()
        with patch("builtins.input", side_effect=["2", "3", "1", "8"]):
            with redirect_stdout(output):
                run_menu_loop(create_initial_prompts())

        result = output.getvalue()
        self.assertIn("[ 전체 프롬프트 목록 ]", result)
        self.assertIn("1. 블로그 초안 작성", result)
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
