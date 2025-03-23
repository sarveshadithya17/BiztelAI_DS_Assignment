# Chat Analysis Project – Methodology & Insights 📊

## 📌 Data Preprocessing Steps
1. **Loading Data:** JSON converted into a structured Pandas DataFrame.
2. **Cleaning Data:** Removed duplicates, optimized data types.
3. **Text Preprocessing:**
   - Lowercasing
   - Removing punctuation
   - Stopword removal
   - Tokenization & lemmatization

---

## 📌 Exploratory Data Analysis (EDA)
- **Most Discussed Articles:** Identified articles with the highest number of conversations.
- **Agent Behavior Analysis:** Compared message counts between `agent_1` & `agent_2`.
- **Sentiment Distribution:** Found that most messages were "Curious" and "Neutral."

---

## 📌 API Implementation
Developed using **Flask** / **FastAPI**:
- **`/summary`** – Dataset insights
- **`/transform`** – Real-time text transformation
- **`/analyze`** – Chat transcript analysis

---

## 📌 Performance Optimizations
✅ **Vectorized Pandas operations**  
✅ **Asynchronous API processing** (Flask & FastAPI)  
✅ **Memory-efficient data handling**  

---

## 📌 Future Enhancements
- Integrate **LLM for automated summaries**.
- Improve **sentiment classification using NLP**.
- Deploy API using **Docker & AWS Lambda**.

---

## 📌 Author
Developed by **Sarvesh Adithya J.** 🚀
