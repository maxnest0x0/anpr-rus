import cv2

class Detector:
    MODEL = cv2.CascadeClassifier('model/model.xml')
    MODEL_PARAM = {'scaleFactor': 1.1, 'minNeighbors': 5}

    def __init__(self, img_path):
        self.__img_path = img_path

    @staticmethod
    def show_img(img) -> None:
        cv2.imshow('Detected Image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def draw_box(img, x1, y1, x2, y2):
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    def open_img(self):
        car_img = cv2.imread(self.__img_path)
        car_img = cv2.cvtColor(car_img, cv2.COLOR_BGR2RGB)
        return car_img

    def __plate_extract(self):
        car_img = self.open_img()
        rect = self.MODEL.detectMultiScale(car_img,
                                           scaleFactor=self.MODEL_PARAM['scaleFactor'],
                                           minNeighbors=self.MODEL_PARAM['minNeighbors'])

        for x, y, w, h in rect:
            x1 = x + 5
            x2 = x + w - 15
            y1 = y + 10
            y2 = y + h - 5
            result = car_img[y1:y2, x1:x2]
            self.draw_box(car_img, x1, y1, x2, y2)
            self.show_img(car_img)  # Показать изображение с прямоугольником
        return result

    def __resize_img(self, img, scale_percent: int):
        height = int(img.shape[0] * scale_percent / 100)
        width = int(img.shape[1] * scale_percent / 100)

        resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

        return resized_img

    def get_license_plate(self):
        extract_img = self.__plate_extract()
        extract_img = self.__resize_img(extract_img, 150)
        return extract_img

# Пример использования
detector = Detector('../data_for_check/car.jpg')
license_plate_image = detector.get_license_plate()




