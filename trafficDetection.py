
import cv2  
import numpy as np

MIN_AREA=300
VIDEO_FILE = "sampleVideo.mp4"  
video = cv2.VideoCapture(VIDEO_FILE)
ROAD_POLYGON = [(0.51, 0.38), (0.60, 0.38), (0.76, 1.0), (0.39, 1.0)]

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

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    vehicle_count = 0
    for contour in contours:
        if cv2.contourArea(contour) > MIN_AREA:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            vehicle_count += 1

    cv2.putText(frame, "Vehicles: " + str(vehicle_count), (10, 30),
    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.polylines(frame, [points], True, (0, 255, 255), 2)
    cv2.imshow("Original video", frame)
    cv2.imshow("Moving objects (mask)", mask)



    key = cv2.waitKey(30)
    if key == ord("q"):
        break
    elif key == ord(" "):
        cv2.waitKey(5000)      # freeze for 5000 ms = 5 seconds, then carry on

video.release()
cv2.destroyAllWindows()
print("Done.")