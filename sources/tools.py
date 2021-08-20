import os
import sys


def convert_video(actual_path, new_path, w=640, h=360):
    """Convert to h265, scale and black and white  """
    os.system("ffmpeg -i " + actual_path + "  -c:v libx265 -an -x265-params crf=25 -vf scale=" + str(w) + ":" + str(
        h) + ",format=gray " + new_path + ".mp4")


def accelerate_video(actual_path, new_path, speed=0.5):
    """Accelerate a video """
    os.system("ffmpeg -i " + actual_path + " -vf  setpts="+str(speed)+"*PTS "+ new_path + ".mp4")



