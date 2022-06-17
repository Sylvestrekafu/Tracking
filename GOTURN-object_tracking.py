import cv2
import os
import sys

# init tracker
Goturn_tracker = cv2.TrackerGOTURN_create()


video = cv2.VideoCapture("movie.mp4")
if  not (os.path.isfile('goturn.caffemodel') and os.path.isfile('goturn.prototxt')):
    errorMsg = '''
    Could not find GOTURN model in current directory.
    Please ensure goturn.caffemodel and goturn.prototxt are in the current directory
    '''

if not video.isOpened():
    print("Could not open video")

    #read the first frame

ret, frame =video.read()
frame =cv2.resize(frame,(1280,720),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)


if not ret:
    print("Cannot read video file")
else:
    bbox = cv2.selectROI(frame,False)
    x0, y0 , x1,y1 = bbox
    print("valeur de xo:",x0)
    print("**************************")
    print("valeur de yo:", y0)
    print("**************************")
    print("valeur de x1:", x1)
    print("**************************")
    print("valeur de y1:", y1)

    #box =(x0,y0, x1,y1)
    if bbox:
        print("Bonding box", bbox)
        ok =Goturn_tracker.init(frame, bbox)


video.release()
cv2.destroyAllWindows()


video = cv2.VideoCapture("movie.mp4")

# Vérification que la vidéo s'est ouverte correctement
if not video.isOpened():
    print("Could not open video")

# Boucler jusqu'à ce que l'utilisateur arrête la vidéo, ou que la vidéo se termine
while True:
    ret, frame = video.read()
    frame = cv2.resize(frame, (1280, 720), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
    if not ret:
        print("Cannot read video file")
        break

    # Démarrer le timer
    timer = cv2.getTickCount()

    # Mettre à jour le tracker
    ok, bbox = Goturn_tracker.update(frame)

    # Calculer les Frames per second (FPS)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

    # Dessiner le rectangle englobant
    if ok:
        # Le suivi a réussi
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        print("bounding 0:",(bbox[0]))
        print(("********"))
        print("Bounding box 1:",bbox[1])

        print(("***********$$$$$$$$$"))
        print(p1)
        print("$$$$$$$$$$$$$")
        print(p2)

    else:
        # Le suivi a échoué
        cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    # Afficher le type de tracker sur l'image
    #cv2.putText(frame, "GoturnTracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

    # Afficher aussi le FPS
    cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

    # Afficher le résultat
    cv2.imshow("Tracking", frame)

    # Arrêter si la touche 'escape' est pressée
    k = cv2.waitKey(1) & 0xff

    if k == 27: break

video.release()

cv2.destroyAllWindows()