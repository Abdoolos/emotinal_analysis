from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
from typing import Dict, Optional
import os
import logging
import time
import gc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmotionClassifier:
    def __init__(self):
        # Using a multilingual model that supports Arabic
        self.model_name = "CAMeL-Lab/bert-base-arabic-camelbert-mix"
        self.tokenizer = None
        self.model = None
        self.max_retries = 3
        self.retry_delay = 5  # seconds
        self.cache_dir = os.environ.get('TRANSFORMERS_CACHE', '/tmp/transformers_cache')
        
        # Define emotion labels
        self.emotion_labels = [
            'فرح',    # joy
            'حزن',    # sadness
            'غضب',    # anger
            'خوف',    # fear
            'مفاجأة', # surprise
            'حب',     # love
            'محايد'   # neutral
        ]
        
        # Initialize the model with optimizations
        self.initialize_model()
        
    def initialize_model(self):
        """Initialize the model with retries and error handling"""
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Attempting to load model (attempt {attempt + 1}/{self.max_retries})")
                
                # Clear memory
                gc.collect()
                torch.cuda.empty_cache() if torch.cuda.is_available() else None
                
                # Load tokenizer with memory optimization
                if self.tokenizer is None:
                    self.tokenizer = AutoTokenizer.from_pretrained(
                        self.model_name,
                        local_files_only=False,
                        cache_dir=self.cache_dir,
                        low_cpu_mem_usage=True
                    )
                
                # Load model with memory optimization
                if self.model is None:
                    self.model = AutoModelForSequenceClassification.from_pretrained(
                        self.model_name,
                        num_labels=7,
                        local_files_only=False,
                        cache_dir=self.cache_dir,
                        low_cpu_mem_usage=True,
                        torch_dtype=torch.float32
                    )
                    
                    # Move model to CPU explicitly and optimize memory
                    self.model.to('cpu')
                    self.model.eval()  # Set to evaluation mode
                
                logger.info("Model loaded successfully")
                return True
                
            except Exception as e:
                logger.error(f"Error loading model: {str(e)}")
                if attempt < self.max_retries - 1:
                    logger.info(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    logger.error("Failed to load model after all attempts")
                    raise RuntimeError("Failed to initialize the emotion classifier model")

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
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model not initialized. Please ensure the model is properly loaded.")

        try:
            # Preprocess the text
            text = self.preprocess_text(text)
            
            # Clear memory before prediction
            gc.collect()
            torch.cuda.empty_cache() if torch.cuda.is_available() else None
            
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
                
            logger.info("Prediction successful")

            # Convert predictions to dictionary
            predictions = {}
            for idx, emotion in enumerate(self.emotion_labels):
                predictions[emotion] = float(probs[0][idx])

            # Clear memory after prediction
            del outputs
            gc.collect()
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            raise RuntimeError(f"Failed to predict emotions: {str(e)}")

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
