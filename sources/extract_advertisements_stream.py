import cv2
import sys
import time
from tqdm import tqdm
from datetime import datetime
from datetime import timedelta


def found_match(descriptor_channel_frame, descriptor_current_frame, bf=cv2.BFMatcher(cv2.NORM_HAMMING), thresh=0.80,
                ):
    found = False
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
        time.sleep(3)
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
        cap = cv2.VideoCapture(path_video)
        if not cap:
             print("Failed VideoCapture")
        frame_size = (int(cap.get(3)), int(cap.get(4)))
        fps = cap.get(cv2.CAP_PROP_FPS)
        return cap, frame_size, fps
    except cv2.error:
        print("Error in read_video function ")


def read_video(cap):
    ret, current_frame = cap.read()
    # if ret is False:
        # print("No frame founded in  the read_video function")
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


def extract_ads_stream(path_video, path_channel_frame,show_video = True, confidence = 0.35):
    """ This is the man function. The input may be note resized to (360, 180)"""
    start_programme = datetime.now()
    print(" \n \n*** The programme started at {}  \n".format(start_programme))

    cap, frame_size, fps = capture_video(path_video)
    descriptor_channel_frame = des_channel_frame(str(path_channel_frame))
    nbr = 0
    threshold_start = [0]
    i = 1
    bar = tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    while True:
        bar.update(i)
        ret, current_frame = read_video(cap)
        while ret == False:
            print("*** Stream connection lost after {}\n*** Trying to reconnect".format(
                datetime.now()-start_programme))
            time.sleep(1)
            cap,_,_ = capture_video(path_video)
            ret, _ = read_video(cap)
            if ret == True:
                print("*** Stream connection established")
                break 

        else: 

            descriptor_current_frame, current_frame = des_current_frame(
                current_frame)
            _, ts = found_match(descriptor_channel_frame,
                                descriptor_current_frame)
            threshold_start.append(ts)
            Found_s = - threshold_start[-1] + threshold_start[-2]
            if show_video == True:
                cv2.imshow('frame', current_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            if Found_s > confidence:
                print("\n*** Start recording number {} with confidence {}".format(
                    nbr, abs(round(Found_s, 2))))
                writer = cv2.VideoWriter("../Recordings/output_" + str(nbr) + "_" + str(
                    timedelta(seconds=cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)) + "_" + str(
                    datetime.now()) + ".mp4",
                    cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
                    fps, frame_size)
                threshold_start = [0]
                frame_end = time.perf_counter()
                while True:
                    ret, current_frame = read_video(cap)
                    if show_video == True:
                        cv2.imshow('frame', current_frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    bar.update(i)
                    writer.write(current_frame)
                    descriptor_current_frame, current_frame = des_current_frame(
                        current_frame)
                    _, ts = found_match(
                        descriptor_channel_frame, descriptor_current_frame)
                    threshold_start.append(ts)
                    Found_s = - threshold_start[-1] + threshold_start[-2]
                    """Break if the jingle does not appears where time exceed 15 min = 900sec """
                    if time.perf_counter() - frame_end > 900:
                        print("*** End not found")
                        nbr = nbr + 1
                        break
                    if Found_s > confidence:
                        print("\n*** End recording number {} with confidence {}".format(
                            nbr, abs(round(Found_s, 2))))
                        nbr = nbr + 1
                        # writer.release()
                        break
                            
                        


            # break
if __name__ == '__main__':
    extract_ads_stream(*sys.argv[1:])


                

# # Usage 
# ENTV : http://aptv.one:8000/live/899606913121352/1593574628/191.ts
# extract_ads("/Users/anis/PycharmProjects/TV-Advertisements-Detection/Videos/test_resized.ts",
            # "/Users/anis/PycharmProjects/TV-Advertisements-Detection/Frames_channels/ENTV.jpg", show_video=False)
