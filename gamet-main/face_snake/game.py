import pygame
import cv2
import mediapipe as mp
import threading
import random
import time

current_direction = (1, 0)


def hand_control_loop():
    global current_direction
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

                finger_tips = [8, 12, 16, 20]
                fingers_up = 0
                lm = handLms.landmark
                for tip in finger_tips:
                    if lm[tip].y < lm[tip - 2].y:
                        fingers_up += 1

                if fingers_up == 0:
                    pass
                elif fingers_up == 1:
                    current_direction = (-1, 0)
                elif fingers_up == 2:
                    current_direction = (1, 0)
                elif fingers_up == 3:
                    current_direction = (0, -1)
                elif fingers_up == 4:
                    current_direction = (0, 1)

        cv2.imshow("Камера — рука", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

        time.sleep(0.03)

    cap.release()
    cv2.destroyAllWindows()


def run():
    global current_direction
    pygame.init()
    cell = 20
    cols, rows = 30, 30
    width, height = cols * cell, rows * cell
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    snake_head_img = pygame.image.load("C:/Users/Yerlan/PycharmProjects/Games/games/face_snake/snake_head1.png")
    snake_body_img = pygame.image.load("C:/Users/Yerlan/PycharmProjects/Games/games/face_snake/snake_body.png")
    apple_img = pygame.image.load("C:/Users/Yerlan/PycharmProjects/Games/games/face_snake/apple.png")

    snake_head_img = pygame.transform.scale(snake_head_img, (cell, cell))
    snake_body_img = pygame.transform.scale(snake_body_img, (cell, cell))
    apple_img = pygame.transform.scale(apple_img, (cell, cell))

    snake = [(cols // 2, rows // 2)]
    direction = (1, 0)
    food = (random.randint(0, cols - 1), random.randint(0, rows - 1))
    score = 0
    speed = 0.15
    last_move = time.time()

    cam_thread = threading.Thread(target=hand_control_loop, daemon=True)
    cam_thread.start()

    def reset_game():
        global current_direction
        nonlocal snake, food, score, direction, last_move
        snake = [(cols // 2, rows // 2)]
        direction = (1, 0)
        food = (random.randint(0, cols - 1), random.randint(0, rows - 1))
        score = 0
        current_direction = (1, 0)
        last_move = time.time()

    running = True
    while running:
        screen.fill((0, 0, 0))

        if current_direction[0] != -direction[0] or current_direction[1] != -direction[1]:
            direction = current_direction

        now = time.time()
        if now - last_move >= speed:
            last_move = now
            new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

            new_head = (new_head[0] % cols, new_head[1] % rows)

            if new_head in snake:
                print("💀 Game Over")
                reset_game()

            snake.insert(0, new_head)

            # Еда
            if new_head == food:
                score += 1
                while food in snake:
                    food = (random.randint(0, cols - 1), random.randint(0, rows - 1))
            else:
                snake.pop()

        for i, (x, y) in enumerate(snake):
            if i == 0:
                screen.blit(snake_head_img, (x * cell, y * cell))
            else:
                screen.blit(snake_body_img, (x * cell, y * cell))

        screen.blit(apple_img, (food[0] * cell, food[1] * cell))

        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Count: {score}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    run()
