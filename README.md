# 📂 파일 무결성 검사기 (File Integrity Checker)

[파일 무결성 검증 스캐너]

지정한 디렉터리의 모든 파일 상태를 스캔하여 Hash(SHA-256) 기반의 베이스(.base_hash)를 생성합니다. 이후 파일의 상태를 '동일, 생성, 변경, 삭제, 이동/이름 변경, 거부'로 구분하여 감지합니다.

🖥️ CLI와 GUI를 모두 지원합니다.

## ✨ 주요 기능

- **최초 스캔** : 'SHA-256' Hash를 사용하여 파일의 고유한 베이스(.base_hash) 생성
- **무결성 검사** : 베이스를 기준으로 현재 파일 상태와 비교
  - `동일` : 변경이 없는 파일
  - `생성` : 새로 추가된 파일
  - `변경` : 내용이 수정된 파일
  - `삭제` : 삭제된 파일
  - `이동/이름 변경` : 경로나 이름이 바뀐 파일
  - `거부` : 접근 불가 파일 (검사 불가)

## 🛠️ 사용 기술

- **Python 3**
- **hashlib** : SHA-256 기반 Hash 계산
- **os** : 디렉터리 순회
- **sys** : 명령행 인자
- **Tkinter** : GUI 구현

## ⚙️ 설치 및 준비

### 이 프로젝트는 Python 표준 라이브러리만 사용하므로 별도의 라이브러리를 설치할 필요가 없습니다.

1.  이 저장소를 클론(Clone)합니다.
    ```bash
    git clone [https://github.com/](https://github.com/)[Your-Username]/[Your-Repository-Name].git
    ```
2.  프로젝트 디렉터리로 이동합니다.

    ```bash
    cd [Your-Repository-Name]
    ```

3.  CLI(`main.py`)와 GUI(`gui_main.py`) 중 실행 방식을 선택합니다.

## 🚀 실행

### CLI

터미널에서 아래 명령어를 입력합니다. (scan : 최초 스캔, check : 무결성 검사) ("PATH" : 절대 경로/상대 경로를 문자열로 입력)

```bash
python main.py scan/check "PATH"
```

---

### GUI

아래 명령어를 입력하여 `gui_main.py` 를 실행합니다.

```bash
python gui_main.py
```
