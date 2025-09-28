import pygame
import cv2
import mediapipe as mp
import threading
import time
import random

jump_signal = False

def hand_control_loop():
    global jump_signal
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            lm = hand.landmark

            if lm[8].y < lm[6].y:
                jump_signal = True

        cv2.imshow("Камера — рука", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def run():
    global jump_signal
    pygame.init()
    WIDTH, HEIGHT = 500, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    bird_x = 100
    bird_y = HEIGHT // 2
    bird_radius = 20
    velocity = 0
    gravity = 0.5
    jump_strength = -10

    pipe_width = 80
    gap = 200
    pipe_x = WIDTH
    pipe_height = random.randint(100, HEIGHT - gap - 100)

    score = 0
    font = pygame.font.SysFont(None, 48)

    cam_thread = threading.Thread(target=hand_control_loop, daemon=True)
    cam_thread.start()

    def reset():
        nonlocal bird_y, velocity, pipe_x, pipe_height, score
        bird_y = HEIGHT // 2
        velocity = 0
        pipe_x = WIDTH
        pipe_height = random.randint(100, HEIGHT - gap - 100)
        score = 0

    running = True
    while running:
        screen.fill((135, 206, 235))

        if jump_signal:
            velocity = jump_strength
            jump_signal = False

        velocity += gravity
        bird_y += velocity

        pipe_x -= 5
        if pipe_x < -pipe_width:
            pipe_x = WIDTH
            pipe_height = random.randint(100, HEIGHT - gap - 100)
            score += 1

        bird_rect = pygame.Rect(bird_x - bird_radius, bird_y - bird_radius, bird_radius * 2, bird_radius * 2)
        top_pipe = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
        bottom_pipe = pygame.Rect(pipe_x, pipe_height + gap, pipe_width, HEIGHT)

        if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe) or bird_y > HEIGHT or bird_y < 0:
            reset()

        pygame.draw.circle(screen, (255, 255, 0), (bird_x, int(bird_y)), bird_radius)
        pygame.draw.rect(screen, (34, 139, 34), top_pipe)
        pygame.draw.rect(screen, (34, 139, 34), bottom_pipe)

        score_text = font.render(f"Count: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run()
