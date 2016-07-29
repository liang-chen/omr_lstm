
from globalv import data_path, const_rows, const_cols
import cv2


class sequenceLabelGenerator(object):

    def __init__(self, img, label):
        self._image_name = img
        self._label_name = label
        self._image = None
        self._label = []
        self._load()

    def _read_image(self):
        tmp = cv2.imread(data_path + self._image_name, 0)
        (rows, cols) = tmp.shape
        #use constant width and height
        ratio = const_rows/float(rows)
        tmp = cv2.resize(tmp, (0, 0), fx=ratio, fy=ratio)
        cols = int(cols*ratio)
        if cols > const_cols:
            self._image = tmp[:,0:int(const_cols)]
        else:
            pad = int(const_cols) - cols
            self._image = cv2.copyMakeBorder(tmp, top = 0, bottom = 0, left= pad, right = 0, borderType= cv2.BORDER_CONSTANT, value=255 )
            for l in self._label:
                l[1] += pad
                l[2] += pad
                
    def _read_label(self):
        with open(data_path + self._label_name, "r") as file:
            for line in file:
                temp = line.strip().split()
                temp[0:4] = [int(x) for x in temp[0:4]] #rhythm, start col, end col, num of pitches
                self._label.append(temp)

    def _load(self):
        self._read_label()
        self._read_image()

    def show(self):
        img = cv2.cvtColor(self._image, cv2.COLOR_GRAY2RGB)
        (rows, cols) = self._image.shape
        font = cv2.FONT_HERSHEY_SIMPLEX
        #print rows, cols
        for l in self._label:
            rhythm = l[0]
            start = l[1]
            end = l[2]
            cv2.rectangle(img, (start - 2, 1), (end + 2, rows - 1), (0, 0, 255), 2)
            cv2.putText(img, str(rhythm), (start - 10, 12), font, 0.3, (0, 0, 255), 1)

        cv2.imshow("rhythm map", img)
        cv2.waitKey(0)

    def slice(self, start, end):
        label = None

        for l in self._label:
            overlap = max(0, min(end, l[2]) - max(start, l[1]))
            
            if overlap > 0.5*min(end-start, l[2] - l[1]):
                label = l
                break
            
        return self._image[:, start:end], label
