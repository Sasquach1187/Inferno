import pygame
import os

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
FPS = 60

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Inferno")

scroll = 0

# Load images
light_image = pygame.image.load("Lights.png").convert_alpha()
light_width = light_image.get_width()
light_height = light_image.get_height()

bg_images = []
for i in range(1, 9):
    image = pygame.image.load(f"layer-{i}.png").convert_alpha()
    bg_images.append(image)
bg_width = bg_images[0].get_width()

# Button class
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action

# Load button images
resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
options_img = pygame.image.load("images/button_options.png").convert_alpha()
quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
audio_img = pygame.image.load('images/button_audio.png').convert_alpha()
keys_img = pygame.image.load('images/button_keys.png').convert_alpha()
back_img = pygame.image.load('images/button_back.png').convert_alpha()

# Create button instances
resume_button = Button(304, 125, resume_img, 1)
options_button = Button(297, 250, options_img, 1)
quit_button = Button(336, 375, quit_img, 1)
audio_button = Button(225, 200, audio_img, 1)
keys_button = Button(246, 325, keys_img, 1)
back_button = Button(332, 450, back_img, 1)

# Draw background
def draw_bg():
    for x in range(9):
        speed = 1
        for i in bg_images:
            screen.blit(i, ((x * bg_width) - scroll * speed, 0))
            speed += 0.2

# Draw light
def draw_light():
    for x in range(15):
        screen.blit(light_image, ((x * light_width) - scroll * 2.2, SCREEN_HEIGHT - light_height))

# Draw text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0: idle
        for i in range(4):
            img = pygame.image.load(f'img/player/Idle/{i}.png').convert_alpha()  # Corrected file path
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            self.animation_list.append(img)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.update_time = pygame.time.get_ticks()

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        # Update animation
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0

    def update(self):
        self.update_animation()

    def draw(self):
        screen.blit(self.image, self.rect)

# Main game variables
run = True
game_paused = False
menu_state = "main"
TEXT_COL = (255, 255, 255)
font = pygame.font.SysFont("arialblack", 40)

# Create player instance
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Main game loop
while run:
    clock.tick(FPS)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_paused = not game_paused

    # Draw world or menu
    if game_paused:
        screen.fill((52, 78, 91))  # Fill screen with a color when paused
        if menu_state == "main":
            if resume_button.draw(screen):
                game_paused = False
            if options_button.draw(screen):
                menu_state = "options"
            if quit_button.draw(screen):
                run = False
        elif menu_state == "options":
            if audio_button.draw(screen):
                print("Audio Settings")
            if keys_button.draw(screen):
                print("Change Key Bindings")
            if back_button.draw(screen):
                menu_state = "main"
    else:
        screen.fill((0, 0, 0))  # Clear the screen
        draw_bg()
        draw_light()
        player.update()
        player.draw()

    pygame.display.update()

pygame.quit()
