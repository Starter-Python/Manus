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

처음 실행하면 6개 카테고리를 포함한 기본 예시 프롬프트 **10개**와 숫자 메뉴가 표시됩니다. 숫자를 입력하고 Enter를 누르면 기능을 선택할 수 있습니다.

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
| 1 | `2` | 기본 프롬프트 10개와 즐겨찾기 별 표시가 나오는지 확인 |
| 2 | `1` | 새 프롬프트 추가 메뉴 진입 |
| 3 | 제목: `회의록 요약` | 제목 입력 확인 |
| 4 | 내용: `다음 회의록을 세 문장으로 요약하세요.` | 내용 입력 확인 |
| 5 | 카테고리 번호: `5` | 자동화 카테고리 선택 확인. 제목과 내용이 기존 항목과 모두 같으면 중복 등록 안내가 표시됨 |
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

## 7. Git 충돌(Conflict) 해결하기

Git 충돌은 **내 PC의 변경 내용과 GitHub에서 새로 받아오는 변경 내용이 같은 위치를 서로 다르게 수정했을 때** 발생합니다. 충돌은 오류가 아니라 어떤 내용을 남길지 사람이 결정해야 한다는 신호입니다. 해결 전에는 반드시 `git status`로 현재 상황을 확인하고, 이해되지 않는 파일은 임의로 덮어쓰지 않는 것이 중요합니다.

### 7-1. 충돌을 예방하는 가장 안전한 작업 순서

작업을 시작하기 전에는 최신 변경 사항을 먼저 받고, 작업이 끝난 뒤에는 작고 의미 있는 단위로 커밋합니다. 수정한 파일이 있을 때 바로 `git pull`을 하기보다 먼저 상태를 확인하고 커밋하거나 임시 보관합니다.

```bash
# 1. 저장소 최상위 폴더에서 현재 상태 확인
cd ..
git status

# 2-A. 수정한 내용을 남길 경우: 스테이지·커밋 후 최신 내용 받기
git add "AI 활용 학습 A1-1"
git commit -m "docs(A1-1): 작업 내용 설명"
git pull origin main

# 2-B. 아직 커밋하고 싶지 않은 경우: 임시 보관 후 최신 내용 받기
git stash push -m "작업 중인 A1-1 변경"
git pull origin main
git stash pop
```

`git stash pop` 뒤에도 충돌이 생길 수 있습니다. 이 경우에도 아래의 같은 해결 절차를 따르면 됩니다. 임시 보관 목록은 `git stash list`로 확인할 수 있습니다.

### 7-2. VSCode에서 충돌을 해결하는 순서

`git pull` 또는 **Source Control > Pull** 이후 충돌이 생기면 VSCode 왼쪽의 **Source Control** 아이콘에 `MERGE CHANGES` 또는 충돌 파일 목록이 나타납니다. 해당 파일을 클릭하면 VSCode의 Conflict Editor가 열립니다.

| 단계 | VSCode에서 할 일 | 확인할 내용 |
| --- | --- | --- |
| 1 | Source Control에서 충돌 파일을 엽니다. | 어떤 파일이 충돌했는지 확인합니다. |
| 2 | 충돌 구간마다 **Accept Current Change**, **Accept Incoming Change**, **Accept Both Changes** 중 하나를 고릅니다. | Current는 내 PC의 현재 브랜치 내용, Incoming은 GitHub에서 받아오는 내용입니다. |
| 3 | 두 내용을 함께 남겼다면 직접 편집해 최종 문장·코드가 자연스러운지 확인합니다. | 중복, 누락, 들여쓰기 오류를 제거합니다. |
| 4 | 저장한 뒤 Source Control에서 `+`로 해결된 파일을 스테이지합니다. | 파일이 `Staged Changes`에 나타나는지 확인합니다. |
| 5 | 커밋 메시지를 작성해 **Commit**합니다. | 병합 해결을 하나의 커밋으로 기록합니다. |
| 6 | **Sync Changes** 또는 **Push**를 선택합니다. | 해결된 결과가 GitHub에 반영됩니다. |

Conflict Editor가 보이지 않는 경우에는 파일 안에서 **충돌 시작 표식, 구분 표식, 충돌 끝 표식**을 직접 찾을 수 있습니다. 실제 표식은 각각 `작은부등호(<) 7개 + HEAD`, `등호(=) 7개`, `큰부등호(>) 7개 + origin/main`의 형태입니다. 세 표식과 필요 없는 내용을 모두 지운 뒤, 남길 최종 내용만 저장해야 합니다.

