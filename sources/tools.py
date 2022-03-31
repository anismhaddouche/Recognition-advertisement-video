import os
import cv2
import subprocess
import requests

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
    

def record_live_stream(link, name):
     """ Record from a iptv link   """
     os.system("ffmpeg  -i    " + link + "  -c:v copy " + name)


def cut_video(video_in, video_out, start, end):
    os.system("ffmpeg -i " + video_in + " -ss " + start  + " -to " + end + " -async 1 -c copy  " + video_out)


resize_frame("/Users/anis/PycharmProjects/TV-Advertisements-Detection/Frames_channels/ENTV_MARS_22.png",
             "/Users/anis/PycharmProjects/TV-Advertisements-Detection/Frames_channels/ENTV_MARS_22_resized.png", size=(320, 180), write=True)




#
# def ssh_connection():
#     token = requests.get("curl 'https://token.kube.easybroadcast.fr/authtoken?url=http://apphta.easybroadcast.fr/apphta' \
#   -H 'Connection: keep-alive' \
#   -H 'Pragma: no-cache' \
#   -H 'Cache-Control: no-cache' \
#   -H 'sec-ch-ua: "Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36' \
#   -H 'Accept: /' \
#   -H 'Origin: https://www.htatv.com/' \
#   -H 'Sec-Fetch-Site: cross-site' \
#   -H 'Sec-Fetch-Mode: cors' \
#   -H 'Sec-Fetch-Dest: empty' \
#   -H 'Referer: https://www.htatv.com/' \
#   -H 'Accept-Language: fr' \
#   --compressed")
#     print(token)
# ssh_connection()
