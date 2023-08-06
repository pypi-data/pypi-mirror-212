import json

def read_json_file(path: str) -> dict | list | None:
    try:
        with open(path, 'r') as f:
            result=json.load(f)
            return result
    except:
        return None

def write_json_file(obj:list | dict , file_name:str="default_json.json"):
    with open(file_name, 'w') as f:
        json.dump(obj, f, indent=4)