```text
[충돌 시작 표식] HEAD
내 PC에서 수정한 내용
[구분 표식]
GitHub에서 받아온 내용
[충돌 끝 표식] origin/main
```

충돌을 모두 해결한 뒤 터미널에서 아래 명령을 실행합니다. `Unmerged paths`가 남아 있지 않고 `working tree clean`이 보이면 정상적으로 정리된 것입니다.

```bash
git status
git add "AI 활용 학습 A1-1"
git commit -m "merge: resolve A1-1 conflict"
git push origin main
```

### 7-3. Push가 거부되었을 때

`git push`에서 다른 사람이 먼저 변경을 올렸다는 이유로 거부되면, 내 커밋은 유지된 상태입니다. 당황하지 말고 최신 내용을 받은 뒤 충돌이 있으면 앞 절차에 따라 해결합니다.

```bash
git pull origin main
# 충돌이 없다면 바로 다음 명령을 실행
git push origin main
```

### 7-4. 병합을 중단하고 이전 상태로 돌아가기

아직 해결 방향을 결정하지 못했다면 병합을 중단할 수 있습니다. 다만 **병합 과정에서 직접 수정한 내용은 사라질 수 있으므로**, 필요한 내용은 복사해 별도 메모에 백업한 뒤 실행합니다.

```bash
git merge --abort
```

`git pull`을 rebase 방식으로 수행했고 rebase 충돌 메시지가 나온 경우에는 아래 명령을 사용합니다.

```bash
git rebase --abort
```

`git reset --hard`는 아직 커밋하지 않은 작업을 되돌릴 수 있으므로, 충돌 해결 방법으로 사용하지 않습니다. 해결이 어렵다면 `git status` 출력과 충돌 파일의 내용을 먼저 보관한 뒤 도움을 요청하는 것이 안전합니다.

## 8. 과제 제출용 화면 캡처 순서

과제 제출을 위한 캡처는 아래 순서대로 하면 빠뜨릴 항목이 줄어듭니다.

| 캡처 | VSCode 또는 터미널에서 할 일 |
| --- | --- |
| 개발 환경 | VSCode 화면, `python --version` 또는 `python3 --version`, `git --version` 결과를 함께 캡처 |
| Hello 실행 | `hello.py`에 `print("Hello")`를 작성하고 실행 결과를 캡처 |
| 프로그램 메뉴 | `prompt_manager.py` 실행 직후 메뉴를 캡처 |
| 프롬프트 추가 | 메뉴 `1`로 제목·내용·카테고리를 입력하는 장면을 캡처 |
| 목록과 검색 | 메뉴 `2`, 메뉴 `4`의 결과를 각각 캡처 |
| Git 이력 | 저장소 최상위 폴더에서 `git log --oneline --graph`를 실행해 브랜치와 merge 커밋이 보이도록 캡처 |

## 9. 자주 생기는 문제

| 상황 | 원인과 해결 방법 |
| --- | --- |
| `python` 또는 `python3`를 찾을 수 없음 | Python이 설치되지 않았거나 PATH 설정이 되지 않은 경우입니다. Python을 설치한 뒤 VSCode를 다시 시작합니다. |
| VSCode에서 실행 버튼이 보이지 않음 | Python 확장을 설치하고, `Ctrl + Shift + P`에서 `Python: Select Interpreter`를 선택해 Python 3.10 이상 인터프리터를 지정합니다. |
| `ModuleNotFoundError`가 발생함 | 터미널이 `AI 활용 학습 A1-1` 폴더에 있는지 확인한 뒤 다시 실행합니다. |
| `git push`에서 인증 오류가 발생함 | VSCode 계정 메뉴에서 GitHub 로그인을 확인하거나, 터미널 안내에 따라 GitHub 인증을 완료합니다. |
| `git pull`에서 충돌이 발생함 | 충돌 표시가 난 파일을 열어 두 버전의 내용을 비교하고, 필요한 내용을 남긴 뒤 저장·커밋합니다. 확신이 없으면 변경을 먼저 백업하고 도움을 요청합니다. |

이제 `README.md`에서 프로그램 기능을 확인하고, `과제_수행_설명서.md`에서 코드 원리를 읽고, `요구사항_점검표.md`에서 제출 전 체크할 항목을 확인하면 됩니다.
