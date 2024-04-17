import cv2
import Hand_Tracking2 as htm
import time
import numpy as np
import cvzone
from pynput.keyboard import Controller, Key


# def drawALL(img, buttonList):
#
#     for button in buttonList:
#         x, y = button.pos
#         w, h = button.size
#
#         cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
#         cv2.putText(img, button.text, (x + 20, y + 65),
#         cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
#
#     return img

def drawAll(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.pos
        cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
                      (255, 0, 255), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x + 40, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)

    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    print(mask.shape)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text



def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1920)
    cap.set(4, 1080)

    detector = htm.handDetector(maxHands=1)

    finaltext = ""
    keyboard = Controller()



    keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
            ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
            ]

    buttonList = []

    buttonList.append(Button([900, 350], "Backspace", size=[250, 85]))



    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):

            buttonList.append(Button([125 * j + 50, 100 * i + 50], key))
    while True:
        success, img = cap.read()
        hands = detector.findHands(img)
        lmList = detector.findPosition(img)

        img = drawAll(img, buttonList)

        if lmList:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                if x < lmList[8][1] < x + w and y < lmList[8][2] < y + h:
                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                    # When cliked
                    l = detector.distance_between_fingers(img, p1=8, p2=12, pp1=1, pp2=1, pp3=2, pp4=2, draw=False)
                    print(l)

                    if l < 50:
                        if button.text == "Backspace":
                            finaltext = finaltext[:-1]  # usuń ostatnią literę
                            keyboard.press(Key.backspace)  # symuluj wciśnięcie klawisza backspace
                            keyboard.release(Key.backspace)
                        else:
                            keyboard.press(button.text)
                            finaltext += button.text


                        cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        time.sleep(0.15)


        cv2.rectangle(img, (200, 350), (700, 450), (175, 0, 175), cv2.FILLED)
        cv2.putText(img, finaltext, (200, 430),
                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)



        cv2.imshow("Image", img)
        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()




if __name__ == '__main__':
    main()

