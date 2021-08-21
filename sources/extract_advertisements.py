import cv2
import sys
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


def exctract_ads(path_video, path_channel_frame):
    orb = cv2.ORB_create(nfeatures=100)
    # cap = cv2.VideoCapture("../Videos/test_resized.ts")
    cap = cv2.VideoCapture(str(path_video))
    frame_size = (int(cap.get(3)), int(cap.get(4)))
    fps = cap.get(cv2.CAP_PROP_FPS)
    channel_frame = cv2.cvtColor(cv2.imread(str(path_channel_frame)), cv2.COLOR_BGR2GRAY)
    _, descriptor_channel_frame = orb.detectAndCompute(channel_frame, None)
    nbr = 0
    treshold_start = [0]
    i = 1
    pbar = tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    while True:
        pbar.update(i)
        ret, current_frame = cap.read()
        if ret:
            current_frame = cv2.resize(current_frame, (320, 180))
            current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
            _, descriptor_current_frame = orb.detectAndCompute(current_frame, None)
            Found, ts = found_match(descriptor_channel_frame, descriptor_current_frame)
            treshold_start.append(ts)
            Found_s = treshold_start[-1] - treshold_start[-2]
            # cv2.imshow('frame', current_frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
            if Found_s < -0.40:
                output = cv2.VideoWriter("../Recordings/output_" + str(nbr) + "_" + str(
                    timedelta(seconds=cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)) + "_" + str(datetime.now()) + ".mp4",
                                         cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
                                         fps, frame_size)
                treshold_start = [0]
                frame_end = time.perf_counter()
                print(" Start recording number {} with Found_s = {}".format(nbr,Found_s))
                while True:
                    ret, current_frame = cap.read()
                    pbar.update(i)
                    output.write(current_frame)
                    current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
                    current_frame = cv2.resize(current_frame, (320, 180))
                    _, descriptor_current_frame = orb.detectAndCompute(current_frame, None)
                    Found, ts = found_match(descriptor_channel_frame, descriptor_current_frame)
                    treshold_start.append(ts)
                    Found_s = treshold_start[-1] - treshold_start[-2]
                    if time.perf_counter() - frame_end > 900:
                        print("End not found")
                        nbr = nbr + 1
                        break
                    if Found_s < -0.40:
                        print(" End recording number {}".format(nbr), "Founds_s", Found_s)
                        nbr = nbr + 1
                        break
                    # cv2.imshow('frame', current_frame)
                    # if cv2.waitKey(1) & 0xFF == ord('q'):
                    #     break
        # cap.release()
        # cv2.destroyAllWindows()
        else:
            print("Finish reading")
            break


# exctract_ads("../Videos/test_resized.ts", "../Frames_channels/ENTV.jpg")

if __name__ == '__main__':
    # Map command line arguments to function arguments.
    exctract_ads(*sys.argv[1:])
