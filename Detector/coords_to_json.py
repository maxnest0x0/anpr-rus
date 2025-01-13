import json
from main import Detector


def normalize(box, shape):
    x1, y1, x2, y2 = box
    image_height, image_width = shape[:2]
    x_norm = (x1 + x2) / 2 / image_width
    y_norm = (y1 + y2) / 2 / image_height
    box_width_norm = (x2 - x1) / image_width
    box_height_norm = (y2 - y1) / image_height
    return [round(x_norm, 4), round(y_norm, 4), round(box_width_norm, 4), round(box_height_norm, 4)]


with open('../Dataset/license_plates.json', 'r') as f:
    data = json.load(f)
    for i in range(1, 10008):
        detector = Detector(f'../Dataset/Imgs/{1}.jpg')
        detector.get_license_plate()
        print(detector.get_coords())
        data[i - 1]['box'] = normalize(detector.get_coords(), detector.get_shape_img())
        break
with open('../Dataset/license_plates.json', 'w') as f:
    json.dump(data, f, indent=4)
