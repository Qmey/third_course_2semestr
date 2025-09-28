import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sprite Animation")

sprite_images = [
    pygame.image.load('sprite_pose1.png'),
    pygame.image.load('sprite_pose2.png'),
    pygame.image.load('sprite_pose3.png'),
    pygame.image.load('sprite_pose4.png'),
    pygame.image.load('sprite_pose5.png'),
    pygame.image.load('sprite_pose6.png'),
    pygame.image.load('sprite_pose7.png'),
    pygame.image.load('sprite_pose8.png')
]

current_pose = 0
sprite_rect = sprite_images[current_pose].get_rect()

sprite_speed_x, sprite_speed_y = 5, 5

running = True
while running:
    screen.fill((0, 0, 0))

    sprite_rect.x += sprite_speed_x
    sprite_rect.y += sprite_speed_y

    if sprite_rect.right > WIDTH or sprite_rect.left < 0:
        sprite_speed_x = -sprite_speed_x

    if sprite_rect.bottom > HEIGHT or sprite_rect.top < 0:
        sprite_speed_y = -sprite_speed_y

    screen.blit(sprite_images[current_pose], sprite_rect)

    current_pose = (current_pose + 1) % len(sprite_images)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    pygame.time.Clock().tick(24)

pygame.quit()
