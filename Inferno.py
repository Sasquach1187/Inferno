import pygame
import sys
import os




# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
FPS = 60




# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750


screen_width = SCREEN_WIDTH
screen_height = SCREEN_HEIGHT


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Inferno")
player_speed = 4


player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
       
# Define camera properties
camera_pos = [0, 0]






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
start_img = pygame.image.load("images/button_resume.png").convert_alpha()  # Used for start button
resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
options_img = pygame.image.load("images/button_options.png").convert_alpha()
quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
audio_img = pygame.image.load('images/button_audio.png').convert_alpha()
keys_img = pygame.image.load('images/button_keys.png').convert_alpha()
back_img = pygame.image.load('images/button_back.png').convert_alpha()




# Create button instances
start_button = Button(304, 125, start_img, 1)
resume_button = Button(304, 125, resume_img, 1)
options_button = Button(297, 250, options_img, 1)
quit_button = Button(336, 375, quit_img, 1)
audio_button = Button(225, 200, audio_img, 1)
keys_button = Button(246, 325, keys_img, 1)
back_button = Button(332, 450, back_img, 1)




# Load sounds
pygame.mixer.music.load('Oasis.wav')
click_sound = pygame.mixer.Sound('Oasis.wav')




# Set initial volume levels
background_music_volume = 0.4
sound_effects_volume = 0.4
pygame.mixer.music.set_volume(background_music_volume)
click_sound.set_volume(sound_effects_volume)




# Main loop
running = True
pygame.mixer.music.play(-1)  # Start playing background music




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


















# Health bar class
class HealthBar():
    def __init__(self, x, y, width, height, max_health):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_health = max_health
        self.health = max_health
















    def draw(self, surface):
        # Draw background
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        # Draw health
        health_rect = pygame.Rect(self.rect.x, self.rect.y, int(self.rect.width * (self.health / self.max_health)), self.rect.height)
        pygame.draw.rect(surface, (0, 255, 0), health_rect)
















    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
















# Load sprite images
sprite_folder = '120x80_PNGSheets'  # Folder containing the sprite images
idle_image = pygame.image.load(os.path.join(sprite_folder, '_Idle.png')).convert_alpha()
idle_frame_width = idle_image.get_width() // 10  # Assuming there are 10 frames in the idle animation
idle_frame_height = idle_image.get_height()
idle_frames = [idle_image.subsurface(pygame.Rect(i * idle_frame_width, 0, idle_frame_width, idle_frame_height)) for i in range(10)]
















# Load run image and slice it into frames
run_image = pygame.image.load(os.path.join(sprite_folder, '_Run.png')).convert_alpha()
run_frame_width = run_image.get_width() // 10  # Assuming there are 10 frames in the run animation
run_frame_height = run_image.get_height()
run_frames = [run_image.subsurface(pygame.Rect(i * run_frame_width, 0, run_frame_width, run_frame_height)) for i in range(10)]
















# Load jump images
jump_image = pygame.image.load(os.path.join(sprite_folder, '_Jump.png')).convert_alpha()
jump_fall_image = pygame.image.load(os.path.join(sprite_folder, '_Fall.png')).convert_alpha()
jump_frame_width = jump_image.get_width() // 3  # Assuming there are 3 frames in the jump animation
jump_frame_height = jump_image.get_height()
jump_frames = [jump_image.subsurface(pygame.Rect(i * jump_frame_width, 0, jump_frame_width, jump_frame_height)) for i in range(3)]
jump_fall_frame_width = jump_fall_image.get_width() // 3  # Assuming there are 3 frames in the jump animation
jump_fall_frame_height = jump_fall_image.get_height()
jump_fall_frames = [jump_fall_image.subsurface(pygame.Rect(i * jump_fall_frame_width, 0, jump_fall_frame_width, jump_fall_frame_height)) for i in range(3)]
















# Load attack image
attack_image = pygame.image.load(os.path.join(sprite_folder, '_Attack2.png')).convert_alpha()
attack_frame_width = attack_image.get_width() // 6  # Assuming there are 6 frames in the attack animation
attack_frame_height = attack_image.get_height()
attack_frames = [attack_image.subsurface(pygame.Rect(i * attack_frame_width, 0, attack_frame_width, attack_frame_height)) for i in range(6)]
















# Load roll image
roll_image = pygame.image.load(os.path.join(sprite_folder, '_Roll.png')).convert_alpha()
roll_frame_width = roll_image.get_width() // 12  # Assuming there are 12 frames in the roll animation
roll_frame_height = roll_image.get_height()
roll_frames = [roll_image.subsurface(pygame.Rect(i * roll_frame_width, 0, roll_frame_width, roll_frame_height)) for i in range(12)]












