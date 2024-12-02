

import pygame
import json
from button import Button, ImageButton
from save_load import save_game, load_game

# 加載對話文件
with open("dialogues.json", "r", encoding="utf-8") as file:
    dialogues_data = json.load(file)

# 初始化
pygame.init()
screen_width, screen_height = 1040, 585
window_surface = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("撲通撲通甜蜜冒險！")
# 設置字體，使用支持中文的字體
font_path = "fonts/NotoSansCJK-Regular.ttc"  # 確保路徑正確
font = pygame.font.Font(font_path, 20)

# 加載背景圖
background_images = {
    "menu": pygame.image.load("img/background.png").convert(),
    "name_input": pygame.image.load("img/page1.png").convert(),
    "page1": pygame.image.load("img/page1.jpg").convert(),
    "page2": pygame.image.load("img/page2.webp").convert(),
    "page3": pygame.image.load("img/page2-1.jpg").convert(),
    "page4": pygame.image.load("img/page13.jpg").convert(),
    "page5": pygame.image.load("img/page3.jpg").convert(),
    "page6": pygame.image.load("img/page4.jpg").convert(),
    "page7": pygame.image.load("img/page5.jpg").convert(),
    "page8": pygame.image.load("img/page6.jpg").convert(),
    "page9": pygame.image.load("img/page7.jpg").convert(),
    "page10": pygame.image.load("img/page8.jpg").convert(),
    "page11": pygame.image.load("img/page9.jpg").convert(),
    "page12": pygame.image.load("img/page10.jpg").convert(),
    "page13": pygame.image.load("img/page11.jpg").convert(),
    "page14": pygame.image.load("img/page12.jpg").convert(),
    "retry_page1": pygame.image.load("img/page1.jpg").convert(),
    "retry_page2": pygame.image.load("img/page15.png").convert(),
    "retry_page3": pygame.image.load("img/page6.jpg").convert(),
    "retry_page4": pygame.image.load("img/page9.jpg").convert(),
    "success_page1": pygame.image.load("img/page14.jpg").convert(),
    "success_page2": pygame.image.load("img/page2-1.jpg").convert(),
    "success_page3": pygame.image.load("img/page6.jpg").convert(),
    "success_page4": pygame.image.load("img/page9.jpg").convert(),
}
for key in background_images:
    background_images[key] = pygame.transform.scale(background_images[key], (screen_width, screen_height))

# 加載按鈕圖片
menu_button_image = pygame.image.load("img/menu.png").convert_alpha()  # 使用 .convert_alpha() 以支持透明背景
menu_button_image = pygame.transform.scale(menu_button_image, (60, 60))

# 取得目前頁面數據
def get_current_page_data():
    return dialogues_data[current_page]

# 頁面狀態
current_page: str = "menu"
player_name: str = ""
current_dialogue_index = 0
show_menu = False  # 是否显示菜单
show_question = False  # 是否显示问题
input_active = False  # 控制輸入框是否被激活
color_inactive = pygame.Color("gray")  # 未激活時的邊框顏色
color_active = pygame.Color("lightskyblue")  # 激活時的邊框顏色
input_color = color_inactive  # 初始為未激活狀態

# 開始新遊戲
def start_new_game():
    """
    開始新遊戲，重置對話進度並跳轉到第一頁。
    """
    global current_dialogue_index, player_name, show_menu, show_question
    current_dialogue_index = 0  # 重置對話索引
    player_name = ""  # 重置玩家名字
    show_menu = False  # 隱藏菜單
    show_question = False  # 隱藏問題
    go_to("name_input")  # 跳轉到第一頁

# 切換頁面
def go_to(page_id):
    global current_page, show_menu
    if page_id in background_images:
        current_page = page_id # 更新 current_page
        show_menu = False  # 切換頁面時自動關閉菜單
    else:
        print(f"錯誤：頁面 '{page_id}' 尚未定義！")

# 切換菜單顯示狀態
def toggle_menu():
    global show_menu
    show_menu = not show_menu

