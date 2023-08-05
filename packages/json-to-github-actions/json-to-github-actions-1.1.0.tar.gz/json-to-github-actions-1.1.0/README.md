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

```json
{
  "repo_url": "https://github.com/user_name/json_to_github_actions.git",
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
  "copy_dirs_outputs": []
}

'''

yaml_data = json_to_github_actions(json_data)
```

這將把 JSON 格式的數據轉換為適用於 GitHub Actions 的 YAML 格式。之後，您可以選擇將 `yaml_data` 保存到檔案中。
