from flask import Flask, render_template, request, redirect, url_for
from ultralytics import YOLO
from pathlib import Path
from database import *
from pdf_generator import generate_pdf
import os
import cv2

# ==========================================
# Flask App
# ==========================================

app = Flask(__name__)

# ==========================================
# Folders
# ==========================================

UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"
REPORT_FOLDER = "static/reports"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RESULT_FOLDER"] = RESULT_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER

# ==========================================
# Load YOLO Model
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "material_inspection_training" / "weights" / "best.pt"

print("====================================")
print("MODEL PATH :", MODEL_PATH)
print("MODEL EXISTS :", MODEL_PATH.exists())
print("====================================")

model = YOLO(str(MODEL_PATH))

# ==========================================
# Create Database
# ==========================================

create_database()

# ==========================================
# Home
# ==========================================

@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# Upload & Detection
# ==========================================

@app.route("/upload", methods=["POST"])
def upload():

    if "image" not in request.files:
        return "No image uploaded."

    file = request.files["image"]

    if file.filename == "":
        return "No file selected."

    filename = file.filename

    upload_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(upload_path)

    # ======================================
    # YOLO Prediction
    # ======================================

    results = model.predict(upload_path)

    result = results[0]

    annotated = result.plot()

    result_path = os.path.join(
        app.config["RESULT_FOLDER"],
        filename
    )

    cv2.imwrite(result_path, annotated)

    # ======================================
    # Extract Defects
    # ======================================

    defects = []

    total_confidence = 0

    for box in result.boxes:

        cls = int(box.cls[0])

        conf = float(box.conf[0])

        total_confidence += conf

        defects.append({
            "name": model.names[cls],
            "confidence": round(conf * 100, 2)
        })

    # ======================================
    # PASS / FAIL
    # ======================================

    if len(defects) == 0:

        status = "PASS"

        average_confidence = 0

        insert_inspection(
            filename,
            "None",
            0,
            status
        )

    else:

        status = "FAIL"

        average_confidence = round(
            (total_confidence / len(defects)) * 100,
            2
        )

        for defect in defects:

            insert_inspection(
                filename,
                defect["name"],
                defect["confidence"],
                status
            )

    # ======================================
    # Generate PDF Report
    # ======================================

    report_name = os.path.splitext(filename)[0] + ".pdf"

    report_path = os.path.join(
        app.config["REPORT_FOLDER"],
        report_name
    )

    generate_pdf(
        report_path,
        filename,
        defects,
        average_confidence,
        status
    )

    # ======================================
    # Result Page
    # ======================================

    return render_template(
        "result.html",
        original_image=filename,
        detected_image=filename,
        defects=defects,
        status=status,
        average_confidence=average_confidence,
        report_name=report_name
    )


# ==========================================
# Dashboard
# ==========================================

@app.route("/dashboard")
def dashboard():

    keyword = request.args.get("search", "")

    status = request.args.get("status", "ALL")

    stats = get_dashboard_stats()

    inspections = search_inspections(keyword, status)

    defect_counts = get_defect_counts()

    labels = [row[0] for row in defect_counts]

    values = [row[1] for row in defect_counts]

    return render_template(
        "dashboard.html",
        stats=stats,
        inspections=inspections,
        labels=labels,
        values=values,
        keyword=keyword,
        selected_status=status
    )
@app.route("/analytics")
def analytics():

    stats = get_dashboard_stats()

    trend = get_inspection_trend()
    top = get_top_defects()

    common = get_most_common_defect()
    highest = get_highest_confidence()

    top_defects = get_top_defects()

    pie_labels = []
    pie_values = []

    for row in top_defects:

        pie_labels.append(row[0])
        pie_values.append(row[1])

    top_labels = [row[0] for row in top]
    top_values = [row[1] for row in top]

    return render_template(

    "analytics.html",

    stats=stats,

    common=common,

    highest=highest,

    top_labels=top_labels,

    top_values=top_values,

    pie_labels=pie_labels,

    pie_values=pie_values

)
# ==========================================
# Clear History
# ==========================================

@app.route("/clear")
def clear():

    clear_database()

    return redirect(url_for("dashboard"))


# ==========================================
# Run
# ==========================================


if __name__ == "__main__":
    app.run(debug=True)