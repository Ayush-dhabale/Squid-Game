import cv2
import time
import tkinter as tk
from functools import partial

cap = cv2.VideoCapture(0)

fgbg = cv2.createBackgroundSubtractorMOG2()
motion_threshold = 5000

video = cv2.VideoCapture('squidgame2.mp4')

root = tk.Tk()
root.title("Game Over")
root.geometry("400x400")

result_label = tk.Label(root, font=("Arial", 24))
result_label.pack(pady=20)

score_label = tk.Label(root, font=("Arial", 18))
score_label.pack()

def restart_program(window):
    window.destroy()
    cap.release()
    video.release()
    cv2.destroyAllWindows()
    exec(open(__file__).read())

play_again_button = tk.Button(root, text="Play Again", font=("Arial", 14))
play_again_button.configure(command=partial(restart_program, root))
play_again_button.pack(pady=10)

start_time = time.time()
lose_flag = False

while True:
    _, frame = cap.read()

    video_frame_timestamp = video.get(cv2.CAP_PROP_POS_MSEC)

    ret, video_frame = video.read()
    if not ret:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, video_frame = video.read()

    fgmask = fgbg.apply(frame)

    motion_pixels = cv2.countNonZero(fgmask)

    if video_frame_timestamp >= 1200 and video_frame_timestamp <= 1450 and motion_pixels > motion_threshold:
        lose_flag = True

    video_frame = cv2.resize(video_frame, (200, 400))

    video_height, video_width, _ = video_frame.shape

    x = frame.shape[1] - video_width - 10
    y = frame.shape[0] - video_height - 10

    frame[y:y+video_height, x:x+video_width] = video_frame

    cv2.imshow('Frame', frame)

    if lose_flag:
        score = int(time.time() - start_time)

        if score >= 10:
            result_label.config(text="YOU WON!!", fg="green")
            
        else:
            result_label.config(text="YOU LOSE!!", fg="red")
            score_label.config(text=f"Score: {score}")
            result_label.pack()
            score_label.pack()

        
        play_again_button.pack()
        root.update()
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
video.release()
cv2.destroyAllWindows()

root.mainloop()
