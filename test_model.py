from ultralytics import YOLO

model = YOLO(r"C:\Users\dubey\OneDrive\Desktop\material_inspection1\material_inspection_training\weights\best.pt")

# Test on an image
results = model.predict(source=r"c:\Users\dubey\Downloads\TEST.jpg", show=True)

print("Detection done!")