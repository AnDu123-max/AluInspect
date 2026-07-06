# 🤖 AluInspect – AI-Powered Aluminium Surface Inspection System

AluInspect is an AI-powered web application that automatically detects surface defects on aluminium materials using the YOLOv8 deep learning model. The system helps automate quality inspection by identifying defects, classifying products as PASS or FAIL, generating inspection reports, and providing analytics through an interactive dashboard.

---

## 📌 Features

- AI-powered aluminium surface defect detection
- YOLOv8 object detection model
- Upload aluminium images for inspection
- Real-time defect detection
- PASS / FAIL classification
- Confidence score display
- Inspection history
- Search and filter inspections
- Interactive analytics dashboard
- Pie charts and bar charts
- PDF inspection report generation
- SQLite database integration
- Modern responsive UI

---

## 🛠️ Technologies Used

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Chart.js

### Backend
- Python
- Flask

### AI & Computer Vision
- YOLOv8
- OpenCV
- Ultralytics

### Database
- SQLite

---

## 📂 Project Structure

```
AluInspect/
│
├── app.py
├── database.py
├── requirements.txt
├── database.db
│
├── static/
│   ├── css/
│   ├── uploads/
│   └── results/
│
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── analytics.html
│   └── report.html
│
├── model/
│   └── best.pt
│
└── README.md
```

---

## ⚙️ How to Run

### Clone Repository

```bash
git clone https://github.com/YourUsername/AluInspect.git
```

### Go into project folder

```bash
cd AluInspect
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run application

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```

---

## 📊 Dashboard

The dashboard includes

- Total inspections
- Passed inspections
- Failed inspections
- Average confidence
- PASS vs FAIL chart
- Defect distribution chart
- Inspection history
- Search functionality

---

## 📈 Analytics

The analytics page provides

- Inspection statistics
- Defect distribution
- Confidence analysis
- Interactive charts
- Historical inspection data

---

## 📄 Output

- Detected defect image
- Confidence score
- PASS / FAIL status
- PDF inspection report
- Inspection history

---

## 🎯 Future Improvements

- User Login & Authentication
- Multi-user support
- Live camera inspection
- Email report generation
- Cloud database integration
- Mobile application
- Real-time factory deployment

---

## 👨‍💻 Author

**Anurag Dubey**

B.Tech Computer Science Engineering

Project: **AluInspect – AI-Powered Aluminium Surface Inspection System**
