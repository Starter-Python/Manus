# VSCode 사용 안내 | GitHub에서 내려받아 A1-1 과제 실행하기

이 문서는 처음 사용하는 사람을 기준으로 **GitHub의 `Manus` 저장소를 VSCode에 내려받고**, `AI 활용 학습 A1-1` 폴더의 프로그램을 실행·테스트·수정한 뒤 다시 GitHub에 올리는 과정을 설명합니다. 작업할 저장소 주소는 다음과 같습니다.

> 저장소 주소: [https://github.com/Starter-Python/Manus](https://github.com/Starter-Python/Manus)

## 1. 처음 한 번만 준비할 것

먼저 PC에 VSCode, Python, Git을 설치합니다. VSCode를 실행한 뒤 왼쪽의 **Extensions** 탭에서 `Python`을 검색하고, 게시자가 Microsoft인 Python 확장을 설치합니다. 필요하다면 `Korean Language Pack`도 설치할 수 있습니다.

| 준비 항목 | 확인 방법 | 목표 |
| --- | --- | --- |
| VSCode | VSCode 앱 실행 | 편집기 실행 가능 |
| Python | 터미널에서 `python --version` 또는 `python3 --version` | Python 3.10 이상 |
| Git | 터미널에서 `git --version` | Git 버전이 출력됨 |
| Python 확장 | VSCode Extensions에서 `Python` 검색 | Microsoft Python 확장 설치 |
| GitHub 로그인 | VSCode 좌측 하단 계정 아이콘 | 사용 중인 GitHub 계정으로 로그인 |

Windows에서는 대체로 `python` 명령을 사용하고, macOS·Linux에서는 `python3` 명령을 사용합니다. 아래 명령에서 자신의 PC에 맞는 명령을 선택하면 됩니다.

## 2. GitHub 저장소를 VSCode로 내려받기

가장 쉬운 방법은 VSCode의 명령 팔레트를 사용하는 것입니다. VSCode에서 `Ctrl + Shift + P`를 누르고 `Git: Clone`을 선택합니다. 주소 입력란에 아래 주소를 붙여넣고, PC에서 저장소를 저장할 폴더를 선택합니다.

```text
https://github.com/Starter-Python/Manus.git
```

복제가 끝난 뒤 **Open** 또는 **Open Cloned Repository**를 선택합니다. 신뢰 여부를 묻는 창이 나오면 본인이 내려받은 저장소임을 확인한 뒤 신뢰합니다. VSCode 왼쪽 탐색기에서 `AI 활용 학습 A1-1` 폴더를 열면 과제 파일을 볼 수 있습니다.

터미널을 사용하는 방법도 있습니다. VSCode에서 `Terminal > New Terminal`을 연 뒤, 원하는 작업 위치에서 아래 명령을 실행합니다. 복제가 끝나면 `File > Open Folder...` 메뉴로 `Manus` 폴더를 엽니다.

```bash
git clone https://github.com/Starter-Python/Manus.git
cd Manus
```

## 3. A1-1 프로그램 실행하기

VSCode에서 상단 메뉴 **Terminal > New Terminal**을 선택합니다. 터미널이 저장소 최상위 폴더(`Manus`)에서 열렸다면 아래처럼 A1-1 폴더로 이동합니다. 폴더 이름에 공백과 한글이 있으므로 따옴표를 포함하는 것이 안전합니다.

```bash
cd "AI 활용 학습 A1-1"
```

그다음 Python 버전을 확인하고 프로그램을 실행합니다.

| 운영체제 환경 | 버전 확인 | 프로그램 실행 |
| --- | --- | --- |
| Windows에서 `python` 사용 | `python --version` | `python prompt_manager.py` |
| macOS·Linux에서 `python3` 사용 | `python3 --version` | `python3 prompt_manager.py` |

처음 실행하면 기본 예시 프롬프트 3개와 숫자 메뉴가 표시됩니다. 숫자를 입력하고 Enter를 누르면 기능을 선택할 수 있습니다.

```text
1. 프롬프트 추가
2. 전체 프롬프트 목록 보기
3. 카테고리별 조회
4. 프롬프트 검색
5. 프롬프트 상세 보기
6. 즐겨찾기 추가/해제
7. 즐겨찾기 목록 보기
8. 종료
```

## 4. 프로그램을 한 번 직접 사용해 보기

아래 순서대로 입력하면 기본 기능을 빠르게 확인할 수 있습니다. 입력 예시는 실제 프롬프트 내용으로 바꾸어도 됩니다.

| 순서 | 입력 | 확인할 내용 |
| --- | --- | --- |
| 1 | `2` | 기본 프롬프트 3개와 즐겨찾기 별 표시가 나오는지 확인 |
| 2 | `1` | 새 프롬프트 추가 메뉴 진입 |
| 3 | 제목: `회의록 요약` | 제목 입력 확인 |
| 4 | 내용: `다음 회의록을 세 문장으로 요약하세요.` | 내용 입력 확인 |
| 5 | 카테고리 번호: `5` | 자동화 카테고리 선택 확인 |
| 6 | `4` → 검색어: `회의` | 제목 또는 내용에서 검색되는지 확인 |
| 7 | `5` → 프롬프트 번호 입력 | 상세 내용이 나오는지 확인 |
| 8 | `6` → 프롬프트 번호 입력 | 즐겨찾기 추가 또는 해제 확인 |
| 9 | `7` | 즐겨찾기 항목만 출력되는지 확인 |
| 10 | `8` | 프로그램 종료 |

프로그램에서 새로 추가하거나 즐겨찾기한 데이터는 **현재 실행 중에만 유지**됩니다. 종료 후 다시 실행하면 기본 예시 데이터로 초기화되는 것이 과제의 정상 동작입니다.

## 5. 자동 테스트 실행하기

프로그램의 핵심 데이터 처리 로직은 자동 테스트로 확인할 수 있습니다. A1-1 폴더에서 다음 명령을 실행합니다.

```bash
# Windows
python -m unittest discover -s tests -v

# macOS·Linux
python3 -m unittest discover -s tests -v
```

모든 항목이 `ok`로 표시되고 마지막에 `OK`가 나오면 테스트를 통과한 것입니다. 코드 문법만 빠르게 확인하려면 아래 명령을 사용합니다.

```bash
# Windows
python -m py_compile prompt_manager.py

# macOS·Linux
python3 -m py_compile prompt_manager.py
```

## 6. 코드를 수정한 뒤 GitHub에 다시 올리기

수정 전에는 먼저 최신 변경사항을 받아 충돌 가능성을 줄입니다. VSCode 터미널에서 저장소 최상위 폴더로 이동한 뒤 아래 명령을 실행합니다.

```bash
cd ..
git pull origin main
git status
```

그다음 `AI 활용 학습 A1-1/prompt_manager.py` 또는 문서를 수정하고 저장합니다. 변경한 내용을 확인한 뒤, 의미가 드러나는 메시지로 커밋하고 GitHub에 올립니다.

```bash
git status
git add "AI 활용 학습 A1-1"
git commit -m "feat(A1-1): 설명이 드러나는 변경 내용"
git push origin main
```

`git status` 결과에 `working tree clean`이 나오고 `git push`가 성공하면 GitHub에 반영된 것입니다. 웹 브라우저에서 [Manus 저장소](https://github.com/Starter-Python/Manus)를 새로고침해 변경 파일을 확인합니다.

VSCode 화면으로만 처리할 수도 있습니다. 왼쪽의 **Source Control** 아이콘을 열고 변경 파일을 확인한 뒤, `+` 버튼으로 스테이지에 올립니다. 위의 메시지 입력란에 커밋 메시지를 작성하고 **Commit**을 선택합니다. 마지막으로 **Sync Changes** 또는 **Push**를 선택하면 됩니다. 단, 처음에는 터미널 명령을 함께 사용하면 현재 상태를 더 쉽게 이해할 수 있습니다.

> 작업을 시작하기 전에는 항상 `git pull origin main`으로 최신 코드를 받고, 작업이 끝난 뒤에는 `git status`로 내가 바꾼 파일을 확인하는 습관을 들이세요. 다른 사람이 같은 파일을 수정했다면 충돌이 생길 수 있으므로, 충돌 메시지가 보이면 임의로 덮어쓰지 말고 내용을 비교한 뒤 해결해야 합니다.

## 7. 과제 제출용 화면 캡처 순서

과제 제출을 위한 캡처는 아래 순서대로 하면 빠뜨릴 항목이 줄어듭니다.

| 캡처 | VSCode 또는 터미널에서 할 일 |
| --- | --- |
| 개발 환경 | VSCode 화면, `python --version` 또는 `python3 --version`, `git --version` 결과를 함께 캡처 |
| Hello 실행 | `hello.py`에 `print("Hello")`를 작성하고 실행 결과를 캡처 |
| 프로그램 메뉴 | `prompt_manager.py` 실행 직후 메뉴를 캡처 |
| 프롬프트 추가 | 메뉴 `1`로 제목·내용·카테고리를 입력하는 장면을 캡처 |
| 목록과 검색 | 메뉴 `2`, 메뉴 `4`의 결과를 각각 캡처 |
| Git 이력 | 저장소 최상위 폴더에서 `git log --oneline --graph`를 실행해 브랜치와 merge 커밋이 보이도록 캡처 |

## 8. 자주 생기는 문제

| 상황 | 원인과 해결 방법 |
| --- | --- |
| `python` 또는 `python3`를 찾을 수 없음 | Python이 설치되지 않았거나 PATH 설정이 되지 않은 경우입니다. Python을 설치한 뒤 VSCode를 다시 시작합니다. |
| VSCode에서 실행 버튼이 보이지 않음 | Python 확장을 설치하고, `Ctrl + Shift + P`에서 `Python: Select Interpreter`를 선택해 Python 3.10 이상 인터프리터를 지정합니다. |
| `ModuleNotFoundError`가 발생함 | 터미널이 `AI 활용 학습 A1-1` 폴더에 있는지 확인한 뒤 다시 실행합니다. |
| `git push`에서 인증 오류가 발생함 | VSCode 계정 메뉴에서 GitHub 로그인을 확인하거나, 터미널 안내에 따라 GitHub 인증을 완료합니다. |
| `git pull`에서 충돌이 발생함 | 충돌 표시가 난 파일을 열어 두 버전의 내용을 비교하고, 필요한 내용을 남긴 뒤 저장·커밋합니다. 확신이 없으면 변경을 먼저 백업하고 도움을 요청합니다. |

이제 `README.md`에서 프로그램 기능을 확인하고, `과제_수행_설명서.md`에서 코드 원리를 읽고, `요구사항_점검표.md`에서 제출 전 체크할 항목을 확인하면 됩니다.
