from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
from typing import Dict

class EmotionClassifier:
    def __init__(self):
        # Using a multilingual model that supports Arabic
        self.model_name = "CAMeL-Lab/bert-base-arabic-camelbert-mix"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=7  # Updated number of emotion classes
        )
        self.emotion_labels = [
            'فرح',    # joy
            'حزن',    # sadness
            'غضب',    # anger
            'خوف',    # fear
            'مفاجأة', # surprise
            'حب',     # love
            'محايد'   # neutral
        ]

    def preprocess_text(self, text: str) -> str:
        """Preprocess text for Arabic language handling"""
        # Remove excessive whitespace
        text = ' '.join(text.split())
        return text

    def predict_emotion(self, text: str) -> Dict[str, float]:
        """
        Predict emotions from text with confidence scores
        Returns a dictionary of emotion labels and their probabilities
        """
        # Preprocess the text
        text = self.preprocess_text(text)
        
        # Tokenize and prepare for model
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        )

        # Get model predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = F.softmax(outputs.logits, dim=1)

        # Convert predictions to dictionary
        predictions = {}
        for idx, emotion in enumerate(self.emotion_labels):
            predictions[emotion] = float(probs[0][idx])

        return predictions

    def get_dominant_emotion(self, text: str) -> str:
        """Get the emotion with highest confidence score"""
        predictions = self.predict_emotion(text)
        return max(predictions.items(), key=lambda x: x[1])[0]

    def get_emotion_summary(self, text: str) -> dict:
        """Get comprehensive emotion analysis"""
        predictions = self.predict_emotion(text)
        dominant_emotion = self.get_dominant_emotion(text)
        
        return {
            "text": text,
            "emotions": predictions,
            "dominant_emotion": dominant_emotion,
            "confidence": predictions[dominant_emotion]
        }
