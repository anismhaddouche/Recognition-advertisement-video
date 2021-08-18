import cv2
from datetime import timedelta
from datetime import datetime
import ntpath
from tqdm import tqdm
import csv
import sys

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


def csv_write(fields=['first', 'second', 'third', 'forth', 'fifth'], file="../time_adversitements.csv"):
    with open(file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)

def time_ads(path, descriptor):
    orb = cv2.ORB_create(nfeatures=100)
    cap = cv2.VideoCapture(str(path))
    channel_frame = cv2.imread(str(descriptor))
    channel_frame = cv2.cvtColor(channel_frame, cv2.COLOR_BGR2GRAY)
    _, descriptor_channel_frame = orb.detectAndCompute(channel_frame, None)
    treshold_start = [0]
    i = 1
    pbar = tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    while True:
        pbar.update(i)
        ret, current_frame = cap.read()
        if ret == True:
            # print(str(timedelta(seconds=cap.get(cv2.CAP_PROP_POS_MSEC)/1000)), cap.get(cv2.CAP_PROP_POS_FRAMES))
            current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
            _, descriptor_current_frame = orb.detectAndCompute(current_frame, None)
            # cv2.imshow('frame', current_frame)
            # if cv2.waitKey(int(cap.get(cv2.CAP_PROP_FPS))) & 0xFF == ord('q'):
            #     break
            _, ts = found_match(descriptor_channel_frame, descriptor_current_frame)
            treshold_start.append(ts)
            Found_s = treshold_start[-1] - treshold_start[-2]
            # print(Found_s)
            if Found_s < -0.80:
                field = [str(datetime.now()), str(timedelta(seconds=cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)),str(cap.get(cv2.CAP_PROP_POS_FRAMES)),str(ntpath.basename(path))]
                print(field)
                csv_write(field)
        else:
            print("Finish reading")
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # Map command line arguments to function arguments.
    time_ads(*sys.argv[1:])