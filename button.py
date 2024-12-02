import pygame

class Button:
    def __init__(self, x, y, width, height, text, callback, color=(247, 219, 240), hover_color=(232, 186, 221), text_color=(135, 121, 168), border_color=(135, 121, 168), border_width=2, border_radius=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font("fonts/NotoSansCJK-Regular.ttc", 25)
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.current_color = self.color
        self.callback = callback

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        self.current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color

        # 绘制边框
        if self.border_width > 0:
            border_rect = self.rect.inflate(self.border_width * 2, self.border_width * 2)
            pygame.draw.rect(screen, self.border_color, border_rect, border_radius=self.border_radius)

        # 绘制按钮
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=self.border_radius)
        # 绘制文字
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

class ImageButton(Button):
    def __init__(self, x, y, image, action=None):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.action = action

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                self.action()
