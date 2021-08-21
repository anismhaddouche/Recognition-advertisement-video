import os
import cv2


def convert_video(actual_path, new_path, w=320, h=180):
    """Convert to h265, scale and black and white  """
    os.system("ffmpeg -i " + actual_path + "  -c:v libx265 -an -x265-params crf=25 -vf scale=" + str(w) + ":" + str(
        h) + ",format=gray " + new_path + ".mp4")


def accelerate_video(actual_path, new_path, speed=0.5):
    """Accelerate a video """
    os.system("ffmpeg -i " + actual_path + " -vf  setpts=" + str(speed) + "*PTS " + new_path + ".mp4")


def resize_frame(actual_path, new_path, size=(320, 180), write=False):
    frame = cv2.resize(cv2.imread(actual_path), size)
    if write:
        frame = cv2.imwrite(new_path, frame)
    return frame


def extract_frames(path):
    name = os.path.basename(path)
    cap = cv2.VideoCapture(path)
    i = 0
    while cap.isOpened():  # While the video in opened
        ret, frame = cap.read()
        if ret == False:
            break
        cv2.imwrite('../Frames/' + str(name) + str(i) + '.jpg', frame)
        i += 1
        cv2.imshow("as", frame)
        ch = 0xFF & cv2.waitKey(1)  # Wait for a second
        if ch == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
