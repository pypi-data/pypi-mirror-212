# JSON 轉 GitHub Actions YAML
```
🐔動機: 全球免費20 VMs運算，有感試用，可以把 python 或 julia 放到 github actions 算 
💣地雷: 格式轉換會存在很多 bugs, 要先生最終無 bugs .yml 才反推轉換的 .py 此套件程式碼
🧪實驗: Roy julia套件清物聯網資料已經分散兩台 VMs (每個4GB .zip處理55分鐘)運算成功
🧾待辦: 雖然可分散運算了，但運算結果還需要轉化為 github release .zip 抓回來結果
這個 Python 套件能將 JSON 格式轉化為 GitHub Actions 的 YAML 格式。
```

## 安裝
python3 -m pip install json-to-github-actions

## CLI 用法
```
python json_to_github_actions.py --json_file [json_file] --yaml_file [yaml_file]
```

範例：
```bash
python json_to_github_actions.py --json_file input.json --yaml_file output.yaml
```
輸入 `json_file` 是您的 JSON 檔案路徑，並將產生的 GitHub Actions YAML 檔案保存到給定的 `yaml_file` 路徑。
## 套件 import 用法
首先，將 `json_to_github_actions.py` 腳本導入您的專案。

```python
from json_to_github_actions import json_to_github_actions
```
然後您可以調用 `json_to_github_actions()` 函數將 JSON 輸入轉換為 YAML 格式。

## JSON 格式
JSON 檔案必須包含以下結構：
```
{
  "repo_url": "https://github.com/bohachu/json_to_github_actions.git",
  "script_name": "add_two_numbers.py",
  "script_dir": "/add_two_numbers/",
  "execution_environment": [
    {
      "language": "python",
      "version": "3.8",
      "installation_command": "python -m pip install -r requirements.txt"
    }
  ],
  "max_parallel": 3,
  "json_parameters": [
    {
      "a": 1,
      "b": 2
    },
    {
      "a": 3,
      "b": 4
    },
    {
      "a": 5,
      "b": 6
    },
    {
      "a": 7,
      "b": 8
    }
  ],
  "output_directory": "add_two_numbers/data/"
}
```

JSON 結構包含以下字段：
- `repo_url`：執行腳本的倉庫的 URL。
- `script_name`：要執行的腳本的名稱。
- `script_dir`：腳本文件夾的相對路徑。
- `execution_environment`：包含要在其中運行測試的環境設置的陣列。 您可以為 Python 和 Julia 語言指定多個環境。
- `max_parallel`：最大並行運行的數量。
- `json_parameters`：參數和值的陣列，這些參數和值將傳遞給腳本。
- `output_directory`：腳本將結果輸出到的文件夾的名稱。

## 注意事項
- 當前支持Python和Julia語言。 若要添加對其他語言的支持，可以編輯 `json_to_github_actions.py` 文件並添加相應的執行命令。
- 模板目前僅適用於 "on": "workflow_dispatch"。 若要基於不同事件觸發 GitHub Actions，請在生成 YAML 檔案後手動更新該字段。
- 如果在運行腳本時遇到問題或錯誤，請檢查您的 JSON 文件的語法和結構是否正確。 

## 敬告
您自己承擔使用自動生成的 GitHub Actions YAML 文件的風險，我們對任何由此導致的後果和損失概不負責。 您應充分測試 YAML 文件以確保其符合預期行為，並完成所需任務。