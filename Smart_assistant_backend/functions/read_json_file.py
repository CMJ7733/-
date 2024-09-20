import json
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在.")
        return None
    except json.JSONDecodeError:
        print(f"文件 {file_path} 不是有效的 JSON.")
        return None