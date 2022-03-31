import cv2
from datetime import timedelta
from datetime import datetime
import ntpath
from tqdm import tqdm
import csv
import sys


def found_match(descriptor_channel_frame, descriptor_current_frame, bf=cv2.BFMatcher(cv2.NORM_HAMMING), thresh=0.80,
                found=False):
    """Check if two image match. Note that in the following the found return is not used """
    # bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(descriptor_channel_frame, descriptor_current_frame, k=2)
    good = []
    for m, n in matches:
        if m.distance < 0.80 * n.distance:
            good.append([m])
    threshold = len(good) / len(descriptor_channel_frame)
    # print(threshold)
    if threshold > thresh:
        # print("similar")
        found = True
    return found, threshold


def csv_write(fields=None, file="../time_ads.csv"):
    """Write in the parameters [Date and current time,video time,frame position,video name, score
        ] when the Jingle appears in a video"""
    if fields is None:
        fields = ["Date and current time", "video time", "frame position", "video name", "score"]
    try:
        with open(file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
            f.close()
    except NameError:
        print("Can't open the CSV file")


def time_ads(path, descriptor):
    """ This is the main function. Take the video path (path) and the descriptor Jingle of the channel as arguments (
    descriptor) """
    orb = cv2.ORB_create(nfeatures=100)
    cap = cv2.VideoCapture(str(path))
    channel_frame = cv2.imread(str(descriptor))
    channel_frame = cv2.cvtColor(channel_frame, cv2.COLOR_BGR2GRAY)
    _, descriptor_channel_frame = orb.detectAndCompute(channel_frame, None)
    threshold_start = [0]
    i = 1
    bar = tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    while True:
        bar.update(i)
        ret, current_frame = cap.read()
        if ret:
            # print(cap.get(cv2.CAP_PROP_FORMAT))
            # print(str(timedelta(seconds=cap.get(cv2.CAP_PROP_POS_MSEC)/1000)), cap.get(cv2.CAP_PROP_POS_FRAMES))
            current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
            _, descriptor_current_frame = orb.detectAndCompute(current_frame, None)
            current_frame = cv2.resize(current_frame, (320, 180))
            cv2.imshow('frame', current_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            _, ts = found_match(descriptor_channel_frame, descriptor_current_frame)
            threshold_start.append(ts)
            Found_s = threshold_start[-1] - threshold_start[-2]
            # print(Found_s)
            if Found_s < -0.35:
                field = [str(datetime.now()), str(timedelta(seconds=cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)),
                         str(cap.get(cv2.CAP_PROP_POS_FRAMES)), str(ntpath.basename(path)), str(Found_s)]
                print(field)
                csv_write(field)
        else:
            print("Finish reading")
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    time_ads(*sys.argv[1:])

# usage : python3 time_advertisements.py ../Videos/test_resized.ts ../Frames_channels/ENTV.jpg
