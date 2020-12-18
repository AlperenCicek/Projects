import cv2
import numpy as np
import time

class SlidingImage:
    def __init__(self, x, y, saveName, startPosition = "top"):
        self.x = x
        self.y = y
        self.saveName = saveName
        self.startPosition = startPosition
        self.capture()

    def capture(self):
        if self.startPosition == "top":
            row = 0
        cap = cv2.VideoCapture(0)
        cap.set(3, self.x)
        cap.set(4, self.y)
        tempArray = []

        while(True):
            _, frame = cap.read()
            frameArray = np.array(frame)
            cv2.line(frame, (0, row), (np.size(frameArray, 1), row), (0, 255, 255), 2)
            cv2.imshow("Frame", frame)
            print("0 to", np.size(frameArray, 0), ":", row)
            if row < np.size(frameArray, 0):
                tempArray.append(frameArray[row])
                arr = np.array(tempArray)
                cv2.imshow("Sliding Frame", arr)
                time.sleep(0.05)
                row = row + 1
            else:
                break
            
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break
        cap.release()
        cv2.imshow("Result", arr)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

sample = SlidingImage(640, 360, "top")