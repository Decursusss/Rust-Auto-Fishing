import os
import time
import cv2
import numpy as np
from PIL import ImageGrab
import keyboard
import json
from datetime import datetime

class DatasetCollector:
    def __init__(self, output_dir="DataSet3/train/images", labels_dir="DataSet3/train/labels"):
        self.output_dir = output_dir
        self.labels_dir = labels_dir
        self.current_image = None
        self.current_boxes = []
        self.is_recording = False
        
        # Создаем директории, если они не существуют
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(labels_dir, exist_ok=True)
        
        # Загружаем конфигурацию
        self.config = self.load_config()
        
    def load_config(self):
        config_path = "dataset_config.json"
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            # Создаем базовую конфигурацию
            config = {
                "hotkeys": {
                    "start_recording": "f1",
                    "stop_recording": "f2",
                    "save_image": "f3",
                    "add_box": "f4",
                    "exit": "esc"
                },
                "image_settings": {
                    "resolution": [1920, 1080],
                    "format": "png"
                }
            }
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4)
            return config

    def capture_screen(self):
        """Захват экрана"""
        screen = np.array(ImageGrab.grab())
        return cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

    def save_image_with_boxes(self, image, boxes):
        """Сохранение изображения и разметки"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(self.output_dir, f"bobber_{timestamp}.png")
        label_path = os.path.join(self.labels_dir, f"bobber_{timestamp}.txt")
        
        # Сохраняем изображение
        cv2.imwrite(image_path, image)
        
        # Сохраняем разметку в формате YOLO
        height, width = image.shape[:2]
        with open(label_path, 'w') as f:
            for box in boxes:
                x1, y1, x2, y2 = box
                # Конвертируем в формат YOLO (нормализованные координаты)
                x_center = ((x1 + x2) / 2) / width
                y_center = ((y1 + y2) / 2) / height
                box_width = (x2 - x1) / width
                box_height = (y2 - y1) / height
                f.write(f"0 {x_center} {y_center} {box_width} {box_height}\n")

    def run(self):
        print("Запуск сборщика датасета...")
        print("Горячие клавиши:")
        print(f"F1 - Начать запись")
        print(f"F2 - Остановить запись")
        print(f"F3 - Сохранить текущий кадр")
        print(f"F4 - Добавить разметку")
        print(f"ESC - Выход")

        while True:
            if keyboard.is_pressed(self.config["hotkeys"]["exit"]):
                break
                
            if keyboard.is_pressed(self.config["hotkeys"]["start_recording"]):
                self.is_recording = True
                print("Запись начата")
                time.sleep(0.5)  # Предотвращаем множественные нажатия
                
            if keyboard.is_pressed(self.config["hotkeys"]["stop_recording"]):
                self.is_recording = False
                print("Запись остановлена")
                time.sleep(0.5)
                
            if self.is_recording:
                self.current_image = self.capture_screen()
                
                # Отображаем текущий кадр
                display_image = self.current_image.copy()
                for box in self.current_boxes:
                    x1, y1, x2, y2 = box
                    cv2.rectangle(display_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                cv2.imshow("Dataset Collector", display_image)
                cv2.waitKey(1)
                
                if keyboard.is_pressed(self.config["hotkeys"]["save_image"]):
                    self.save_image_with_boxes(self.current_image, self.current_boxes)
                    print(f"Изображение сохранено")
                    self.current_boxes = []
                    time.sleep(0.5)
                    
                if keyboard.is_pressed(self.config["hotkeys"]["add_box"]):
                    # Здесь можно добавить логику для ручной разметки
                    # Например, через клики мыши
                    print("Режим разметки активирован")
                    time.sleep(0.5)

        cv2.destroyAllWindows()

if __name__ == "__main__":
    collector = DatasetCollector()
    collector.run() 