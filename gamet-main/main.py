import pygame
from game_manager import launch_game

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Face Game Hub")

WHITE = (255, 255, 255)
GRAY = (30, 30, 30)
LIGHT_GRAY = (100, 100, 100)
BLUE = (0, 150, 255)

font = pygame.font.SysFont(None, 48)

games = [
    {"title": "Ping Pong", "module": "face_pong"},
    {"title": "Snake", "module": "face_snake"},
    {"title": "Flappy Bird", "module": "flappy_bird"},
    {"title": "Look-Alike", "module": "look_alike"},
]

button_height = 70
button_width = 400
button_margin = 20
start_y = 150

def draw_button(text, x, y, hovered):
    color = LIGHT_GRAY if hovered else WHITE
    pygame.draw.rect(screen, color, (x, y, button_width, button_height), border_radius=10)
    label = font.render(text, True, GRAY)
    label_rect = label.get_rect(center=(x + button_width // 2, y + button_height // 2))
    screen.blit(label, label_rect)

running = True
while running:
    screen.fill(GRAY)

    title = font.render("Game Hub", True, BLUE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    mouse_pos = pygame.mouse.get_pos()
    mouse_click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_click = True

    for index, game in enumerate(games):
        x = WIDTH // 2 - button_width // 2
        y = start_y + index * (button_height + button_margin)
        hovered = x <= mouse_pos[0] <= x + button_width and y <= mouse_pos[1] <= y + button_height

        draw_button(game["title"], x, y, hovered)

        if hovered and mouse_click:
            launch_game(game["module"])

    pygame.display.flip()

pygame.quit()
