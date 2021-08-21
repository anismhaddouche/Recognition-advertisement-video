import cv2
import os
import time
from tqdm import tqdm
from datetime import datetime
from datetime import timedelta


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
# cap = cv2.VideoCapture("../Videos/test_resized.ts")
cap=cv2.VideoCapture("http://aptv.one:80/live/899606913121352/1593574628/50508.ts")
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_size = (frame_width, frame_height)
fps = cap.get(cv2.CAP_PROP_FPS)
channel_frame = cv2.imread("../Frames_channels/ENTV.jpg")
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
    ret, current_frame = cap.read()
    current_frame = cv2.resize(current_frame, (320, 180))
    current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    _, descriptor_current_frame = orb.detectAndCompute(current_frame, None)
    cv2.imshow('frame', current_frame)
    Found, ts = found_match(descriptor_channel_frame, descriptor_current_frame)
    treshold_start.append(ts)
    Found_s = treshold_start[-1] - treshold_start[-2]
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # print(Found_s)
    if Found_s < -0.40:
        output = cv2.VideoWriter("../Recordings/output_" + str(nbr) + "_" +str(timedelta(seconds=cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)) +"_"+ str(datetime.now())+ ".mp4", cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
                                 fps,
                                 frame_size)
        treshold_start = [0]
        frame_end = time.perf_counter()
        print(" Start recording number {}".format(nbr),"Founds_s",Found_s)
        while True:
            # print("recording number {}".format(nbr))
            ret, current_frame = cap.read()
            pbar.update(i)
            output.write(current_frame)
            current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
            current_frame = cv2.resize(current_frame, (320, 180))
            _, descriptor_current_frame = orb.detectAndCompute(current_frame, None)
            Found, ts = found_match(descriptor_channel_frame, descriptor_current_frame)
            treshold_start.append(ts)
            Found_s = treshold_start[-1] - treshold_start[-2]
            # print(Found_s)
            cv2.imshow('frame', current_frame)
            if time.perf_counter()-frame_end>900:
                print("End not found")
                nbr = nbr + 1
                break
            if Found_s < -0.40:
                print(" End recording number {}".format(nbr),"Founds_s",Found_s)
                nbr = nbr + 1
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
cap.release()
cv2.destroyAllWindows()