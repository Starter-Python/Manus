# `prompt_manager.py` 파일 구조와 동작 원리

이 문서는 A1-1 과제의 핵심 파일인 `prompt_manager.py`를 위에서 아래로 읽으며 이해할 수 있도록 설명합니다. 이 파일은 **터미널에서 메뉴 번호를 입력받아 프롬프트를 관리하는 콘솔 프로그램**입니다. 프로그램을 종료하면 실행 중의 데이터는 사라지고, 다음 실행에서는 기본 예시 데이터로 다시 시작합니다.

> 가장 중요한 실행 조건은 **VSCode 통합 터미널**입니다. 이 파일은 `input()`으로 사용자의 키보드 입력을 받으므로, Output 창·Debug Console·Code Runner의 `Run Code`가 아니라 `Terminal > New Terminal`에서 실행해야 합니다.

## 1. 파일 전체 흐름 한눈에 보기

```text
프로그램 실행
    ↓
if __name__ == "__main__"
    ↓
main()
    ├─ 통합 터미널인지 확인
    │   └─ 아니면 실행 방법을 안내하고 종료
    ├─ 기본 프롬프트 목록을 새로 복사
    └─ run_menu_loop()
         ├─ 메뉴 출력
         ├─ 번호 입력·검증
         ├─ 선택한 기능 함수 실행
         └─ 8번을 누를 때까지 반복
```

| 큰 구역 | 핵심 역할 | 관련 코드 |
| --- | --- | --- |
| 데이터 정의 | 프롬프트가 어떤 정보를 가져야 하는지 정의 | `Prompt`, `CATEGORIES`, `DEFAULT_PROMPTS` |
| 실행 환경 확인 | 입력 가능한 통합 터미널인지 확인 | `is_interactive_terminal()`, `show_terminal_execution_help()` |
| 입력 검증 | 빈 값·잘못된 번호·입력 중단을 안전하게 처리 | `read_user_input()`, `get_non_empty_input()`, `get_menu_choice()` |
| 데이터 처리 | 추가, 검색, 카테고리 필터, 즐겨찾기 처리 | `add_prompt()`, `find_prompts()`, `filter_prompts_by_category()` |
| 화면 출력 | 목록, 상세 정보, 메뉴를 화면에 보여 줌 | `show_prompt_list()`, `show_prompt_detail()`, `show_menu()` |
| 실행 제어 | 메뉴 선택을 기능 함수와 연결 | `run_menu_loop()`, `main()` |

## 2. 맨 위: 모듈 설명과 import

파일 첫 줄의 큰따옴표 문자열은 이 파일이 무엇을 하는지 설명하는 **docstring**입니다. 그 아래에는 필요한 표준 라이브러리를 불러옵니다.

```python
from copy import deepcopy
import sys
from typing import TypedDict
```

| import | 사용하는 이유 |
| --- | --- |
| `deepcopy` | 기본 예시 데이터를 안전하게 복사해, 한 번 실행한 뒤의 변경이 다음 실행에 남지 않도록 합니다. |
| `sys` | 현재 실행 환경이 사용자 입력을 받을 수 있는 터미널인지 확인합니다. |
| `TypedDict` | 프롬프트 딕셔너리에 어떤 키가 필요한지 코드 수준에서 분명히 표시합니다. |

외부 패키지를 설치하지 않고 Python 표준 라이브러리만 사용하므로, `pip install` 없이 실행할 수 있습니다.

## 3. `Prompt`: 프롬프트 데이터의 설계도

`Prompt`는 실제 클래스로 객체를 만드는 용도보다, **딕셔너리가 어떤 키를 가져야 하는지 알려 주는 설계도**입니다.

```python
class Prompt(TypedDict):
    title: str
    content: str
    category: str
    favorite: bool
```

프롬프트 한 건은 아래와 같은 딕셔너리입니다.

```python
{
    "title": "회의록 요약",
    "content": "다음 회의록을 세 문장으로 요약하세요.",
    "category": "자동화",
    "favorite": False,
}
```

