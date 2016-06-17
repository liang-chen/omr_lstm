
from globv import data_path
import cv2


class rhythmMap(object):

    def __init__(self, img, label):
        self._image_name = img
        self._label_name = label
        self._image = None
        self._label = []

    def read_image(self):
        self._image = cv2.imread(data_path + self._image_name, 0)

    def read_label(self):
        with open(data_path + self._label_name, "r") as file:
            for line in file:
                temp = [int(x) for x in line.strip().split()]
                self._label.append(tuple(temp))

    def load(self):
        self.read_image()
        self.read_label()

    def show(self):
        img = cv2.cvtColor(self._image, cv2.COLOR_GRAY2RGB)
        (rows, cols) = self._image.shape
        font = cv2.FONT_HERSHEY_SIMPLEX
        for t in self._label:
            rhythm = t[0]
            start = t[1]
            end = t[2]
            cv2.rectangle(img, (start - 2, 1), (end + 2, rows - 1), (0, 0, 255), 2)
            cv2.putText(img, str(rhythm), (start - 10, 12), font, 0.3, (0, 0, 255), 1)

        cv2.imshow("rhythm map", img)
        cv2.waitKey(0)