# 保存邏輯
def save_game_logic():
    save_game(current_page, current_dialogue_index)
    toggle_menu()  # 保存後關閉選單

# 加載邏輯
def load_game_logic():
    global current_page, current_dialogue_index
    save_data = load_game()
    if save_data:
        current_page = save_data["current_page"]
        current_dialogue_index = save_data["dialogue_index"]


# 按鈕
btn_start = Button(305, 420, 200, 50, "開始遊戲", lambda: go_to("name_input"))
btn_load = Button(535, 420, 200, 50, "讀取進度", load_game_logic)
btn_menu = ImageButton(screen_width - 70, 5, menu_button_image, lambda: toggle_menu())
btn_save = Button(screen_width - 220, 80, 200, 50, "儲存遊戲進度", save_game_logic)
btn_exit = Button(screen_width - 220, 140, 200, 50, "回到主畫面", lambda: go_to("menu"))
btn_ok = Button(305, 420, 200, 50, "ok", lambda: go_to("page1"))

def go_to_name_input():
    global current_page
    current_page = "name_input"

# 新增一個名為 name_input 的頁面
def draw_name_input_page():
    global player_name

    # 绘制背景
    window_surface.blit(background_images["name_input"], (0, 0))
    

    # 绘制输入框
    input_box = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 20, 300, 50)
    pygame.draw.rect(window_surface, (255, 255, 255), input_box, 2)  # 绘制输入框边框


    # 绘制玩家输入的名字
    text_surface = font.render(player_name, True, (255, 255, 255))
    window_surface.blit(text_surface, (input_box.x + 10, input_box.y + 10))

    # 绘制 "请输入你的名字" 提示文本
    prompt_text = font.render("请输入你的名字:", True, (255, 255, 255))
    window_surface.blit(prompt_text, (screen_width // 2 - prompt_text.get_width() // 2, screen_height // 2 - 80))

    # 绘制 "OK" 按钮
    btn_ok.draw(window_surface)

# 更新事件处理逻辑
def handle_name_input_event(event):
    global text, active, player_name, input_active, input_color
    color_inactive = pygame.Color("gray")  # 未激活狀態顏色
    input_box = pygame.Rect(screen_width // 2 - 150, screen_height // 2 - 20, 300, 50)
    text = ""  # 儲存玩家輸入的文本
    # 處理鼠標點擊事件
    if event.type == pygame.MOUSEBUTTONDOWN:
        # 如果點擊了輸入框，則激活該框
        if input_box.collidepoint(event.pos):
            input_active = True  # 激活輸入框
            input_color = color_active
        else:
            input_active = False  # 停止激活
            input_color = color_inactive

    # 處理鍵盤按鍵事件
    if event.type == pygame.KEYDOWN:
        if input_active:
            if event.key == pygame.K_RETURN:  # 當按下回車鍵
                player_name = text  # 儲存玩家名字
                print(f"玩家名字是: {player_name}")
                text = ""  # 清空輸入框中的文字
            elif event.key == pygame.K_BACKSPACE:  # 當按下退格鍵
                text = text[:-1]  # 刪除最後一個字符
            else:
                text += event.unicode  # 其他字符直接添加到輸入框中


def handle_question_answer(user_answer, current_page_data, go_to_callback):
    # 獲取問題數據
    question = current_page_data.get("question")
    if not question:
        return  # 沒有問題，直接返回

    # 檢查答案是否正確
    correct_answer = question["answer"]
    if user_answer == correct_answer:
        print("[調試] 答對了！")
        next_page = question.get("success_page")
    else:
        print("[調試] 答錯了！")
        next_page = question.get("retry_page")

    # 跳轉到對應頁面
    if next_page :
        print(f"[調試] 跳轉到頁面: {next_page}")
        go_to_callback(next_page)
    else:
        print("[調試] 沒有設定下一頁。")


# 更新對話內容，處理對話和問題切換邏輯
def advance_dialogue(dialogues_data, go_to_callback):
    """
    更新對話內容，處理對話和問題切換邏輯。
    """
    global current_dialogue_index, current_page, show_question

    # 取得當前頁面的數據
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

# 問題與選項的顯示和點擊邏輯
def display_question_and_options(window_surface, dialogue_box_rect, question, font):
    """
    在對話框中顯示問題和並排選項。
    """

    #question_text = f"{question['hint']}"
    # 繪製問題文本
    question_text = f"問題：{question['tet']}"
    wrapped_lines = render_text_wrapped(question_text, font, (255, 255, 255), dialogue_box_rect.width - 40)
    text_y = dialogue_box_rect.y + 20
    for line in wrapped_lines:
        question_surface = font.render(line, True, (255, 255, 255))
        window_surface.blit(question_surface, (dialogue_box_rect.x + 20, text_y))
        text_y += 30  # 行間距

    # 並排顯示選項
    options = question["options"]
    option_rects = []
    total_spacing = 20  # 選項間的間距
    option_width = (dialogue_box_rect.width - 40 - total_spacing * (len(options) - 1)) // len(options)
    option_height = 50
    start_x = dialogue_box_rect.x + 20

    for i, option in enumerate(options):
        option_text = f"{i + 1}. {option}"  # 加上序號
        option_surface = font.render(option_text, True, (255, 255, 255))

        # 計算每個選項的位置
        option_x = start_x + i * (option_width + total_spacing)
        option_y = text_y + 20  # 選項位置距離問題文本稍微下移
        option_rect = pygame.Rect(option_x, option_y, option_width, option_height)
        option_rects.append(option_rect)

        # 繪製選項區域（半透明背景）
        pygame.draw.rect(window_surface, (100, 100, 100, 180), option_rect, border_radius=5)
        window_surface.blit(option_surface, (option_x + 10, option_y + 10))  # 選項文本稍微內縮

    return option_rects

# 處理問題選項點擊事件
def handle_question_click(pos, question, option_rects, current_page, dialogues_data):
    """
    處理問題選項點擊事件，檢查回答是否正確，並更新頁面。
    """
    global show_question
    #global current_page
    #current_page = "page1"  # 更新 current_page

    # 檢查每個選項是否被點擊
    for i, option_rect in enumerate(option_rects):
        if option_rect.collidepoint(pos):
            correct_index = question["correct"]  # 獲取正確答案索引
            if i == correct_index:
                print("回答正確！")
                next_page = dialogues_data.get(current_page, {}).get("right_page")  # 獲取下一頁
                if next_page:
                    print(f"跳轉到下一頁: {next_page}")
                    # 更新 current_page 並清除對話進度
                    current_page = next_page
                    go_to(current_page)
                    reset_dialogue()  # 清除對話進度的輔助函數
            else:
                print("回答錯誤！")
                next_page = dialogues_data.get(current_page, {}).get("wrong_page")  # 獲取下一頁
                if next_page:
                    print(f"跳轉到下一頁: {next_page}")
                    # 更新 current_page 並清除對話進度
                    current_page = next_page
                    go_to(current_page)
                    reset_dialogue()  # 清除對話進度的輔助函數
            show_question = False  # 無論正誤，隱藏問題
            return current_page  # 返回新的頁面
    return current_page  # 如果未點擊選項，保持頁面不變




# 重置對話進度
def reset_dialogue():
    """重置對話進度"""
    global current_dialogue_index
    current_dialogue_index = 0

# 對話框
def draw_rounded_rect(surface, color, rect, border_radius):
    pygame.draw.rect(surface, color, rect, border_radius=border_radius)

# 將文字自動換行的函數
def render_text_wrapped(text, font, color, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""
    for word in words:
        # 測量加入單詞後的寬度
        test_line = f"{current_line} {word}".strip()
        text_width, _ = font.size(test_line)
        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:  # 添加剩餘的文字
        lines.append(current_line)
    return lines


# 初始化對話框參數
dialogue_box_height = 160
dialogue_box_color = (168, 160, 160, 180)  # 黑色，透明度 180
dialogue_box_rect = pygame.Rect(20, screen_height - dialogue_box_height - 20, screen_width - 40, dialogue_box_height)
dialogue_box_border_radius = 20
max_text_width = dialogue_box_rect.width - 40  # 留出左右邊距

# 繪製遮罩
def draw_overlay(surface, color=(0, 0, 0, 128)):
    """
    半透明遮罩。
    :param surface: 目標繪製的表面
    :param color: 遮罩顏色，預設為黑色半透明
    """
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill(color)
    surface.blit(overlay, (0, 0))

# 主循環
running = True
while running:
    page_data = get_current_page_data()
    dialogues = page_data.get("dialogues", [])
    question = page_data.get("question", None)
    # 取得背景圖
    background_image = background_images[current_page]
    window_surface.blit(background_image, (0, 0))

    # 只有在非主畫面時繪製對話框
    if current_page != "menu"and"name_input":
        # 繪製圓角半透明對話框
        dialogue_surface = pygame.Surface((dialogue_box_rect.width, dialogue_box_rect.height), pygame.SRCALPHA)
        draw_rounded_rect(dialogue_surface, dialogue_box_color, dialogue_surface.get_rect(), dialogue_box_border_radius)
        window_surface.blit(dialogue_surface, (dialogue_box_rect.x, dialogue_box_rect.y))


        # 顯示圖片
        if not show_question and ".jpg" in dialogues[current_dialogue_index]:
            draw_overlay(window_surface)
            image_path = dialogues[current_dialogue_index]
            image = pygame.image.load(image_path).convert_alpha()
            image_rect = image.get_rect(center=(screen_width // 2, screen_height // 2))
            window_surface.blit(image, image_rect)

        # 如果有對話內容，繪製在對話框內
        if not show_question and current_dialogue_index < len(dialogues) and not ".jpg" in dialogues[current_dialogue_index]:
            dialogue_text = dialogues[current_dialogue_index]
            wrapped_lines = render_text_wrapped(dialogue_text, font, (255, 255, 255), max_text_width)
            text_y = dialogue_box_rect.y + 20
            for line in wrapped_lines:
                dialogue_surface = font.render(line, True, (255, 255, 255))
                window_surface.blit(dialogue_surface, (dialogue_box_rect.x + 20, text_y))
                text_y += 30  # 行間距

        # 如果有問題，顯示在對話框中
        if show_question and question:
            option_rects = display_question_and_options(window_surface, dialogue_box_rect, question, font)

    # 根據目前頁面繪製內容
    if current_page == "menu":
        btn_start.draw(window_surface)
        btn_load.draw(window_surface)
    elif current_page == "name_input":
        # 在 name_input 頁面時，顯示名字輸入框
        draw_name_input_page()
        go_to_name_input()
        handle_name_input_event(event)
    else:
        btn_menu.draw(window_surface)

        # 菜單
        if show_menu:
            draw_overlay(window_surface)
            btn_save.draw(window_surface)
            btn_exit.draw(window_surface)

    # 事件處理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_page != "menu":
                if show_question and question:
                    # 假設 option_rects 是 display_question_and_options 函數生成的矩形區域列表
                    handle_question_click(
                        pos=event.pos,
                        question=question,
                        option_rects=option_rects,  # 必須由對應顯示邏輯生成並傳遞
                        current_page=current_page,
                        dialogues_data=dialogues_data
                    )
                else:
                    advance_dialogue(dialogues_data, go_to)
        if current_page == "menu":
            btn_start.handle_event(event)
            btn_load.handle_event(event)
        elif current_page == "name_input":
            go_to_name_input()
            handle_name_input_event(event)  # 处理名字输入框的事件
            btn_ok.handle_event(event)
     
            
            if player_name and event.type == pygame.MOUSEBUTTONDOWN and btn_ok.rect.collidepoint(event.pos):
                go_to("page1")  # 跳转到page1，开始游戏
        else:
            btn_menu.handle_event(event)

            # 如果菜单显示，处理菜单按钮的点击事件
            if show_menu:
                btn_save.handle_event(event)
                btn_exit.handle_event(event)


    # 更新屏幕
    pygame.display.update()

pygame.quit()
