import cv2
import mediapipe as mp

def run():
    cap = cv2.VideoCapture(0)
    mp_face = mp.solutions.face_mesh
    face_mesh = mp_face.FaceMesh(static_image_mode=False)

    ball_x, ball_y = 320, 240
    ball_dx, ball_dy = 6, 6
    paddle_height = 100
    player_y = 200
    score_player = 0
    score_bot = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            for lm in results.multi_face_landmarks[0].landmark:
                nose_y = int(lm.y * h)
                break
            player_y = max(0, min(h - paddle_height, nose_y - paddle_height // 2))

        bot_y = ball_y - paddle_height // 2
        bot_y = max(0, min(h - paddle_height, bot_y))

        ball_x += ball_dx
        ball_y += ball_dy

        if ball_y <= 0 or ball_y >= h:
            ball_dy *= -1

        if ball_x <= 20 and player_y <= ball_y <= player_y + paddle_height:
            ball_dx *= -1

        if ball_x >= w - 30 and bot_y <= ball_y <= bot_y + paddle_height:
            ball_dx *= -1

        if ball_x <= 0:
            score_bot += 1
            ball_x, ball_y = w // 2, h // 2
        elif ball_x >= w:
            score_player += 1
            ball_x, ball_y = w // 2, h // 2

        game_frame = frame.copy()

        cv2.rectangle(game_frame, (10, player_y), (20, player_y + paddle_height), (0, 255, 0), -1)

        cv2.rectangle(game_frame, (w - 20, bot_y), (w - 10, bot_y + paddle_height), (255, 0, 0), -1)

        cv2.circle(game_frame, (ball_x, ball_y), 10, (255, 255, 255), -1)

        cv2.putText(game_frame, f"{score_player} : {score_bot}", (w // 2 - 50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 0), 3)

        cv2.imshow("Face Pong", game_frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run()
