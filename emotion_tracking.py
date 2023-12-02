import cv2
import opencv_jupyter_ui as jcv2
from feat import Detector
from IPython.display import Image

from feat.utils import FEAT_EMOTION_COLUMNS


def main():
    # ---------------------------------------------------------------- #
    # Use an OpenCV window to display a live feed of your webcam.
    # When you press SPACE, the program should toggle between "recording" mode and "stopped" mode.
    # * In "stopped" mode, you should only display the live feed, with no modifications.
    # * In "recording" mode, you should display a red circle on the top left corner to show that the mode is active.
    #   You should use the `face_tracker` to find any faces in the current frame, and display
    #   a green rectangle where the detected faces are (draw the outline, not a solid rectangle).

    detector = Detector(device="cpu")

    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    cv2.namedWindow("Emotion Tracking")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("OpenCV found an error reading the next frame.")
            break
 
        faces = detector.detect_faces(frame)
        landmarks = detector.detect_landmarks(frame, faces)
        emotions = detector.detect_emotions(frame, faces, landmarks)
        aus = detector.detect_aus(frame,landmarks)

        faces = faces[0]
        landmarks = landmarks[0]
        emotions = emotions[0]
        aus = aus[0]
        
        display = frame.copy()

        strongest_emotion = emotions.argmax(axis=1)

        for (face, top_emo) in zip(faces, strongest_emotion):
            (x0, y0, x1, y1, p) = face
            cv2.rectangle(display, (int(x0), int(y0)), (int(x1), int(y1)), (255, 0, 0), 3)
            cv2.putText(display, FEAT_EMOTION_COLUMNS[top_emo], (int(x0), int(y0 - 10)), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0), 2)    

        cv2.circle(display, (32, 32), 16, (0, 0, 255), -1)

        cv2.imshow("Emotion Tracking", display)

        key = cv2.waitKey(1) & 0xFF
        if key == 27: # ESC pressed
            break 
        

    cam.release()
    cv2.destroyAllWindows()
    # ---------------------------------------------------------------- #


if __name__ == "__main__":
    main()
