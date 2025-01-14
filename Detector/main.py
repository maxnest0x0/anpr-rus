import cv2
from ultralytics import YOLO
import easyocr

model_path='Detector/model/best.pt'
model = YOLO(model_path)

reader = easyocr.Reader(['ru'])

class Detector:
    def __init__(self, img_source):
        self.__img_source = img_source
        self.img = None
        self.detected = 0
        self.recognized = 0

    @staticmethod
    def show_img(img, window_name='Detected Image') -> None:
        cv2.imshow(window_name, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def draw_box(img, x1, y1, x2, y2, color=(0, 255, 0), thickness=2):
        cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)

    def open_img(self):
        if isinstance(self.__img_source, str):
            car_img = cv2.imread(self.__img_source)
            if car_img is None:
                raise FileNotFoundError(f"Не удалось загрузить изображение по пути: {self.__img_source}")
            car_img = cv2.cvtColor(car_img, cv2.COLOR_BGR2RGB)
        else:
            car_img = self.__img_source
        return car_img

    def __plate_extract(self):
        car_img = self.img = self.open_img()

        results = model(car_img)

        extracted_plates = []
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()
            class_ids = result.boxes.cls.cpu().numpy()

            for box, confidence, class_id in zip(boxes, confidences, class_ids):
                x1, y1, x2, y2 = map(int, box)
                w = x2 - x1
                h = y2 - y1

                if class_id == 0:
                    plate_img = car_img[y1:y2, x1:x2].copy()
                    extracted_plates.append((plate_img, confidence, (x1, y1), (w, h)))
                    self.draw_box(car_img, x1, y1, x2, y2)

        return extracted_plates

    def __resize_img(self, img, scale_percent: int):
        if img is None: return None

        height = int(img.shape[0] * scale_percent / 100)
        width = int(img.shape[1] * scale_percent / 100)

        resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
        return resized_img

    def get_license_plate(self):
        extracted_plates = self.__plate_extract()

        result_plates = []
        for extract_img, confidence, pos, size in extracted_plates:
            self.detected += 1

            extract_img = self.__resize_img(extract_img, 150)
            confidence = confidence.item()

            result = reader.readtext(extract_img)

            if result:
                self.recognized += 1
                plate_text = " ".join([text[1] for text in result])
                print(f"Распознанный номер: {plate_text}")
            else:
                plate_text = None
                print("Не удалось распознать номер.")

            result_plates.append((extract_img, plate_text, confidence, pos, size))

        return result_plates
