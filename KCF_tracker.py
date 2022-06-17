import opencv_camera
import cv2

# Intit tracker
kcf_tracker = cv2.TrackerKCF.create()


video = cv2.VideoCapture("car.mp4")

# Vérification que la vidéo s'est ouverte correctement
if not video.isOpened():
    print("Could not open video")

# Lecture du premier frame
ret, frame = video.read()
if not ret:
    print("Cannot read video file")
else:
    bbox = cv2.selectROI(frame, False)
    if bbox:
        print("bounding box", bbox)
        ok = kcf_tracker.init(frame, bbox)

video.release()
cv2.destroyAllWindows()