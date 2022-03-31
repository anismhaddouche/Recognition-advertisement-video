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
<<<<<<< HEAD
        cap = cv2.VideoCapture(path_video)
        if not cap:
             print("Failed VideoCapture")
=======
        cap = cv2.VideoCapture(str(path_video))
>>>>>>> 2c2709ebc7fc449f783160abe56d5b1c8f46baf5
        frame_size = (int(cap.get(3)), int(cap.get(4)))
        fps = cap.get(cv2.CAP_PROP_FPS)
        return cap, frame_size, fps
    except cv2.error:
        print("Error in read_video function ")


def read_video(cap):
    ret, current_frame = cap.read()
<<<<<<< HEAD
    # if ret is False:
        # print("No frame founded in  the read_video function")
=======
    if ret is False:
        print("Error in read_video function")
>>>>>>> 2c2709ebc7fc449f783160abe56d5b1c8f46baf5
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


<<<<<<< HEAD
def extract_ads(path_video, path_channel_frame,show_video = False, confidence = 0.30):
    """ This is the man function. The input may be note resized to (360, 180)"""
    start_programme = datetime.now()
    print("The programme started at {}  \n".format(start_programme))

    cap, frame_size, fps = capture_video(path_video)
=======
def extract_ads(path_video, path_channel_frame):
    """ This is the man function. The input may be note resized to (360, 180)"""
    cap, frame_size, fps = capture_video(str(path_video))
>>>>>>> 2c2709ebc7fc449f783160abe56d5b1c8f46baf5
    descriptor_channel_frame = des_channel_frame(str(path_channel_frame))
    nbr = 0
    threshold_start = [0]
    i = 1
    bar = tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    while True:
        bar.update(i)
        ret, current_frame = read_video(cap)
<<<<<<< HEAD

=======
>>>>>>> 2c2709ebc7fc449f783160abe56d5b1c8f46baf5
        if ret:
            descriptor_current_frame, current_frame = des_current_frame(current_frame)
            _, ts = found_match(descriptor_channel_frame, descriptor_current_frame)
            threshold_start.append(ts)
<<<<<<< HEAD
            Found_s = - threshold_start[-1] + threshold_start[-2]
            if show_video == True: 
                cv2.imshow('frame', current_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            if Found_s > confidence:
                print(" Start recording number {} with confidence {}".format(
                    nbr, abs(round(Found_s, 2))))
                writer = cv2.VideoWriter("../Recordings/output_" + str(nbr) + "_" + str(
=======
            Found_s = threshold_start[-1] - threshold_start[-2]
            cv2.imshow('frame', current_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if Found_s < -0.70:
                output = cv2.VideoWriter("../Recordings/output_" + str(nbr) + "_" + str(
>>>>>>> 2c2709ebc7fc449f783160abe56d5b1c8f46baf5
                    timedelta(seconds=cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)) + "_" + str(
                    datetime.now()) + ".mp4",
                                         cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
                                         fps, frame_size)
                threshold_start = [0]
                frame_end = time.perf_counter()
<<<<<<< HEAD
                while True:
                    ret, current_frame = read_video(cap)
                    if show_video == True:
                        cv2.imshow('frame', current_frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    bar.update(i)

                    # w, h,_ = current_frame.shape
                    # print(w,h, frame_size)

                    writer.write(current_frame)
                    descriptor_current_frame, current_frame = des_current_frame(current_frame)
                    _, ts = found_match(descriptor_channel_frame, descriptor_current_frame)
                    threshold_start.append(ts)
                    Found_s = - threshold_start[-1] + threshold_start[-2]
                    """Break if the jingle does not appears where time exceed 15 min = 900sec """
=======
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
>>>>>>> 2c2709ebc7fc449f783160abe56d5b1c8f46baf5
                    if time.perf_counter() - frame_end > 900:
                        print("End not found")
                        nbr = nbr + 1
                        break
<<<<<<< HEAD
                    if Found_s > confidence:
                        print(" End recording number {} with confidence {}".format(nbr, abs(round(Found_s,2))))
                        nbr = nbr + 1
                        # writer.release()
                        break

        else:
            time.sleep(10)
            End_programme = datetime.now()
            print("\nThe programme finished at {}".format(End_programme))
            print("Duration of the execution {} ".format(
                End_programme - start_programme ))
            cap.release()
            cv2.destroyAllWindows()
            # break
if __name__ == '__main__':
    extract_ads(*sys.argv[1:])
                

# # Usage 
# ENTV : http://aptv.one:8000/live/899606913121352/1593574628/191.ts
# extract_ads("/Users/anis/PycharmProjects/TV-Advertisements-Detection/Videos/test_resized.ts",
            # "/Users/anis/PycharmProjects/TV-Advertisements-Detection/Frames_channels/ENTV.jpg", show_video=False)
=======
                    if Found_s < -0.70:
                        print(" End recording number {}".format(nbr), "Founds_s", Found_s)
                        nbr = nbr + 1
                        break

        else:
            print("Finish reading")
            cap.release()
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    extract_ads(*sys.argv[1:])

# Usage : extract_ads("../Videos/test_resized.ts", "../Frames_channels/ENTER.jpg")
>>>>>>> 2c2709ebc7fc449f783160abe56d5b1c8f46baf5
