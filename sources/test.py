import numpy as np
import cv2
from tqdm import tqdm

cap = cv2.VideoCapture("../Videos/test.ts")
# outcap = cv2.VideoWriter("output.MP4",     cv2.VideoWriter_fourcc('H','2','6','4'), 30, (int(cap.get(3)),int(cap.get(4))))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(int(cap.get(3)),int(cap.get(4)))
print("total frames :",frame_count)

i = 1
pbar = tqdm(total = frame_count)
while cap.isOpened():
    pbar.update(i)
    ret, frame = cap.read()
    if frame is None:
       print('completed...!')
       break
cap.release()
cap.release()