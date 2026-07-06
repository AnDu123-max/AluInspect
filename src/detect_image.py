from ultralytics import YOLO
import cv2
import os

# -----------------------------
# Load trained YOLO model
# -----------------------------
MODEL_PATH = "material_inspection_training/weights/best.pt"

model = YOLO(MODEL_PATH)

# -----------------------------
# Test image path
# -----------------------------
IMAGE_PATH = "test_images/crazing_1.jpg"

# Check if image exists
if not os.path.exists(IMAGE_PATH):
    print(f"❌ Image not found: {IMAGE_PATH}")
    exit()

# -----------------------------
# Perform prediction
# -----------------------------
results = model.predict(
    source=IMAGE_PATH,
    conf=0.25,
    save=False
)

# -----------------------------
# Print inspection result
# -----------------------------
print("\n========== MATERIAL INSPECTION ==========\n")

boxes = results[0].boxes

if len(boxes) == 0:
    print("✅ PASS")
    print("No defects detected.")

else:
    print("❌ FAIL")
    print(f"\nDetected {len(boxes)} defect(s):\n")

    for box in boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])

        print(f"• {model.names[cls]}  ({conf:.2%})")

# -----------------------------
# Display image
# -----------------------------
annotated = results[0].plot()

cv2.imshow("Material Inspection", annotated)
cv2.waitKey(0)
cv2.destroyAllWindows()