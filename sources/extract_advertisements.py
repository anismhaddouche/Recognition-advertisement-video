import cv2
import sys
import time
from tqdm import tqdm
from datetime import datetime
from datetime import timedelta


def found_match(descriptor_channel_frame, descriptor_current_frame, bf=cv2.BFMatcher(cv2.NORM_HAMMING), thresh=0.80,
                found=False):
    threshold = 0
    try:
        matches = bf.knnMatch(descriptor_channel_frame, descriptor_current_frame, k=2)
        good = []
        for m, n in matches:
            if m.distance < 0.80 * n.distance:
                good.append([m])
        threshold = len(good) / len(descriptor_channel_frame)
        if threshold > thresh:
            # print("similar")
            found = True
            # print(threshold)
    except (TypeError, cv2.error):
        print("Error in the  found_match function")
        pass
    return found, threshold


def des_current_frame(current_frame):
    orb = cv2.ORB_create(nfeatures=100)
    try:
        current_frame = cv2.resize(current_frame, (320, 180))
        current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        _, descriptor_current_frame = orb.detectAndCompute(current_frame, None)
        return descriptor_current_frame, current_frame
    except cv2.error:
        print("Error in des_current_frame function")


def capture_video(path_video):
    try:
        cap = cv2.VideoCapture(str(path_video))
        frame_size = (int(cap.get(3)), int(cap.get(4)))
        fps = cap.get(cv2.CAP_PROP_FPS)
        return cap, frame_size, fps
    except cv2.error:
        print("Error in read_video function ")


def read_video(cap):
    ret, current_frame = cap.read()
    if ret is False:
        print("Error in read_video function")
    return ret, current_frame


def des_channel_frame(path_channel_frame):
    try:
        orb = cv2.ORB_create(nfeatures=100)
        channel_frame = cv2.cvtColor(cv2.imread(str(path_channel_frame)), cv2.COLOR_BGR2GRAY)
        _, descriptor_channel_frame = orb.detectAndCompute(channel_frame, None)
        return descriptor_channel_frame
    except cv2.error:
        print('Error in des_channel_frame function ')
        pass


def extract_ads(path_video, path_channel_frame):
    """ This is the man function. The input may be note resized to (360, 180)"""
    cap, frame_size, fps = capture_video(str(path_video))
    descriptor_channel_frame = des_channel_frame(str(path_channel_frame))
    nbr = 0
    threshold_start = [0]
    i = 1
    bar = tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    while True:
        bar.update(i)
        ret, current_frame = read_video(cap)
        if ret:
            descriptor_current_frame, current_frame = des_current_frame(current_frame)
            _, ts = found_match(descriptor_channel_frame, descriptor_current_frame)
            threshold_start.append(ts)
            Found_s = threshold_start[-1] - threshold_start[-2]
            cv2.imshow('frame', current_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if Found_s < -0.70:
                output = cv2.VideoWriter("../Recordings/output_" + str(nbr) + "_" + str(
                    timedelta(seconds=cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)) + "_" + str(
                    datetime.now()) + ".mp4",
                                         cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
                                         fps, frame_size)
                threshold_start = [0]
                frame_end = time.perf_counter()
                print(" Start recording number {} with Found_s = {}".format(nbr, Found_s))
                while True:
                    ret, current_frame = read_video(cap)
                    cv2.imshow('frame', current_frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    bar.update(i)
                    output.write(current_frame)
                    descriptor_current_frame, current_frame = des_current_frame(current_frame)
                    _, ts = found_match(descriptor_channel_frame, descriptor_current_frame)
                    threshold_start.append(ts)
                    Found_s = threshold_start[-1] - threshold_start[-2]
                    """Break if the jingle appears if time exceed 15 min = 900sec """
                    if time.perf_counter() - frame_end > 900:
                        print("End not found")
                        nbr = nbr + 1
                        break
                    if Found_s < -0.70:
                        print(" End recording number {}".format(nbr), "Founds_s", Found_s)
                        nbr = nbr + 1
                        break

        else:
            print("Finish reading")
            cap.release()
            cv2.destroyAllWindows()
            break


# Usage : extract_ads("../Videos/test_resized.ts", "../Frames_channels/ENTER.jpg")

if __name__ == '__main__':
    extract_ads(*sys.argv[1:])
