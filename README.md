# Chat Analysis API 🚀

## 📌 Project Overview
This project analyzes chat transcripts between agents discussing articles from the Washington Post. It provides:
- **Data preprocessing & transformation**
- **Exploratory Data Analysis (EDA)**
- **REST API for chat analysis using Flask/FASTAPI**
- **Optimized for performance & scalability**

---

## 📌 Installation & Setup

### 1️⃣ Install Dependencies
```bash
pip install flask pandas numpy matplotlib seaborn fastapi uvicorn
```

### 2️⃣ Run Flask API
```bash
python app.py
```
or run FASTAPI:
```bash
uvicorn app:app --reload
```

---

## 📌 API Endpoints

### ✅ `GET /summary`
Returns dataset overview.

**Example:**
```bash
curl http://127.0.0.1:5000/summary
```

---

### ✅ `POST /transform`
Transforms raw input into a preprocessed form.

**Example:**
```bash
Invoke-WebRequest -Uri "http://127.0.0.1:5000/transform" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"text": "Hello, this is a sample message!"}' -UseBasicParsing
```

---

### ✅ `POST /analyze`
Analyzes a chat transcript and returns:
- **Article URL**
- **Message count per agent**
- **Overall sentiments**

**Example:**
```bash
Invoke-WebRequest -Uri "http://127.0.0.1:5000/analyze" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"conversation_id": "t_d004c097-424d-45d4-8f91-833d85c2da31"}' -UseBasicParsing
```

---

## 📌 Running Exploratory Data Analysis (EDA)
```bash
jupyter notebook EDA.ipynb
```

---

## 📌 Author
Developed by **Sarvesh Adithya J** 🚀