# Load Mushroom sprite sheets
shroom_folder = 'Mushroom'
enemy_idle_image = pygame.image.load(os.path.join(shroom_folder, 'Idle.png')).convert_alpha()
enemy_idle_frame_width = enemy_idle_image.get_width() // 4  # Assuming there are 4 frames in the idle animation
enemy_idle_frame_height = enemy_idle_image.get_height()
enemy_idle_frames = [enemy_idle_image.subsurface(pygame.Rect(i * enemy_idle_frame_width, 0, enemy_idle_frame_width, enemy_idle_frame_height)) for i in range(4)]
















enemy_run_image = pygame.image.load(os.path.join(shroom_folder, 'Run.png')).convert_alpha()
enemy_run_frame_width = enemy_run_image.get_width() // 8  # Assuming there are 8 frames in the run animation
enemy_run_frame_height = enemy_run_image.get_height()
enemy_run_frames = [enemy_run_image.subsurface(pygame.Rect(i * enemy_run_frame_width, 0, enemy_run_frame_width, enemy_run_frame_height)) for i in range(8)]
















enemy_attack_image = pygame.image.load(os.path.join(shroom_folder, 'Attack.png')).convert_alpha()
enemy_attack_frame_width = enemy_attack_image.get_width() // 8  # Assuming there are 8 frames in the attack animation
enemy_attack_frame_height = enemy_attack_image.get_height()
enemy_attack_frames = [enemy_attack_image.subsurface(pygame.Rect(i * enemy_attack_frame_width, 0, enemy_attack_frame_width, enemy_attack_frame_height)) for i in range(8)]
















enemy_death_image = pygame.image.load(os.path.join(shroom_folder, 'Death.png')).convert_alpha()
enemy_death_frame_width = enemy_death_image.get_width() // 4  # Assuming there are 4 frames in the death animation
enemy_death_frame_height = enemy_death_image.get_height()
enemy_death_frames = [enemy_death_image.subsurface(pygame.Rect(i * enemy_death_frame_width, 0, enemy_death_frame_width, enemy_death_frame_height)) for i in range(4)]
















skeleton_folder = 'Skeleton'
skeleton_idle_image = pygame.image.load(os.path.join(skeleton_folder, 'Idle.png')).convert_alpha()
skeleton_idle_frame_width = skeleton_idle_image.get_width() // 4  # Assuming there are 4 frames in the idle animation
skeleton_idle_frame_height = skeleton_idle_image.get_height()
skeleton_idle_frames = [skeleton_idle_image.subsurface(pygame.Rect(i * skeleton_idle_frame_width, 0, skeleton_idle_frame_width, skeleton_idle_frame_height)) for i in range(4)]
















skeleton_walk_image = pygame.image.load(os.path.join(skeleton_folder, 'Walk.png')).convert_alpha()
skeleton_walk_frame_width = skeleton_walk_image.get_width() // 4  # Assuming there are 4 frames in the walk animation
skeleton_walk_frame_height = skeleton_walk_image.get_height()
skeleton_walk_frames = [skeleton_walk_image.subsurface(pygame.Rect(i * skeleton_walk_frame_width, 0, skeleton_walk_frame_width, skeleton_walk_frame_height)) for i in range(4)]
















skeleton_attack_image = pygame.image.load(os.path.join(skeleton_folder, 'Attack.png')).convert_alpha()
skeleton_attack_frame_width = skeleton_attack_image.get_width() // 8  # Assuming there are 8 frames in the attack animation
skeleton_attack_frame_height = skeleton_attack_image.get_height()
skeleton_attack_frames = [skeleton_attack_image.subsurface(pygame.Rect(i * skeleton_attack_frame_width, 0, skeleton_attack_frame_width, skeleton_attack_frame_height)) for i in range(8)]
















skeleton_death_image = pygame.image.load(os.path.join(skeleton_folder, 'Death.png')).convert_alpha()
skeleton_death_frame_width = skeleton_death_image.get_width() // 4  # Assuming there are 4 frames in the death animation
skeleton_death_frame_height = skeleton_death_image.get_height()
skeleton_death_frames = [skeleton_death_image.subsurface(pygame.Rect(i * skeleton_death_frame_width, 0, skeleton_death_frame_width, skeleton_death_frame_height)) for i in range(4)]
















skeleton_shield_image = pygame.image.load(os.path.join(skeleton_folder, 'Shield.png')).convert_alpha()
skeleton_shield_frame_width = skeleton_shield_image.get_width() // 4  # Assuming there are 4 frames in the shield animation
skeleton_shield_frame_height = skeleton_shield_image.get_height()
skeleton_shield_frames = [skeleton_shield_image.subsurface(pygame.Rect(i * skeleton_shield_frame_width, 0, skeleton_shield_frame_width, skeleton_shield_frame_height)) for i in range(4)]
















# Load Goblin sprite sheets
goblin_folder = 'Goblin'
goblin_idle_image = pygame.image.load(os.path.join(goblin_folder, 'Idle.png')).convert_alpha()
goblin_idle_frame_width = goblin_idle_image.get_width() // 4  # Assuming there are 4 frames in the idle animation
goblin_idle_frame_height = goblin_idle_image.get_height()
goblin_idle_frames = [goblin_idle_image.subsurface(pygame.Rect(i * goblin_idle_frame_width, 0, goblin_idle_frame_width, goblin_idle_frame_height)) for i in range(4)]
















