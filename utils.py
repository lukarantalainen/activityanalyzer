import json

def load_json(path):
    with open(path, "r") as f:
        try:
            return json.load(f)
        except Exception as e:
            print(e)
            return {}

def clear_json(path):
    with open(path, "w") as f:
        json.dump({}, f)

def save_json(data, path):
    try:
            with open(path, "w") as f:
                json.dump(data, f)
    except Exception as e:
        print(e)