| 키 | 자료형 | 의미 |
| --- | --- | --- |
| `title` | 문자열 | 목록에서 빠르게 구분하는 제목 |
| `content` | 문자열 | 실제로 사용할 프롬프트 전체 내용 |
| `category` | 문자열 | 텍스트 생성, 이미지 생성, 자동화 등의 분류 |
| `favorite` | 불리언 | 즐겨찾기 여부. `True`면 별을 표시 |

전체 프롬프트는 여러 개가 필요하므로 `list[Prompt]`에 저장합니다. 즉 **리스트 안에 프롬프트 딕셔너리가 여러 개 들어 있는 구조**입니다.

## 4. 상수: 카테고리, 기본 데이터, 메뉴

### 4-1. `CATEGORIES`

`CATEGORIES`는 프로그램이 처음부터 제공하는 카테고리 목록입니다. 튜플로 만들었기 때문에 실행 중에 실수로 값이 바뀌지 않습니다. 새 프롬프트를 추가할 때 번호로 선택하는 메뉴의 원본이 됩니다.

### 4-2. `DEFAULT_PROMPTS`

`DEFAULT_PROMPTS`에는 프로그램을 시작할 때 보여 줄 예시 프롬프트 **10개**가 들어 있습니다. 텍스트 생성, 이미지 생성, 영상 생성, 페르소나, 자동화, 기타의 6개 카테고리를 모두 포함하며, 과제 요구사항인 ‘기본 데이터 3개 이상’을 넉넉히 만족합니다.

### 4-3. `MENU_OPTIONS`

`MENU_OPTIONS`는 메뉴 번호와 기능 이름을 연결하는 딕셔너리입니다.

```python
MENU_OPTIONS = {
    "1": "프롬프트 추가",
    "2": "전체 프롬프트 목록 보기",
    # 중간 생략
    "8": "종료",
}
```

메뉴 번호를 문자열로 저장한 이유는 `input()`이 항상 문자열을 반환하기 때문입니다. 예를 들어 사용자가 `2`를 입력해도 프로그램 내부에서는 `"2"`가 됩니다.

## 5. 실행 데이터 만들기: `create_initial_prompts()`

```python
def create_initial_prompts() -> list[Prompt]:
    return deepcopy(DEFAULT_PROMPTS)
```

이 함수는 기본 데이터를 그대로 돌려주지 않고 `deepcopy()`로 복사합니다. 만약 복사하지 않고 `DEFAULT_PROMPTS`를 그대로 사용하면, 실행 중에 즐겨찾기 상태를 바꾼 일이 원본 데이터에도 남을 수 있습니다. 깊은 복사는 리스트 안의 딕셔너리까지 모두 새로 복사하므로 실행마다 독립적인 목록을 만듭니다.

| 상황 | 깊은 복사 없이 사용했을 때 | `deepcopy()`를 사용했을 때 |
| --- | --- | --- |
| 즐겨찾기 변경 | 기본 데이터의 값도 바뀔 위험 | 현재 실행 목록만 바뀜 |
| 새 프롬프트 추가 | 다음 실행에 영향을 줄 수 있음 | 다음 실행은 다시 기본 10개부터 시작 |
| 테스트 | 테스트끼리 데이터가 섞일 수 있음 | 테스트마다 안전하게 독립 실행 |

## 6. VSCode 실행 환경 확인

`is_interactive_terminal()`은 `sys.stdin.isatty()`와 `sys.stdout.isatty()`를 사용해 현재 화면이 **입력 가능한 터미널인지** 확인합니다.

```python
def is_interactive_terminal() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()
```

VSCode의 통합 터미널은 일반적으로 이 조건을 만족합니다. 반대로 Code Runner의 Output 창처럼 입력이 불안정하거나 없는 환경에서는 조건이 거짓이 됩니다. 이때 `show_terminal_execution_help()`가 실행되어 메뉴가 멈춘 것처럼 보이는 대신, 어디에서 실행해야 하는지 안내합니다.

| 실행 방식 | 입력 가능 여부 | 프로그램 반응 |
| --- | --- | --- |
| VSCode `Terminal > New Terminal` | 가능 | 정상 메뉴 실행 |
| VSCode `Run Python File in Terminal` | 가능 | 정상 메뉴 실행 |
| Code Runner의 `Run Code` | 불안정하거나 불가 | 통합 터미널 실행 방법 안내 |
| Debug Console | 입력 불안정 | 통합 터미널 실행 방법 안내 |

