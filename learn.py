from ultralytics import YOLO

def study():
  """обучаем YOLO модель на нашем датасете"""
  dataset_path = "data.yaml"
  model = YOLO("yolo11n.pt")
  model.train(data=dataset_path, epochs=150, batch=16, imgsz=640)


def testCase():
  """Проверяем новую модель"""
  model = YOLO("runs/detect/train8/weights/best.pt")
  result = model("DataSet/test/images/1gdbfp1a_jpg.rf.419de6d84df61d5eaf8f9b009c62e607.jpg", conf=0.1)
  result[0].show()

testCase()