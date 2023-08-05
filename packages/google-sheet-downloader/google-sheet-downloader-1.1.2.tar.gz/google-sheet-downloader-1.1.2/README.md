# 積木塊：Google Sheets 下載器 by Bowen Chiu
這是一個能夠下載 Google Sheets 試算表的小工具。使用者可以輸入 Google 服務帳戶金鑰、試算表 ID、輸出資料夾路徑等資訊，程式會利用 Google Sheets API 下載資料並存成 CSV 檔案。

## 使用說明
特色:
- 支援快取功能，曾經下載過的 google sheet document id 就不會再下載，飛快
- 支援多個檔案下載
- 支援一個 spreadsheet 當中所有的 worksheet 下載轉換為多個 .csv 檔案
- 可 CLI 運用 command line 操作
- 可 pip install package 當成套件呼叫而無須透過 CLI 也能用

安裝:
```
python3 -m pip install google-sheet-downloader
```

使用:
```
python3 -m google_sheet_downloader [-h] 
   --key-file KEY_FILE 
   --sheet-ids SHEET_IDS 
   --output-folder OUTPUT_FOLDER 
   [--force]                               
```

## 詳細說明

1. 申請 Google 服務帳戶金鑰
    1. 進入 [Google Cloud Console](https://console.cloud.google.com/)
    2. 建立一個專案或使用現有的專案
    3. 選擇左上角的導覽功能表 > API 和服務 > 憑證
    4. 在「憑證」頁面中點擊「建立憑證」，然後選擇「服務帳戶」
    5. 填寫相關資訊，完成後下載 JSON 金鑰檔案
2. 安裝 Python 3.x
3. 安裝相依套件
   ```sh
   pip install -r requirements.txt
   ```
4. 執行程式
   ```sh
   python google-sheet-downloader.py --key-file <金鑰檔案路徑> --sheet-ids <試算表 ID> --output-folder <輸出資料夾路徑>
   ```
   可以同時下載多個試算表，試算表 ID 以逗號分隔。
   可以使用 `--force` 強制重新下載資料，忽略快取的檢查。

## 參數說明

- `--key-file`：必填參數，Google 服務帳戶金鑰的 JSON 檔案路徑
- `--sheet-ids`：必填參數，要下載的試算表 ID，以逗號分隔
- `--output-folder`：必填參數，下載完成後要存放 CSV 檔案的資料夾路徑
- `--force`：選填參數，是否強制重新下載，忽略快取檢查，預設為 `False`

## 注意事項

- 程式下載的 CSV 檔案以試算表 ID、試算表名稱、工作表名稱作為檔案名稱。
- 如果輸出資料夾已經有相同檔名的 CSV 檔案，程式不會覆蓋原本的檔案，也不會下載該工作表的資料。
- 下載的 CSV 檔案編碼為 UTF-8，換行符號為 CRLF。

# 自然語言原始設計

### 001 用途描述：

本專案提供一個命令列工具，用於下載多個 Google 試算表並將其儲存在指定資料夾中。它具有類似緩存功能，如果已經下載過某個試算表，則會跳過該試算表，避免重複下載。

### 002 程式碼檔名：

`google_sheet_downloader.py`

### 003 可單元測試的功能描述：

T01 一次可下載多個 Google 試算表並儲存為 CSV 檔案到指定路徑
T02 檢查已下載的試算表，避免重複下載，已經下載過的相當於有快取
T03 執行參數可以強迫重新下載試算表，忽略快取
T04 要單獨一個處理 argparse 的 function（只有呼叫 cli會用到）, 要單獨獨立一個接收 argparse 參數的 function（為了做成套件給別人呼叫用，別人用套件時不會用到 cli）

### 004 輸入目錄結構設計：

```
./users/bohachu_gmail_com/github/bohachu/google_sheet_downloader/google_sheet_downloader.py
./users/bohachu_gmail_com/github/bohachu/google_sheet_downloader/keys/google_service_account_key.json
```

### 005 輸入檔案格式設計：

- `google_service_account_key.json`: Google 服務帳戶的密鑰 JSON 檔案

### 006 輸出目錄結構設計：

```
./users/bohachu_gmail_com/github/bohachu/google_sheet_downloader/data/sheets_output/spreadsheet_試算表名字_worksheet_頁籤名字_doc-id_14GQkXftKXoaIJ_TKxtXzae1J7p10XznGgF_lg7cDG8g.csv
```

### 007 輸出檔案格式設計：

- 輸出檔案為 CSV 格式，一個 CSV 代表一個 worksheet 頁籤資料。

### 008 命令列用法：

```
python3 -m google_sheet_downloader --key-file <service_account_key.json> --sheet-ids <sheet_id1,sheet_id2> --output-folder <sheets_output>
```

### 009 命令列範例：

```
python3 -m google_sheet_downloader --key-file google_service_account_key.json --sheet-ids 1a2B3c4D5e6F,1x2y3z4A5B --output-folder sheets_output
```

CLI 參數設計：

- `--key-file`: Google 服務帳戶的密鑰 JSON 檔案路徑
- `--sheet-ids`: 要下載的多個 Google 試算表的 ID，以逗號分隔
- `--output-folder`: 輸出 CSV 檔案的資料夾路徑
