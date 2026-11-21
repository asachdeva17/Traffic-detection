
import cv2  
import numpy as np

INTERVAL_SECONDS = 10
LOW_MAX = 3
MEDIUM_MAX = 7
MIN_AREA=150
VIDEO_FILE = "sampleVideo.mp4"  
video = cv2.VideoCapture(VIDEO_FILE)
ROAD_POLYGON = [(0.51, 0.38), (0.60, 0.38), (0.76, 1.0), (0.39, 1.0)]

def congestion_level(average):
    if average <= LOW_MAX:
        return "Low"
    elif average <= MEDIUM_MAX:
        return "Medium"
    return "High"

class IntervalResult:
    def __init__(self, start_time, end_time, average_count):
        self.start_time = start_time
        self.end_time = end_time
        self.average_count = average_count
        self.level = congestion_level(average_count)


class TrafficReport:
    def __init__(self, video_path, interval_seconds):
        self.video_path = video_path
        self.interval_seconds = interval_seconds
        self.intervals = []

    def add_interval(self, start_time, end_time, counts):
        average = sum(counts) / len(counts)
        self.intervals.append(IntervalResult(start_time, end_time, average))

    def overall_level(self):
        averages = [r.average_count for r in self.intervals]
        return congestion_level(sum(averages) / len(averages))

if not video.isOpened():
    print("Could not open the video:", VIDEO_FILE)
    print("Check the file name and that it is in the same folder as this script.")
    raise SystemExit

subtractor = cv2.createBackgroundSubtractorMOG2()
brush = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
frame_number = 0
fps = video.get(cv2.CAP_PROP_FPS)
if fps <= 0:
    fps = 30
frames_per_interval = int(fps * INTERVAL_SECONDS)
report = TrafficReport(VIDEO_FILE, INTERVAL_SECONDS)
interval_counts = []

while True:
    success, frame = video.read() 
    if not success:  
            break
    frame_number += 1
    frame = cv2.resize(frame, (960, 540))
    frame = cv2.resize(frame, (960, 540))
    height, width = frame.shape[:2]
    points = np.array([(int(x * width), int(y * height)) for x, y in ROAD_POLYGON], np.int32)
    

    mask = subtractor.apply(frame)
    road_mask = np.zeros(mask.shape, np.uint8)
    cv2.fillPoly(road_mask, [points], 255)
    mask = cv2.bitwise_and(mask, road_mask)
    _, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, brush)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, brush)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    vehicle_count = 0
    for contour in contours:
        if cv2.contourArea(contour) > MIN_AREA:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            vehicle_count += 1

    if frame_number > 30:
        interval_counts.append(vehicle_count)

    if frame_number % frames_per_interval == 0 and interval_counts:
        start_time = len(report.intervals) * INTERVAL_SECONDS
        end_time = frame_number / fps
        report.add_interval(start_time, end_time, interval_counts)
        interval_counts = []

    cv2.putText(frame, "Vehicles: " + str(vehicle_count), (10, 30),
    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    if report.intervals:
        cv2.putText(frame, "Level: " + report.intervals[-1].level, (10, 65),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.polylines(frame, [points], True, (0, 255, 255), 2)
    cv2.imshow("Original video", frame)
    cv2.imshow("Moving objects (mask)", mask)



    key = cv2.waitKey(30)
    if key == ord("q"):
        break
    elif key == ord(" "):
        cv2.waitKey(5000)     

video.release()
cv2.destroyAllWindows()
print("Done.")
print("FPS:", fps, "Frames per interval:", frames_per_interval)