goblin_run_image = pygame.image.load(os.path.join(goblin_folder, 'Run.png')).convert_alpha()
goblin_run_frame_width = goblin_run_image.get_width() // 8  # Assuming there are 8 frames in the run animation
goblin_run_frame_height = goblin_run_image.get_height()
goblin_run_frames = [goblin_run_image.subsurface(pygame.Rect(i * goblin_run_frame_width, 0, goblin_run_frame_width, goblin_run_frame_height)) for i in range(8)]
















goblin_attack_image = pygame.image.load(os.path.join(goblin_folder, 'Attack.png')).convert_alpha()
goblin_attack_frame_width = goblin_attack_image.get_width() // 8  # Assuming there are 8 frames in the attack animation
goblin_attack_frame_height = goblin_attack_image.get_height()
goblin_attack_frames = [goblin_attack_image.subsurface(pygame.Rect(i * goblin_attack_frame_width, 0, goblin_attack_frame_width, goblin_attack_frame_height)) for i in range(8)]
















goblin_death_image = pygame.image.load(os.path.join(goblin_folder, 'Death.png')).convert_alpha()
goblin_death_frame_width = goblin_death_image.get_width() // 4  # Assuming there are 4 frames in the death animation
goblin_death_frame_height = goblin_death_image.get_height()
goblin_death_frames = [goblin_death_image.subsurface(pygame.Rect(i * goblin_death_frame_width, 0, goblin_death_frame_width, goblin_death_frame_height)) for i in range(4)]
















goblin_take_hit_image = pygame.image.load(os.path.join(goblin_folder, 'Take Hit.png')).convert_alpha()
goblin_take_hit_frame_width = goblin_take_hit_image.get_width() // 4  # Assuming there are 4 frames in the take hit animation
goblin_take_hit_frame_height = goblin_take_hit_image.get_height()
goblin_take_hit_frames = [goblin_take_hit_image.subsurface(pygame.Rect(i * goblin_take_hit_frame_width, 0, goblin_take_hit_frame_width, goblin_take_hit_frame_height)) for i in range(4)]
















# Scale up the frames
def scale_frames(frames, scale_factor):
    return [pygame.transform.scale(frame, (int(frame.get_width() * scale_factor), int(frame.get_height() * scale_factor))) for frame in frames]
















# Health bar class
class HealthBar(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, max_health):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.max_health = max_health
        self.health = max_health
        self.width = width
        self.height = height
        self.regen_rate = 2  # Amount of health to regenerate per tick
        self.regen_cooldown = 1000  # Time in milliseconds between each regeneration
        self.last_regen_time = pygame.time.get_ticks()


    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
        if self.health == 0:
            self.kill()


    def regenerate_health(self):
        now = pygame.time.get_ticks()
        if now - self.last_regen_time >= self.regen_cooldown:
            self.health = min(self.max_health, self.health + self.regen_rate)
            self.last_regen_time = now


    def draw(self, surface):
        health_ratio = self.health / self.max_health
        pygame.draw.rect(self.image, (255, 0, 0), (0, 0, self.width, self.height))
        pygame.draw.rect(self.image, (0, 255, 0), (0, 0, int(self.width * health_ratio), self.height))
        surface.blit(self.image, self.rect)
















