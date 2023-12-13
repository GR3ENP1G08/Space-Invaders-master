from ultralytics import YOLO
import cv2
import numpy as np

class ObjectDetection:

    def __init__(self):
        self.model = YOLO("yolov8n.pt")
        print("Known classes ({})".format(len(self.model.names)))
        for i in range(len(self.model.names)):
            print("{} : {}".format(i, self.model.names[i]))

    def process(self, image, object_class):
        image = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2RGB)

        results = self.model(image, verbose=False)

        image_objects = image.copy()

        direction = 0
        position_y = 100

        objects = results[0]
        for object in objects:
            box = object.boxes.data[0]
            pt1 = (int(box[0]), int(box[1]))
            pt2 = (int(box[2]), int(box[3]))
            confidence = box[4]
            class_id = int(box[5])

            if class_id == object_class and confidence > 0.7:
                cv2.rectangle(img=image_objects, pt1=pt1, pt2=pt2, color=(255, 0, 0), thickness=2)
                text = "{}:{:.2f}".format(objects.names[class_id], confidence)
                cv2.putText(img=image_objects,
                            text=text,
                            org=np.array(np.round((float(box[0]), float(box[1] - 1))), dtype=int),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.5,
                            color=(255, 0, 0),
                            thickness=1)

                x = (pt1[0] + pt2[0]) / 2
                position_x = x * 100 / image.shape[1]

                y = (pt1[1] + pt2[1]) / 2
                position_y = y * 100 / image.shape[0]

                if x > (2 / 3) * image.shape[1]:
                    direction = 1
                elif x < (1 / 3) * image.shape[1]:
                    direction = -1

        image_objects = cv2.cvtColor(src=image_objects, code=cv2.COLOR_RGB2BGR)

        return image_objects, direction, position_y < 50