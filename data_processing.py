import pandas as pd
import numpy as np
import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download NLTK resources (run once)
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

class DataLoader:
    """Loads and structures JSON dataset into a Pandas DataFrame."""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        """Reads JSON file and converts it to a structured Pandas DataFrame."""
        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        records = []
        for conv_id, conv_data in data.items():
            article_url = conv_data.get("article_url", "")
            config = conv_data.get("config", "")
            conversation_rating = conv_data.get("conversation_rating", {})

            for message in conv_data.get("content", []):
                record = {
                    "conversation_id": conv_id,
                    "article_url": article_url,
                    "config": config,
                    "message": message.get("message", ""),
                    "agent": message.get("agent", ""),
                    "sentiment": message.get("sentiment", ""),
                    "turn_rating": message.get("turn_rating", ""),
                    "agent_1_rating": conversation_rating.get("agent_1", ""),
                    "agent_2_rating": conversation_rating.get("agent_2", ""),
                }
                records.append(record)

        self.df = pd.DataFrame(records)
        return self.df

class DataCleaner:
    """Handles missing values, duplicates, and optimizes data types."""
    
    def __init__(self, df):
        self.df = df

    def clean_data(self):
        """Removes duplicates, fills missing values, and converts data types."""
        # Convert categorical columns to category type
        categorical_columns = ["config", "agent", "sentiment", "turn_rating", "agent_1_rating", "agent_2_rating"]
        for col in categorical_columns:
            self.df[col] = self.df[col].astype("category")

        # Remove duplicates
        self.df = self.df.drop_duplicates()

        return self.df

class DataTransformer:
    """Preprocesses text by removing stopwords, tokenizing, and normalizing."""
    
    def __init__(self, df):
        self.df = df
        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()

    def preprocess_text(self, text):
        """Converts text to lowercase, removes punctuation, tokenizes, and lemmatizes."""
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
        tokens = word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens if word not in self.stop_words]
        return " ".join(tokens)

    def apply_transformation(self):
        """Applies text preprocessing to the 'message' column."""
        self.df["processed_message"] = self.df["message"].apply(self.preprocess_text)
        return self.df

# === Pipeline Execution ===

if __name__ == "__main__":
    file_path = "BiztelAI_DS_Dataset_Mar'25.json"  # Update with actual file path

    # Load Data
    loader = DataLoader(file_path)
    df = loader.load_data()

    # Clean Data
    cleaner = DataCleaner(df)
    df_cleaned = cleaner.clean_data()

    # Transform Data
    transformer = DataTransformer(df_cleaned)
    df_transformed = transformer.apply_transformation()

    # Save processed data to CSV
    df_transformed.to_csv("processed_chat_data.csv", index=False)

    print("Data processing completed! Processed data saved as 'processed_chat_data.csv'.")