## 7. 입력 처리 함수

### 7-1. `read_user_input()`

모든 사용자 입력은 `read_user_input()`을 거칩니다. 이 함수는 `input()`을 실행하고, 입력 스트림이 닫히는 `EOFError`나 사용자가 `Ctrl+C`를 누른 상황을 `UserInputCancelled` 예외로 통일합니다.

```python
def read_user_input(prompt: str) -> str:
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt) as error:
        raise UserInputCancelled from error
```

이 구조 덕분에 입력이 갑자기 끊겨도 복잡한 오류 화면 대신 `main()`에서 “입력이 중단되어 프로그램을 종료합니다.”라는 안내를 보여 줄 수 있습니다.

### 7-2. `get_non_empty_input()`

제목, 내용, 검색어처럼 비어 있으면 안 되는 값은 이 함수로 받습니다. `strip()`은 입력의 앞뒤 공백을 제거합니다. 예를 들어 공백만 여러 번 입력하면 빈 값으로 판단하여 다시 입력받습니다.

> 이 함수는 **입력이 끝난 뒤 Enter를 눌렀을 때의 값**을 검사합니다. 글자를 입력하는 중간에 Backspace로 지우는 동작은 Python 코드가 아니라 VSCode가 프로그램을 실행한 창의 키보드 처리 방식에 좌우됩니다. 따라서 반드시 통합 터미널에서 실행해야 자연스러운 편집·삭제가 가능합니다.

### 7-3. 번호 검증 함수

`is_valid_prompt_number()`는 문자열이 숫자인지, 그리고 현재 목록 범위 안인지 검사합니다. `get_prompt_index()`는 이 검사를 반복하여 통과한 번호를 리스트에서 사용할 수 있는 0부터 시작하는 위치로 바꿉니다.

```text
화면 번호: 1, 2, 3
리스트 위치: 0, 1, 2
```

## 8. 데이터 처리 함수

### 8-1. 프롬프트 추가

`add_prompt()`는 제목, 내용, 카테고리를 받은 뒤 새 딕셔너리를 만들어 `prompts.append()`로 목록 끝에 추가합니다. 새 항목의 `favorite`는 기본적으로 `False`입니다.

### 8-2. 중복 등록 방지

`normalize_prompt_text()`는 제목이나 내용의 앞뒤 공백, 연속 공백, 영어 대소문자 차이를 정리합니다. `find_duplicate_prompt()`는 정리된 제목과 내용이 모두 같은 기존 항목이 있는지 찾아봅니다. `add_prompt()`는 중복이 발견되면 카테고리 입력 단계로 넘어가지 않고 안내 문구를 출력한 뒤 메뉴로 돌아갑니다.

| 비교 결과 | 프로그램 동작 |
| --- | --- |
| 제목·내용이 모두 같음 | “동일한 프롬프트가 이미 존재합니다”를 출력하고 추가하지 않음 |
| 제목 또는 내용 중 하나가 다름 | 다른 프롬프트로 보고 등록 절차를 계속 진행 |
| 공백 수·영어 대소문자만 다름 | 같은 프롬프트로 보고 중복 등록 차단 |

이 기능은 정확히 같은 프롬프트가 여러 번 쌓이는 문제를 막으면서, 같은 제목의 다른 버전은 저장할 수 있게 해 줍니다.

### 8-3. 카테고리별 조회

카테고리별 조회는 세 함수가 협력합니다.

| 함수 | 역할 |
| --- | --- |
| `get_view_categories()` | 기본 카테고리와 직접 입력한 사용자 정의 카테고리를 하나의 목록으로 만듭니다. |
| `select_category_to_view()` | 사용자가 조회할 카테고리 번호를 고르게 합니다. |
| `filter_prompts_by_category()` | 선택한 카테고리와 일치하는 항목만 새 리스트로 반환합니다. |