# Sprite classes
class Player(pygame.sprite.Sprite):
    def __init__(self, scale_factor=2):
        super().__init__()
        # Load player frames and set initial parameters
        self.idle_frames = scale_frames(idle_frames, scale_factor)
        self.run_frames = scale_frames(run_frames, scale_factor)
        self.jump_frames = scale_frames(jump_frames, scale_factor)
        self.jump_fall_frames = scale_frames(jump_fall_frames, scale_factor)
        self.attack_frames = scale_frames(attack_frames, scale_factor)
        self.roll_frames = scale_frames(roll_frames, scale_factor)


        self.original_idle_frames = self.idle_frames
        self.original_run_frames = self.run_frames
        self.original_jump_frames = self.jump_frames
        self.original_jump_fall_frames = self.jump_fall_frames
        self.original_attack_frames = self.attack_frames
        self.original_roll_frames = self.roll_frames


        self.current_image = 0
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 570)
        self.speed = 4
       
        self.is_moving = False
        self.direction = 'right'
        self.is_jumping = False
        self.jump_velocity = 0
        self.gravity = 1
        self.jump_strength = -15
        self.is_attacking = False
        self.is_rolling = False
        self.last_update = pygame.time.get_ticks()
        self.idle_animation_speed = 200
        self.run_animation_speed = 100
        self.jump_animation_speed = 200
        self.attack_animation_speed = 100
        self.roll_animation_speed = 50
        self.current_idle_frame = 0
        self.current_run_frame = 0
        self.current_jump_frame = 0
        self.current_jump_fall_frame = 0
        self.current_attack_frame = 0
        self.current_roll_frame = 0


        self.health_bar = HealthBar(self.rect.x, self.rect.y - 20, 100, 10, 100)
       
       
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height


    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)


    def update(self, target):
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)


        # Limit scrolling to the map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.camera.width - self.width), x)  # right
        y = max(-(self.camera.height - self.height), y)  # bottom


        self.camera = pygame.Rect(x, y, self.width, self.height)
       
       
       


        # Cooldowns
        self.attack_cooldown = 1000  # 1 second cooldown for attack
        self.roll_cooldown = 1000  # 1 second cooldown for roll
        self.last_attack_time = 0
        self.last_roll_time = 0
       
       
   


    def update(self):
        keys = pygame.key.get_pressed()
        self.is_moving = False


        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.is_moving = True
            self.direction = 'left'
            player_pos[0] -= player_speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.is_moving = True
            self.direction = 'right'


        if not self.is_jumping and keys[pygame.K_SPACE]:
            self.is_jumping = True
            self.jump_velocity = self.jump_strength


        now = pygame.time.get_ticks()
        if self.is_jumping:
            self.rect.y += self.jump_velocity
            self.jump_velocity += self.gravity


            if self.jump_velocity >= 0:
                if now - self.last_update >= self.jump_animation_speed:
                    self.last_update = now
                    self.current_jump_fall_frame = (self.current_jump_fall_frame + 1) % len(self.jump_fall_frames)
                    self.image = self.jump_fall_frames[self.current_jump_fall_frame]
            else:
                if now - self.last_update >= self.jump_animation_speed:
                    self.last_update = now
                    self.current_jump_frame = (self.current_jump_frame + 1) % len(self.jump_frames)
                    self.image = self.jump_frames[self.current_jump_frame]


            if self.rect.y >= 570:
                self.rect.y = 570
                self.is_jumping = False
                self.jump_velocity = 0
        elif self.is_attacking:
            if now - self.last_update >= self.attack_animation_speed:
                self.last_update = now
                self.current_attack_frame = (self.current_attack_frame + 1) % len(self.attack_frames)
                self.image = self.attack_frames[self.current_attack_frame]
        elif self.is_rolling:
            if now - self.last_update >= self.roll_animation_speed:
                self.last_update = now
                self.current_roll_frame = (self.current_roll_frame + 1) % len(self.roll_frames)
                self.image = self.roll_frames[self.current_roll_frame]
            if self.current_roll_frame == len(self.roll_frames) - 1:
                self.is_rolling = False
        elif self.is_moving:
            if now - self.last_update >= self.run_animation_speed:
                self.last_update = now
                self.current_run_frame = (self.current_run_frame + 1) % len(self.run_frames)
                self.image = self.run_frames[self.current_run_frame]
        else:
            if now - self.last_update >= self.idle_animation_speed:
                self.last_update = now
                self.current_idle_frame = (self.current_idle_frame + 1) % len(self.idle_frames)
                self.image = self.idle_frames[self.current_idle_frame]


        if self.direction == 'left':
            self.idle_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_idle_frames]
            self.run_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_run_frames]
            self.jump_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_jump_frames]
            self.jump_fall_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_jump_fall_frames]
            self.attack_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_attack_frames]
            self.roll_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_roll_frames]
        else:
            self.idle_frames = self.original_idle_frames
            self.run_frames = self.original_run_frames
            self.jump_frames = self.original_jump_frames
            self.jump_fall_frames = self.original_jump_fall_frames
            self.attack_frames = self.original_attack_frames
            self.roll_frames = self.original_roll_frames


        self.health_bar.rect.x = self.rect.x
        self.health_bar.rect.y = self.rect.y - 20


        # Regenerate health
        self.health_bar.regenerate_health()


    def attack(self):
        now = pygame.time.get_ticks()
        if now - self.last_attack_time >= self.attack_cooldown:
            self.is_attacking = True
            self.current_attack_frame = 0
            self.last_attack_time = now
            pygame.time.set_timer(pygame.USEREVENT + 1, len(self.attack_frames) * self.attack_animation_speed)


    def roll(self):
        now = pygame.time.get_ticks()
        if now - self.last_roll_time >= self.roll_cooldown:
            self.is_rolling = True
            self.current_roll_frame = 0
            self.last_roll_time = now
            pygame.time.set_timer(pygame.USEREVENT + 2, len(self.roll_frames) * self.roll_animation_speed)


















