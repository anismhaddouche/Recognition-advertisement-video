import cv2
'path = "http://aptv.one:80/live/899606913121352/1593574628/50508.ts "'
path= '/home/anis/PycharmProjects/TV-Advertisements-Detection/Recordings/output_1_0:02:07.400000_2021-08-25 14:06:02.391885.mp4'
cap = cv2.VideoCapture(path)
while True :
    ret, current_frame = cap.read()
    while current_frame is None:
        try:
            print("triying to get a frame")
            current_frame = cap.read(path)
        except:
            pass
    if ret:
        """ Do something"""
        cv2.imshow('frame', current_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("Finish reading ")
        break