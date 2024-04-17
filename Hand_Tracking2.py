import cv2
import mediapipe as mp
import time
import math


class handDetector():
    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplex = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):

        self.lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy, = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                self.lmList.append([id, cx, cy])
                # if draw:
                #     if id == 8:
                #         cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                # if id == 12:
                #     cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        return self.lmList

    def distance_between_fingers(self, img, p1, p2, pp1, pp2, pp3, pp4, draw=True):
        print(self.lmList[p1], self.lmList[p2])

        x1, y1 = self.lmList[p1][pp1], self.lmList[p1][pp3]
        x2, y2 = self.lmList[p2][pp2], self.lmList[p2][pp4]
        cx, cy = (x1 + x2) // 2, (y1 + y1) // 2

        if draw == True:

            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 5)
            cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        return length


def main():
    pTime = 0
    cTime = 0

    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)

        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[8])

            detector.distance_between_fingers(img, p1=8, p2=12, pp1=1, pp2=1, pp3=2, pp4=2, draw=False)

        # fps
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255))
        # fps

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
