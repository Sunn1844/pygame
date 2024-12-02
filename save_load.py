import json

# 保存進度
def save_game(current_page, dialogue_index, save_file="save_data.json"):
    save_data = {
        "current_page": current_page,
        "dialogue_index": dialogue_index
    }
    with open(save_file, "w", encoding="utf-8") as file:
        json.dump(save_data, file, ensure_ascii=False, indent=4)
    print("遊戲進度已保存！")

# 加載進度
def load_game(save_file="save_data.json"):
    try:
        with open(save_file, "r", encoding="utf-8") as file:
            save_data = json.load(file)
            print("遊戲進度已加載！")
            return save_data
    except FileNotFoundError:
        print("未找到保存的遊戲進度！")
        return None
