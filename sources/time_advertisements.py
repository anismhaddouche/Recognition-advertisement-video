import cv2
from datetime import datetime
from tqdm import tqdm





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
channel_frame = cv2.imread("../Frames_channels/ENTV_1.jpg")
channel_frame = cv2.cvtColor(channel_frame, cv2.COLOR_BGR2GRAY)
_, descriptor_channel_frame = orb.detectAndCompute(channel_frame, None)
treshold_start = [0]
f = open("../time_adversitements.txt","w")
i=1
pbar = tqdm(total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
while True:
    # print("Reading...")
    pbar.update(i)
    _, current_frame = cap.read()
    current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    _, descriptor_current_frame = orb.detectAndCompute(current_frame, None)
    cv2.imshow('frame', current_frame)
    if cv2.waitKey(int(cap.get(cv2.CAP_PROP_FPS))) & 0xFF == ord('q'):
        break
    _, ts = found_match(descriptor_channel_frame, descriptor_current_frame)
    treshold_start.append(ts)
    Found_s = treshold_start[-1] - treshold_start[-2]
    # print(Found_s)
    if Found_s < -0.80:
        print(datetime.now())
        f.write(str(datetime.now()))
        f.write('\n')
cap.release()