class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, scale_factor=2):
        super().__init__()
        self.original_idle_frames = scale_frames(enemy_idle_frames, scale_factor)
        self.idle_frames = self.original_idle_frames.copy()
        self.original_run_frames = scale_frames(enemy_run_frames, scale_factor)
        self.run_frames = self.original_run_frames.copy()
        self.original_attack_frames = scale_frames(enemy_attack_frames, scale_factor)
        self.attack_frames = self.original_attack_frames.copy()
        self.original_death_frames = scale_frames(enemy_death_frames, scale_factor)
        self.death_frames = self.original_death_frames.copy()
        self.frames = self.idle_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.animation_speed = 400
        self.last_update = pygame.time.get_ticks()
        self.speed = 1  # Enemy movement speed (slower than player)
        self.direction = 'left'
        self.player = None  # Reference to the player
        self.attack_cooldown = 1000  # 2 seconds cooldown for attack
        self.last_attack = pygame.time.get_ticks()
        self.is_attacking = False
        self.attack_animation_speed = 100
        self.current_attack_frame = 0
        self.is_dead = False
        self.death_animation_speed = 200
        self.current_death_frame = 0
        self.death_time = 1000
        self.death_delay = 1000








        # Health bar
        self.health_bar = HealthBar(self.rect.x, self.rect.y - 20, 100, 10, 50)








    def update(self):
        now = pygame.time.get_ticks()
        if not self.is_dead:
            self.update_animation(now)
            self.update_movement(now)
            self.update_health_bar()
            self.handle_attack(now)
        else:
            self.handle_death(now)
            if self.current_death_frame == len(self.death_frames) - 1 and now - self.death_time >= self.death_delay:
                self.kill()  # Remove the sprite after the delay








        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x += self.speed
            self.is_moving = True
            self.direction = 'left'
        if keys[pygame.K_d]:
            self.rect.x -= self.speed
            self.is_moving = True
            self.direction = 'right'








    def update_animation(self, now):
        if now - self.last_update >= self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]








    def update_movement(self, now):
        if self.player:
            distance_to_player = self.rect.x - self.player.rect.x
            if distance_to_player < -50:  # Enemy is to the left of the player
                self.rect.x += self.speed
                self.direction = 'right'
                self.frames = self.run_frames
            elif distance_to_player > 50:  # Enemy is to the right of the player
                self.rect.x -= self.speed
                self.direction = 'left'
                self.frames = self.run_frames
            elif abs(distance_to_player) < 50:  # Enemy is too close to the player
                if distance_to_player < 0:
                    self.rect.x -= self.speed
                else:
                    self.rect.x += self.speed








            # Basic attack logic
            if abs(distance_to_player) < 50:
                if now - self.last_attack >= self.attack_cooldown:
                    self.last_attack = now
                    self.attack()
                    print("Enemy attacking player!")
                    self.player.health_bar.take_damage(10)
            else:
                self.frames = self.idle_frames








            # Flip the image based on direction
            self.flip_frames_based_on_direction()








    def flip_frames_based_on_direction(self):
        if self.direction == 'left':
            self.idle_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_idle_frames]
            self.run_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_run_frames]
            self.attack_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_attack_frames]
            self.death_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_death_frames]
        else:
            self.idle_frames = self.original_idle_frames
            self.run_frames = self.original_run_frames
            self.attack_frames = self.original_attack_frames
            self.death_frames = self.original_death_frames








    def update_health_bar(self):
        if not self.is_dead:
            self.health_bar.rect.x = self.rect.x
            self.health_bar.rect.y = self.rect.y - 20








    def handle_attack(self, now):
        if self.is_attacking:
            if now - self.last_update >= self.attack_animation_speed:
                self.last_update = now
                self.current_attack_frame = (self.current_attack_frame + 1) % len(self.attack_frames)
                self.image = self.attack_frames[self.current_attack_frame]
                # End attacking animation after one cycle
                if self.current_attack_frame == len(self.attack_frames) - 1:
                    self.is_attacking = False
                    self.frames = self.idle_frames








    def handle_death(self, now):
        if now - self.last_update >= self.death_animation_speed:
            self.last_update = now
            if self.current_death_frame < len(self.death_frames) - 1:
                self.current_death_frame += 1
                self.image = self.death_frames[self.current_death_frame]
            else:
                # Start the death timer after the animation completes
                if self.death_time == 0:
                    self.death_time = now
















    def take_damage(self, amount):
        if not self.is_dead:
            self.health_bar.take_damage(amount)
            if self.health_bar.health <= 0:
                self.die()








    def attack(self):
        self.is_attacking = True
        self.current_attack_frame = 0
        self.frames = self.attack_frames








    def die(self):
        self.is_dead = True
        self.current_death_frame = 0
        self.frames = self.death_frames
        global score
        score += 1  # Increment the score when an enemy dies
























