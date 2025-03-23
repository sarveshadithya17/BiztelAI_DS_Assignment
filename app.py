import pandas as pd
import numpy as np
import json
import re
import logging
import asyncio
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor

# DataLoader Class: Loads and structures dataset
class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        """Load JSON data into a Pandas DataFrame using vectorized operations."""
        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        records = [
            {
                "conversation_id": conv_id,
                "article_url": conv_data.get("article_url", ""),
                "config": conv_data.get("config", ""),
                "message": msg.get("message", ""),
                "agent": msg.get("agent", ""),
                "sentiment": msg.get("sentiment", ""),
                "knowledge_source": ", ".join(msg.get("knowledge_source", [])),
                "turn_rating": msg.get("turn_rating", ""),
                "agent_1_rating": conv_data.get("conversation_rating", {}).get("agent_1", ""),
                "agent_2_rating": conv_data.get("conversation_rating", {}).get("agent_2", ""),
            }
            for conv_id, conv_data in data.items() for msg in conv_data.get("content", [])
        ]
        self.df = pd.DataFrame(records)
        return self.df

# DataCleaner Class: Handles missing values and optimizes data types
class DataCleaner:
    @staticmethod
    def clean_data(df):
        """Optimize data types and remove duplicates."""
        categorical_cols = ["config", "agent", "sentiment", "turn_rating", "agent_1_rating", "agent_2_rating"]
        df[categorical_cols] = df[categorical_cols].astype("category")
        return df.drop_duplicates()

# DataTransformer Class: Handles text preprocessing
class DataTransformer:
    custom_stopwords = set(["the", "a", "an", "is", "to", "and", "in", "on", "at", "for", "with", "about", "by", "from"])

    @staticmethod
    def preprocess_text(text):
        """Vectorized text processing."""
        text = re.sub(r"[^\w\s]", "", text.lower())
        return " ".join(word for word in text.split() if word not in DataTransformer.custom_stopwords)

    @staticmethod
    def apply_text_processing(df):
        df["processed_message"] = df["message"].apply(lambda x: DataTransformer.preprocess_text(x))
        return df

# ChatAnalyzer Class: Provides insights for chat transcripts
class ChatAnalyzer:
    @staticmethod
    def summarize_transcript(df, conversation_id):
        """Extract chat insights asynchronously."""
        transcript = df[df["conversation_id"] == conversation_id]
        if transcript.empty:
            return {"error": "Invalid conversation ID."}

        return {
            "article_url": transcript["article_url"].iloc[0],
            "agent_1_messages": int((transcript["agent"] == "agent_1").sum()),  # Convert int64 to int
            "agent_2_messages": int((transcript["agent"] == "agent_2").sum()),  # Convert int64 to int
            "agent_1_sentiment": str(transcript.loc[transcript["agent"] == "agent_1", "sentiment"].mode()[0]),
            "agent_2_sentiment": str(transcript.loc[transcript["agent"] == "agent_2", "sentiment"].mode()[0])
        }

# Flask API Setup
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
executor = ThreadPoolExecutor()

# Load and process dataset
file_path = "BiztelAI_DS_Dataset_Mar'25.json"  # Replace with actual file path
loader = DataLoader(file_path)
df = loader.load_data()
df = DataCleaner.clean_data(df)
df = DataTransformer.apply_text_processing(df)

# EDA: Visualizing Data Insights
def visualize_data():
    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, x="agent")
    plt.title("Message Count per Agent")
    plt.show()

@app.route("/summary", methods=["GET"])
async def get_summary():
    return jsonify({
        "total_conversations": df["conversation_id"].nunique(),
        "total_messages": len(df),
        "unique_articles": df["article_url"].nunique()
    })

@app.route("/transform", methods=["POST"])
async def transform_text():
    data = request.json
    if "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400
    loop = asyncio.get_running_loop()
    processed_text = await loop.run_in_executor(executor, DataTransformer.preprocess_text, data["text"])
    return jsonify({"processed_text": processed_text})

@app.route("/analyze", methods=["POST"])
async def analyze_chat():
    data = request.json
    if "conversation_id" not in data:
        return jsonify({"error": "Missing 'conversation_id' field"}), 400
    loop = asyncio.get_running_loop()
    summary = await loop.run_in_executor(executor, ChatAnalyzer.summarize_transcript, df, data["conversation_id"])
    return jsonify(summary)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
