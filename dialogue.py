# dialogue.py


# 保存全域狀態
current_page = "menu"
current_dialogue_index = 0
show_question = False

def get_current_page():
    """取得當前頁面"""
    global current_page
    return current_page

def set_current_page(page):
    """設置當前頁面"""
    global current_page
    current_page = page
    print(f"[調試] current_page 已更新為: {current_page}")

def advance_dialogue(dialogues_data, go_to_callback):
    """
    更新對話內容，處理對話和問題切換邏輯。
    """
    global current_dialogue_index, current_page, show_question
    page_data = dialogues_data.get(current_page, {})

    if not page_data:
        print(f"[錯誤] 無法找到頁面 {current_page} 的數據！")
        return

    dialogues = page_data.get("dialogues", [])
    question = page_data.get("question", None)

    print(f"[調試] 當前頁面: {current_page}, 對話索引: {current_dialogue_index}, 總對話數: {len(dialogues)}")

    # 如果對話未結束，繼續下一句
    if current_dialogue_index < len(dialogues) - 1:
        current_dialogue_index += 1
        print(f"[調試] 進入下一句對話，索引變為: {current_dialogue_index}")
    # 如果對話結束且有問題，顯示問題
    elif question and not show_question:
        show_question = True
        print(f"[調試] 對話結束，顯示問題: {question['text']}")
    # 如果問題已經顯示或者對話完全結束，跳轉到下一頁或結束當前頁面
    else:
        show_question = False
        if "next_page" in page_data:
            next_page = page_data["next_page"]
            current_dialogue_index = 0
            go_to_callback(next_page)
            print(f"[調試] 跳轉到下一頁面: {next_page}")
        else:
            print("[調試] 對話結束，且未定義下一頁面。")

def handle_question_click(pos, dialogues_data, go_to_callback, dialogue_box_rect):
    """
    處理問題選項點擊事件，判斷答案是否正確。
    """
    global current_page, show_question
    page_data = get_current_page_data(dialogues_data)
    question = page_data.get("question", None)

    if question:
        options = question["options"]
        correct_index = question["correct"]
        option_height = 50  # 每個選項的高度
        option_spacing = 10  # 選項間距
        start_y = dialogue_box_rect.y + 100  # 選項起始位置

        for i, option in enumerate(options):
            option_rect = pygame.Rect(
                dialogue_box_rect.x + 20,
                start_y + i * (option_height + option_spacing),
                dialogue_box_rect.width - 40,
                option_height,
                )
            if option_rect.collidepoint(pos):
                if i == correct_index:
                    print("回答正確！")
                    if "next_page" in page_data:
                        go_to_callback(page_data["next_page"])
                else:
                    print("回答錯誤！")
                show_question = False  # 無論對錯，隱藏問題
                return

