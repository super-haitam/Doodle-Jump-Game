# Doodle Jump Game
import random
import pygame
pygame.init()
pygame.font.init()

# Screen
WIDTH, HEIGHT = 600, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump")

# Colors
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
PSEUDO_WHITE = tuple(random.randint(200, 255) for _ in range(3))

# Background image
bg_image = pygame.transform.scale(pygame.image.load("assets/background.png"), (WIDTH, HEIGHT))


# Classes
class Player:
    def __init__(self, x, y):
        self.size = 80

        self.images_dict = {
            "right": pygame.transform.scale(pygame.image.load("assets/doodle_jump right.png"), (self.size, self.size)),
            "left": pygame.transform.scale(pygame.image.load("assets/doodle_jump left.png"), (self.size, self.size))
        }

        self.image = self.images_dict["right"]
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y - self.size
        self.old_y = self.rect.y

        self.is_jump = False
        self.reset_jump_count()

        self.reset_gravity()
        self.score = self.highest_score = 0

    def reset_jump_count(self): self.jump_count = -10

    def implement_jump_count(self): self.jump_count += 1

    def handle_collision(self):
        collided_rect = self.is_collision(platforms_list)
        if collided_rect:
            self.rect.bottom = collided_rect.y
            self.jump()
            self.reset_gravity()

    def handle_movement(self):
        self.apply_gravity()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += 10
            self.image = self.images_dict["right"]
        elif keys[pygame.K_LEFT]:
            self.rect.x -= 10
            self.image = self.images_dict["left"]

        if self.is_jump:
            self.rect.y += self.jump_count

        self.handle_collision()

        self.old_y = self.rect.y

    def is_collision(self, collision_list):
        for platform in collision_list:
            rect = platform.rect
            if self.rect.colliderect(rect):
                # Check whether the player hits the platform with its bottom
                bottom_rect_list = [(self.rect.bottomleft[0] + x, self.rect.midbottom[1]) for x in range(self.rect.w)]
                for point in bottom_rect_list:
                    if rect.collidepoint(point[0], point[1]):
                        # Check whether the player hits it when going down not down
                        if self.old_y < self.rect.y:
                            return rect

    def jump(self):
        self.is_jump = True
        self.reset_jump_count()

    def reset_gravity(self): self.gravity = 0

    def apply_gravity(self):
        self.rect.y += self.gravity
        self.gravity += 0.4

    def draw_score(self):
        font = pygame.font.SysFont("comicsans", 30)
        txt = font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(txt, (0, 0))

    def draw(self):
        self.draw_score()
        screen.blit(self.image, (self.rect.x, self.rect.y))

        if not self.rect.x + self.rect.w < WIDTH:
            screen.blit(self.image, (self.rect.x - WIDTH, self.rect.y))
            # Logic to make it seem like it spawns in the other part of screen when it crosses the border in right
            if self.rect.x >= WIDTH:
                self.rect.x = self.rect.x - WIDTH
        if not 0 < self.rect.x:
            screen.blit(self.image, (WIDTH + self.rect.x, self.rect.y))
            # Logic to make it seem like it spawns in the other part of screen when it crosses the border in left
            if self.rect.x + self.rect.w <= 0:
                self.rect.x = WIDTH + self.rect.x


class Platform:
    def __init__(self, iter_index, y=None):
        width, height = 50, 15
        self.image = pygame.transform.scale(pygame.image.load("assets/platform.png"), (width, height))
        self.rect = self.image.get_rect()

        if not y:
            y = platforms_list[iter_index-1].rect.y - random.randint(80, 120)

        self.rect.x, self.rect.y = random.randint(0, WIDTH-width), y

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


# Functions
random_color = lambda a, b: tuple(random.randint(a, b) for _ in range(3))


def draw_loosing():
    screen.fill(PSEUDO_WHITE)

    font = pygame.font.SysFont("comicsans", 60)
    loosing_txt = font.render("YOU LOST!", True, BLACK)

    font = pygame.font.SysFont("comicsans", 30)
    score_txt = font.render(f"Score: {player.score}", True, BLACK)
    highest_score_txt = font.render(f"Highest Score: {player.highest_score}", True, BLACK)

    screen.blit(loosing_txt, ((WIDTH - loosing_txt.get_width())/2, (HEIGHT - loosing_txt.get_height())/2))
    screen.blit(score_txt, ((WIDTH - score_txt.get_width())/2, HEIGHT*(7/12)))
    screen.blit(highest_score_txt, ((WIDTH - highest_score_txt.get_width())/2, HEIGHT*(2/3)))

    pygame.display.flip()


def draw_choice():
    screen.fill(PSEUDO_WHITE)

    font = pygame.font.SysFont("comicsans", 60)
    wlcm_txt = font.render("WELCOME TO", True, BLACK)
    game_name_txt = font.render(pygame.display.get_caption()[0], True, random_color(0, 255))
    game_txt = font.render("GAME", True, BLACK)

    screen.blit(wlcm_txt, ((WIDTH - wlcm_txt.get_width())/2, HEIGHT/4))
    screen.blit(game_name_txt, ((WIDTH - game_name_txt.get_width())/2, HEIGHT*(11/24)))
    screen.blit(game_txt, ((WIDTH - game_txt.get_width())/2, HEIGHT*(2/3)))

    pygame.display.flip()


def draw_screen():
    screen.blit(bg_image, (0, 0))

    for platform in platforms_list:
        platform.draw()

    player.draw()

    pygame.display.flip()


# Vars
platforms_list = [Platform(0, y=HEIGHT-30)]
for i in range(8):
    platforms_list.append(Platform(i+1))

# Instances
lower_platform = platforms_list[0]
for platform in platforms_list:
    if platform.rect.y > lower_platform.rect.y:
        lower_platform = platform
player = Player(lower_platform.rect.x, lower_platform.rect.y)
player.rect.centerx = lower_platform.rect.centerx

# Mainloop
is_started = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and not is_started:
            is_started = True

    if not is_started:
        draw_choice()
        continue

    player.handle_movement()

    # Effect that everything goes down
    if player.rect.y < HEIGHT // 3:
        player.rect.y += 5
        player.score += 1
        for platform in platforms_list:
            platform.rect.y += 5

    # Delete platforms that are outta screen
    delete_platforms = []
    for platform in platforms_list:
        if platform.rect.y >= HEIGHT:
            delete_platforms.append(platform)
            # Append a new Platform() to create illusion that we are going up
            platforms_list.append(Platform(len(platforms_list)))
    for platform in delete_platforms:
        if platform in platforms_list:
            platforms_list.pop(platforms_list.index(platform))

    draw_screen()

    # Check case of loosing
    if player.rect.centery >= HEIGHT:
        player.highest_score = max(player.score, player.highest_score)

        draw_loosing()
        pygame.time.wait(3000)
        is_started = False

        lower_platform = platforms_list[0]
        for platform in platforms_list:
            if platform.rect.y > lower_platform.rect.y:
                lower_platform = platform
        player.rect.centerx = lower_platform.rect.centerx
        player.rect.y = lower_platform.rect.y - player.size

        player.reset_gravity()
        player.is_jump = False
        player.reset_jump_count()

        player.score = 0

# FINISHED IN 22/04/2022
# Pretty Easy by the way