class Skeleton(pygame.sprite.Sprite):
    def __init__(self, x, y, scale_factor=2):
        super().__init__()
        self.original_idle_frames = scale_frames(skeleton_idle_frames, scale_factor)
        self.idle_frames = self.original_idle_frames.copy()
        self.original_walk_frames = scale_frames(skeleton_walk_frames, scale_factor)
        self.walk_frames = self.original_walk_frames.copy()
        self.original_attack_frames = scale_frames(skeleton_attack_frames, scale_factor)
        self.attack_frames = self.original_attack_frames.copy()
        self.original_death_frames = scale_frames(skeleton_death_frames, scale_factor)
        self.death_frames = self.original_death_frames.copy()
        self.original_shield_frames = scale_frames(skeleton_shield_frames, scale_factor)
        self.shield_frames = self.original_shield_frames.copy()
       
        self.frames = self.idle_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.animation_speed = 400
        self.last_update = pygame.time.get_ticks()
        self.speed = 3  # Enemy movement speed
        self.direction = 'left'
        self.player = None  # Reference to the player
        self.attack_cooldown = 1000  # 1 second cooldown for attack
        self.last_attack = pygame.time.get_ticks()
        self.is_attacking = False
        self.attack_animation_speed = 100
        self.current_attack_frame = 0
        self.is_dead = False
        self.death_animation_speed = 200
        self.current_death_frame = 0
        self.is_shielding = False
        self.shield_animation_speed = 100
        self.death_time = 1000
        self.death_delay = 1000
















        # Health bar
        self.health_bar = HealthBar(self.rect.x, self.rect.y - 20, 100, 10, 50)
















    def update(self):
        now = pygame.time.get_ticks()
        if not self.is_dead:
            self.update_animation(now)
            self.update_movement(now)
            self.update_health_bar()
            self.handle_attack(now)
        else:
            self.handle_death(now)
            if self.current_death_frame == len(self.death_frames) - 1 and now - self.death_time >= self.death_delay:
                self.kill()  # Remove the sprite after the delay
           
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x += self.speed
            self.is_moving = True
            self.direction = 'left'
        if keys[pygame.K_d]:
            self.rect.x -= self.speed
            self.is_moving = True
            self.direction = 'right'
           
















    def update_animation(self, now):
        if now - self.last_update >= self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
















    def update_movement(self, now):
        if self.player:
            if self.rect.x < self.player.rect.x:
                self.rect.x += self.speed
                self.direction = 'right'
                self.frames = self.walk_frames
            elif self.rect.x > self.player.rect.x:
                self.rect.x -= self.speed
                self.direction = 'left'
                self.frames = self.walk_frames
















            # Basic attack logic
            if abs(self.rect.x - self.player.rect.x) < 50:
                if now - self.last_attack >= self.attack_cooldown:
                    self.last_attack = now
                    self.attack()
                    print("Skeleton attacking player!")
                    self.player.health_bar.take_damage(20)
            else:
                self.frames = self.idle_frames
















            # Flip the image based on direction
            self.flip_frames_based_on_direction()
















    def flip_frames_based_on_direction(self):
        if self.direction == 'left':
            self.idle_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_idle_frames]
            self.walk_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_walk_frames]
            self.attack_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_attack_frames]
            self.death_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_death_frames]
            self.shield_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_shield_frames]
        else:
            self.idle_frames = self.original_idle_frames
            self.walk_frames = self.original_walk_frames
            self.attack_frames = self.original_attack_frames
            self.death_frames = self.original_death_frames
            self.shield_frames = self.original_shield_frames
















    def update_health_bar(self):
        if not self.is_dead:
            self.health_bar.rect.x = self.rect.x
            self.health_bar.rect.y = self.rect.y - 20
















    def handle_attack(self, now):
        if self.is_attacking:
            if now - self.last_update >= self.attack_animation_speed:
                self.last_update = now
                self.current_attack_frame = (self.current_attack_frame + 1) % len(self.attack_frames)
                self.image = self.attack_frames[self.current_attack_frame]
                # End attacking animation after one cycle
                if self.current_attack_frame == len(self.attack_frames) - 1:
                    self.is_attacking = False
                    self.frames = self.idle_frames
















    def handle_death(self, now):
        if now - self.last_update >= self.death_animation_speed:
            self.last_update = now
            if self.current_death_frame < len(self.death_frames) - 1:
                self.current_death_frame += 1
                self.image = self.death_frames[self.current_death_frame]
















    def take_damage(self, amount):
        if not self.is_dead:
            self.health_bar.take_damage(amount)
            if self.health_bar.health <= 0:
                self.die()
















    def attack(self):
        self.is_attacking = True
        self.current_attack_frame = 0
        self.frames = self.attack_frames
















    def die(self):
        self.is_dead = True
        self.current_death_frame = 0
        self.frames = self.death_frames
        global score
        score += 1  # Increment the score when an enemy dies
















    def shield(self):
        self.is_shielding = True
        self.current_shield_frame = 0
        self.frames = self.shield_frames
















