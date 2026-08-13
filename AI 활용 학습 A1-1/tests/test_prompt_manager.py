"""A1-1 프롬프트 관리자의 순수 데이터 처리 로직을 검증한다."""

import unittest

from prompt_manager import (
    CATEGORIES,
    create_initial_prompts,
    find_prompts,
    get_view_categories,
    is_valid_prompt_number,
)


class PromptManagerTest(unittest.TestCase):
    """기본 데이터, 검색, 유효성 검증 로직을 확인한다."""

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


if __name__ == "__main__":
    unittest.main()
