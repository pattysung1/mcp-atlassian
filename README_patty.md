# Confluence 驗證腳本使用指南

本文件說明如何設定環境並執行 `verify_confluence.py` 腳本，以測試與 Confluence 的連線並查詢指定空間 (Space) 中的頁面。

---

### 首次設定 (僅需執行一次)

如果您是第一次使用，請依照以下步驟完成環境設定。這是一個一次性的過程。

#### 步驟 1: 安裝 Python 相依套件管理工具 `uv`

本專案使用 `uv` 來管理虛擬環境與 Python 套件。您需要先安裝它。

```bash
# 使用 pip 安裝 uv (可能需要繞過系統環境保護)
pip install uv --break-system-packages
```

#### 步驟 2: 建立虛擬環境

虛擬環境能將此專案的套件與您的系統環境隔離開，避免衝突。

```bash
# 在專案根目錄執行此指令，建立名為 .venv 的虛擬環境
python -m uv venv
```

#### 步驟 3: 安裝專案所有相依套件

接下來，我們需要在虛擬環境中安裝所有必要的套件。

```bash
# 啟用虛擬環境
source .venv/bin/activate

# 使用 uv 安裝 pyproject.toml 中定義的所有套件
uv pip install -e .[dev]
```

#### 步驟 4: 設定 `.env` 檔案

腳本需要從 `.env` 檔案讀取您的 Confluence 網址和認證權杖。

1.  將專案中的 `.env.example` 檔案複製一份，並重新命名為 `.env`。
2.  用文字編輯器打開 `.env` 檔案，填寫您的 `CONFLUENCE_URL` 和 `CONFLUENCE_PERSONAL_TOKEN`。

    ```
    CONFLUENCE_URL=https://your-company.atlassian.net
    CONFLUENCE_PERSONAL_TOKEN=your_api_token
    ```

---

### 如何執行測試腳本 (日常使用)

完成首次設定後，未來您每次想執行腳本時，只需要依照以下簡單步驟。

#### 步驟 1: 啟用虛擬環境

**每次**新開一個終端機 (Terminal) 時，都必須先啟用虛擬環境。

```bash
source .venv/bin/activate
```

啟用成功後，您會看到指令提示符號前出現 `(.venv)` 的字樣。

#### 步驟 2: (可選) 修改您想測試的 Space

用文字編輯器打開 `verify_confluence.py` 檔案，找到 `TARGET_SPACE_KEY` 這個變數，將其值修改為您想查詢的 Space Key。

```python
# ...
# 設定您想測試的 Confluence Space Key
TARGET_SPACE_KEY = "您想測試的SpaceKey"
# ...
```

#### 步驟 3: 執行腳本

在已啟用虛擬環境的狀態下，執行以下指令：

```bash
PYTHONPATH=src python verify_confluence.py
```

`PYTHONPATH=src` 的作用是告訴 Python 在執行時，要將 `src` 目錄也納入模組的搜尋路徑，這樣腳本才能成功匯入專案的原始碼。