class Goblin(pygame.sprite.Sprite):
    def __init__(self, x, y, scale_factor=2):
        super().__init__()
        self.original_idle_frames = scale_frames(goblin_idle_frames, scale_factor)
        self.idle_frames = self.original_idle_frames.copy()
        self.original_run_frames = scale_frames(goblin_run_frames, scale_factor)
        self.run_frames = self.original_run_frames.copy()
        self.original_attack_frames = scale_frames(goblin_attack_frames, scale_factor)
        self.attack_frames = self.original_attack_frames.copy()
        self.original_death_frames = scale_frames(goblin_death_frames, scale_factor)
        self.death_frames = self.original_death_frames.copy()
        self.original_take_hit_frames = scale_frames(goblin_take_hit_frames, scale_factor)
        self.take_hit_frames = self.original_take_hit_frames.copy()
       
        self.frames = self.idle_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.animation_speed = 400
        self.last_update = pygame.time.get_ticks()
        self.speed = 3  # Enemy movement speed
        self.direction = 'left'
        self.player = None  # Reference to the player
        self.attack_cooldown = 1000  # 1 second cooldown for attack
        self.last_attack = pygame.time.get_ticks()
        self.is_attacking = False
        self.attack_animation_speed = 100
        self.current_attack_frame = 0
        self.is_dead = False
        self.death_animation_speed = 200
        self.current_death_frame = 0
        self.death_time = 1000
        self.death_delay = 1000
















        # Health bar
        self.health_bar = HealthBar(self.rect.x, self.rect.y - 20, 100, 10, 50)
















    def update(self):
        now = pygame.time.get_ticks()
        if not self.is_dead:
            self.update_animation(now)
            self.update_movement(now)
            self.update_health_bar()
            self.handle_attack(now)
        else:
            self.handle_death(now)
            if self.current_death_frame == len(self.death_frames) - 1 and now - self.death_time >= self.death_delay:
                self.kill()  # Remove the sprite after the delay
           
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x += self.speed
            self.is_moving = True
            self.direction = 'left'
        if keys[pygame.K_d]:
            self.rect.x -= self.speed
            self.is_moving = True
            self.direction = 'right'
















    def update_animation(self, now):
        if now - self.last_update >= self.animation_speed:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
















    def update_movement(self, now):
        if self.player:
            if self.rect.x < self.player.rect.x:
                self.rect.x += self.speed
                self.direction = 'right'
                self.frames = self.run_frames
            elif self.rect.x > self.player.rect.x:
                self.rect.x -= self.speed
                self.direction = 'left'
                self.frames = self.run_frames
















            # Basic attack logic
            if abs(self.rect.x - self.player.rect.x) < 50:
                if now - self.last_attack >= self.attack_cooldown:
                    self.last_attack = now
                    self.attack()
                    print("Goblin attacking player!")
                    self.player.health_bar.take_damage(20)
            else:
                self.frames = self.idle_frames
















            # Flip the image based on direction
            self.flip_frames_based_on_direction()
















    def flip_frames_based_on_direction(self):
        if self.direction == 'left':
            self.idle_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_idle_frames]
            self.run_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_run_frames]
            self.attack_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_attack_frames]
            self.death_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_death_frames]
            self.take_hit_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_take_hit_frames]
        else:
            self.idle_frames = self.original_idle_frames
            self.run_frames = self.original_run_frames
            self.attack_frames = self.original_attack_frames
            self.death_frames = self.original_death_frames
            self.take_hit_frames = self.original_take_hit_frames
















    def update_health_bar(self):
        if not self.is_dead:
            self.health_bar.rect.x = self.rect.x
            self.health_bar.rect.y = self.rect.y - 20
















    def handle_attack(self, now):
        if self.is_attacking:
            if now - self.last_update >= self.attack_animation_speed:
                self.last_update = now
                self.current_attack_frame = (self.current_attack_frame + 1) % len(self.attack_frames)
                self.image = self.attack_frames[self.current_attack_frame]
                # End attacking animation after one cycle
                if self.current_attack_frame == len(self.attack_frames) - 1:
                    self.is_attacking = False
                    self.frames = self.idle_frames
















    def handle_death(self, now):
        if now - self.last_update >= self.death_animation_speed:
            self.last_update = now
            if self.current_death_frame < len(self.death_frames) - 1:
                self.current_death_frame += 1
                self.image = self.death_frames[self.current_death_frame]
















    def take_damage(self, amount):
        if not self.is_dead:
            self.health_bar.take_damage(amount)
            if self.health_bar.health <= 0:
                self.die()
















    def attack(self):
        self.is_attacking = True
        self.current_attack_frame = 0
        self.frames = self.attack_frames
















    def die(self):
        self.is_dead = True
        self.current_death_frame = 0
        self.frames = self.death_frames
        global score
        score += 1  # Increment the score when an enemy dies
















# Create player sprite
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
















# Create enemy sprites
mushroom1 = Enemy(300, 530)  # Adjust the position as needed
mushroom1.player = player  # Assign the player reference
all_sprites.add(mushroom1)
















mushroom2 = Enemy(500, 530)  # Another enemy
mushroom2.player = player  # Assign the player reference
all_sprites.add(mushroom2)
























