from PIL import Image
import os

QUEUE_DIR = "04_Temp/intake_queue"
dummy_path = os.path.join(QUEUE_DIR, "test_plant.jpg")

if not os.path.exists(QUEUE_DIR):
    os.makedirs(QUEUE_DIR)

img = Image.new('RGB', (100, 100), color = 'red')
img.save(dummy_path)
print(f"Created dummy image at {dummy_path}")
