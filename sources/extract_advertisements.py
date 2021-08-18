import cv2
import os
import time
from tqdm import tqdm
#
# def extract_frames(path):
#     name = os.path.basename(path)
#     cap = cv2.VideoCapture(path)
#     i = 0
#     while cap.isOpened():  # While the video in opened
#         ret, frame = cap.read()
#         if ret == False:
#             break
#         cv2.imwrite('../Frames/' + str(name) + str(i) + '.jpg', frame)
#         i += 1
#         cv2.imshow("as", frame)
#         ch = 0xFF & cv2.waitKey(1)  # Wait for a second
#         if ch == 27:
#             break
#     cap.release()
#     cv2.destroyAllWindows()


# extract_frames("../Videos/ENTV_1.ts")

def found_match(descriptor_channel_frame, descriptor_current_frame, bf=cv2.BFMatcher(cv2.NORM_HAMMING), thresh=0.80,
                Found=False):
    # bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(descriptor_channel_frame, descriptor_current_frame, k=2)
    good = []
    for m, n in matches:
        if m.distance < 0.80 * n.distance:
            good.append([m])
    threshold = len(good) / len(descriptor_channel_frame)
    if threshold > thresh:
        # print("similar")
        Found = True
        # print(threshold)
    return Found, threshold


orb = cv2.ORB_create(nfeatures=100)
cap = cv2.VideoCapture("../Videos/test.ts")
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_size = (frame_width, frame_height)
fps = cap.get(cv2.CAP_PROP_FPS)
channel_frame = cv2.imread("../Frames_channels/ENTV_1.jpg")
channel_frame = cv2.cvtColor(channel_frame, cv2.COLOR_BGR2GRAY)
_, descriptor_channel_frame = orb.detectAndCompute(channel_frame, None)
nbr = 0
treshold_start = [0]
# sys.stdout.write("Reading...")
# time_start=time.time()
i=1
pbar = tqdm(total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
while True:
    # print("Reading...")
    pbar.update(i)
    _, current_frame = cap.read()
    current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    _, descriptor_current_frame = orb.detectAndCompute(current_frame, None)
    cv2.imshow('frame', current_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    Found, ts = found_match(descriptor_channel_frame, descriptor_current_frame)
    treshold_start.append(ts)
    Found_s = treshold_start[-1] - treshold_start[-2]
    # print(Found_s)
    if Found_s < -0.80:
        output = cv2.VideoWriter("../Recordings/output" + str(nbr) + ".mp4", cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
                                 fps,
                                 frame_size)
        treshold_start = [0]
        print(" Start recording number {}".format(nbr))
        while True:
            # print("recording number {}".format(nbr))
            ret, current_frame = cap.read()
            pbar.update(i)
            output.write(current_frame)
            current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
            _, descriptor_current_frame = orb.detectAndCompute(current_frame, None)
            Found, ts = found_match(descriptor_channel_frame, descriptor_current_frame)
            treshold_start.append(ts)
            Found_s = treshold_start[-1] - treshold_start[-2]
            # print(Found_s)
            cv2.imshow('frame', current_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if Found_s < -0.80:
                print(" End recording number {}".format(nbr))
                nbr = nbr + 1
                break
cap.release()
cv2.destroyAllWindows()