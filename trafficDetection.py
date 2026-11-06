
import cv2  
import numpy as np

VIDEO_FILE = "sample video.mp4"  
video = cv2.VideoCapture(VIDEO_FILE)
ROAD_POLYGON = [(0.51, 0.28), (0.60, 0.28), (0.76, 1.0), (0.39, 1.0)]

if not video.isOpened():
    print("Could not open the video:", VIDEO_FILE)
    print("Check the file name and that it is in the same folder as this script.")
    raise SystemExit

subtractor = cv2.createBackgroundSubtractorMOG2()

while True:
    success, frame = video.read() 
    if not success:  
            break
    frame = cv2.resize(frame, (960, 540))
    height, width = frame.shape[:2]
    points = np.array([(int(x * width), int(y * height)) for x, y in ROAD_POLYGON], np.int32)
    

    mask = subtractor.apply(frame)
    road_mask = np.zeros(mask.shape, np.uint8)
    cv2.fillPoly(road_mask, [points], 255)
    mask = cv2.bitwise_and(mask, road_mask)

    cv2.polylines(frame, [points], True, (0, 255, 255), 2)
    cv2.imshow("Original video", frame)
    cv2.imshow("Moving objects (mask)", mask)

    if cv2.waitKey(30) == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
print("Done.")