def draw_audio_settings():
    draw_text("Audio Settings", font, TEXT_COL, 250, 100)
    draw_text("Background Music", font, TEXT_COL, 150, 150)
    draw_text("Sound Effects", font, TEXT_COL, 150, 250)
    pygame.draw.rect(screen, (255, 255, 255), bg_music_slider)
    pygame.draw.rect(screen, (0, 0, 255), bg_music_slider_knob)
    pygame.draw.rect(screen, (255, 255, 255), sfx_slider)
    pygame.draw.rect(screen, (0, 0, 255), sfx_slider_knob)




def main_menu():
    screen.fill((52, 78, 91))  # Fill screen with a color for the main menu
    if start_button.draw(screen):
        return "game"
    if options_button.draw(screen):
        return "options"
    if quit_button.draw(screen):
        pygame.quit()
        sys.exit()
    return "main_menu"




def game_over_screen():
    screen.fill((0, 0, 0))  # Fill the screen with black
    draw_text("Game Over", font, (255, 0, 0), SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
    draw_text("Press R to Restart", font, (255, 255, 255), SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 10)
    pygame.display.flip()




    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    return "main_menu"




# Scoring system
score = 0




# Audio settings slider variables
bg_music_slider = pygame.Rect(150, 200, 200, 20)
bg_music_slider_knob = pygame.Rect(150, 195, 10, 30)
sfx_slider = pygame.Rect(150, 300, 200, 20)
sfx_slider_knob = pygame.Rect(150, 295, 10, 30)
dragging_bg_knob = False
dragging_sfx_knob = False




run = True
game_paused = False
menu_state = "main_menu"  # Start with the main menu
TEXT_COL = (255, 255, 255)
font = pygame.font.SysFont("arialblack", 40)


# Initialize the camera with the screen size
camera = Camera(screen_width, screen_height)






# Main game loop
while run:
    clock.tick(FPS)
    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_paused = not game_paused
                if game_paused:
                    menu_state = "main"
            if event.key == pygame.K_SPACE and not game_paused:
                player.is_jumping = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                player.attack()
                # Check if the player is close enough to the enemy to hit
                for enemy in [mushroom1, mushroom2]:
                    if abs(player.rect.x - enemy.rect.x) < 50:
                        enemy.take_damage(10)
            if event.button == 3:  # Right mouse button
                player.roll()
            if bg_music_slider_knob.collidepoint(event.pos):
                dragging_bg_knob = True
            if sfx_slider_knob.collidepoint(event.pos):
                dragging_sfx_knob = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging_bg_knob = False
                dragging_sfx_knob = False
        if event.type == pygame.MOUSEMOTION:
            if dragging_bg_knob:
                bg_music_slider_knob.x = max(bg_music_slider.x, min(event.pos[0], bg_music_slider.x + bg_music_slider.width - bg_music_slider_knob.width))
                background_music_volume = (bg_music_slider_knob.x - bg_music_slider.x) / (bg_music_slider.width - bg_music_slider_knob.width)
                pygame.mixer.music.set_volume(background_music_volume)
            if dragging_sfx_knob:
                sfx_slider_knob.x = max(sfx_slider.x, min(event.pos[0], sfx_slider.x + sfx_slider.width - sfx_slider_knob.width))
                sound_effects_volume = (sfx_slider_knob.x - sfx_slider.x) / (sfx_slider.width - sfx_slider_knob.width)
                click_sound.set_volume(sound_effects_volume)
        if event.type == pygame.USEREVENT + 1:
            player.is_attacking = False
        if event.type == pygame.USEREVENT + 2:
            player.is_rolling = False
           
     # Update the camera
    camera.update(player)
     # Apply the camera offset to the player and other sprites
    for entity in all_sprites:
        screen.blit(entity.image, camera.apply(entity))




    # Draw world or menu
    if menu_state == "main_menu":
        menu_state = main_menu()
    elif menu_state == "game_over":
        menu_state = game_over_screen()
    elif game_paused:
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
                menu_state = "audio"
            if keys_button.draw(screen):
                print("Change Key Bindings")
            if back_button.draw(screen):
                menu_state = "main"
        elif menu_state == "audio":
            draw_audio_settings()
            if back_button.draw(screen):
                menu_state = "options"
    else:
        screen.fill((0, 0, 0))  # Clear the screen
        draw_bg()
        draw_light()
        key = pygame.key.get_pressed()
        if key[pygame.K_a] and scroll > 0:
            scroll -= 2
        if key[pygame.K_d] and scroll < 3000:
            scroll += 2




        # Draw all sprites
        all_sprites.update()
        all_sprites.draw(screen)




        # Draw health bars
        player.health_bar.draw(screen)
        for enemy in [mushroom1, mushroom2]:
            if not enemy.is_dead:
                enemy.health_bar.draw(screen)




        # Draw score
        draw_text(f"Score: {score}", font, TEXT_COL, 10, 10)




        # Check for game over
        if player.health_bar.health <= 0:
            menu_state = "game_over"




    pygame.display.update()




pygame.quit()