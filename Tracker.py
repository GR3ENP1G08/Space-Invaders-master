import cv2


class Tracker:

    def __init__(self, imagem, bbox):
        self.tracker = cv2.TrackerCSRT_create()
        self.tracker.init(imagem, bbox)

    def track(self, image):
        track_ok, bbox = self.tracker.update(image)
        if track_ok:
            x, y, w, h = bbox
            cv2.rectangle(img=image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 255, 255), thickness=2)

            x = (x + (x + w)) / 2
            position_x = x * 100 / image.shape[1]

            if position_x < 30:
                direction = -1
            elif position_x > 70:
                direction = 1
            else:
                direction = 0

            y = (y + (y + h)) / 2
            position_y = y * 100 / image.shape[0]

            return direction, position_y < 50
        else:
            cv2.putText(img=image,
                        text="Tracking failed",
                        org=(5, 35),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.5,
                        color=(0, 0, 255),
                        thickness=2)
            return 0, 0