`filter_prompts_by_category()`는 원래 목록을 바꾸지 않습니다. 조회 결과만 새로 만들어 주므로, 필터링 후에도 전체 목록을 다시 보면 모든 프롬프트가 그대로 남아 있습니다.

### 8-4. 검색

`find_prompts()`는 제목과 내용에 검색어가 들어 있는지 확인합니다. `casefold()`를 사용해 영어 대소문자 차이를 줄입니다. 검색 결과가 없으면 빈 리스트를 반환하고, 목록 출력 함수가 “저장된 프롬프트가 없습니다.”라고 안내합니다.

### 8-5. 즐겨찾기

`toggle_favorite()`는 선택한 항목의 `favorite` 값을 반대로 바꿉니다.

```python
prompt["favorite"] = not prompt["favorite"]
```

현재 값이 `False`라면 `True`가 되고, 다시 선택하면 `False`가 됩니다. `get_favorite_prompts()`는 `favorite`가 참인 항목만 골라 목록으로 반환합니다.

## 9. 화면 출력 함수

출력 로직도 역할별로 나누었습니다.

| 함수 | 화면에 보여 주는 내용 |
| --- | --- |
| `show_menu()` | 메뉴 1~8 |
| `format_prompt_summary()` | 프롬프트 한 건의 번호·제목·카테고리·별 표시를 담은 한 줄 |
| `show_prompt_list()` | 여러 프롬프트의 목록 또는 빈 목록 안내 |
| `show_prompt_detail()` | 선택한 한 프롬프트의 전체 내용 |
| `show_favorites()` | 즐겨찾기된 프롬프트 목록 |

`format_prompt_summary()`를 따로 둔 이유는 목록을 표시하는 규칙을 한 곳에서 관리하기 위해서입니다. 나중에 목록에 생성일이나 태그를 추가하고 싶다면 이 함수만 수정하면 됩니다.

## 10. 메뉴 반복: `run_menu_loop()`

`run_menu_loop()`은 프로그램의 중심입니다. `while True`로 메뉴를 계속 보여 주고, 사용자가 입력한 번호에 따라 알맞은 함수를 호출합니다.

```python
while True:
    show_menu()
    choice = get_menu_choice()

    if choice == "1":
        add_prompt(prompts)
    elif choice == "2":
        show_prompt_list(prompts)
    # 중간 생략
    elif choice == "8":
        return
```

기능 함수가 끝나면 반복문의 처음으로 돌아가 메뉴가 다시 표시됩니다. `8`을 누르면 `return`으로 반복을 끝내고 `main()`으로 돌아갑니다.

## 11. 최종 시작점: `main()`과 `if __name__ == "__main__"`

파일 마지막의 아래 코드는 이 파일을 직접 실행했을 때만 프로그램을 시작하게 합니다.

```python
if __name__ == "__main__":
    main()
```

테스트 파일이 `prompt_manager.py`를 import할 때는 메뉴가 자동으로 실행되면 안 됩니다. 이 조건문이 있기 때문에 테스트에서는 필요한 함수만 불러와 검증할 수 있습니다.

`main()`은 다음 세 가지를 담당합니다.

1. 입력 가능한 통합 터미널인지 확인합니다.
2. 기본 프롬프트 목록을 새로 만들고 메뉴 반복을 시작합니다.
3. Ctrl+C나 입력 종료가 발생하면 친절한 종료 문구를 보여 줍니다.

## 12. 테스트 파일과의 연결

`tests/test_prompt_manager.py`는 프로그램을 실제로 사람 대신 실행해 보며 핵심 기능을 확인합니다. 특히 이번 수정에서는 메뉴 2와 메뉴 3의 출력, 즐겨찾기·카테고리 필터, 비대화형 실행 안내, EOF 입력 중단 처리를 테스트에 추가했습니다.

```bash
python3 -m unittest discover -s tests -v
```

테스트 결과가 모두 `ok`이고 마지막 줄에 `OK`가 보이면, 코드의 주요 함수와 메뉴 흐름이 예상대로 동작한다는 뜻입니다. 다만 실제 VSCode 키보드 입력 경험은 반드시 통합 터미널에서도 한 번 확인해야 합니다.
