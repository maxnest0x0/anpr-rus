import cv2
from ultralytics import YOLO


class Detector:
    def __init__(self, img_path, model_path='model/best.pt'):
        self.__img_path = img_path
        self.model = YOLO(model_path)
        self.coords = []

    @staticmethod
    def show_img(img, window_name='Detected Image') -> None:
        cv2.imshow(window_name, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def draw_box(img, x1, y1, x2, y2, color=(0, 255, 0), thickness=2):
        cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)

    def open_img(self):
        car_img = cv2.imread(self.__img_path)
        if car_img is None:
            raise FileNotFoundError(f"Не удалось загрузить изображение по пути: {self.__img_path}")
        car_img = cv2.cvtColor(car_img, cv2.COLOR_BGR2RGB)
        return car_img

    def __plate_extract(self):
        car_img = self.open_img()

        results = self.model(car_img)

        def process_boxes(img, result):

            boxes = result.boxes.xyxy.cpu().numpy()

            self.coords = result.boxes.xyxy.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy()

            extracted_plates = []

            for box, confidence, class_id in zip(boxes, confidences, class_ids):
                x1, y1, x2, y2 = map(int, box)

                if class_id == 0:
                    plate_img = img[y1:y2, x1:x2]
                    self.draw_box(car_img, x1, y1, x2, y2)
                    extracted_plates.append(plate_img)
                    break
            return extracted_plates

        extracted_plates = process_boxes(car_img, results[0])

        self.show_img(car_img)
        if len(extracted_plates) > 0:
            return extracted_plates[0]
        else:
            return None

    def __resize_img(self, img, scale_percent: int):
        if img is None: return None

        height = int(img.shape[0] * scale_percent / 100)
        width = int(img.shape[1] * scale_percent / 100)

        resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
        return resized_img

    def get_license_plate(self):

        extract_img = self.__plate_extract()

        if extract_img is not None:
            extract_img = self.__resize_img(extract_img, 150)
            return extract_img
        else:
            return None
detector = Detector('path img')
license_plate_image = detector.get_license_plate()

if license_plate_image is not None:
    Detector.show_img(license_plate_image, 'Extracted License Plate')

else:
    print("Не удалось обнаружить номерной знак на изображении")
