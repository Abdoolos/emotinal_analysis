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
        # Using a smaller Arabic model
        self.model_name = "asafaya/bert-mini-arabic"  # Smaller model
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
        
        # Initialize only the tokenizer
        self.initialize_tokenizer()
        
    def initialize_tokenizer(self):
        """Initialize only the tokenizer to save memory"""
        for attempt in range(self.max_retries):
            try:
                logger.info("Loading tokenizer...")
                if self.tokenizer is None:
                    self.tokenizer = AutoTokenizer.from_pretrained(
                        self.model_name,
                        local_files_only=False,
                        cache_dir=self.cache_dir
                    )
                return True
            except Exception as e:
                logger.error(f"Error loading tokenizer: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    raise RuntimeError("Failed to initialize tokenizer")

    def load_model(self):
        """Load the model only when needed"""
        try:
            logger.info("Loading model...")
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name,
                num_labels=7,
                local_files_only=False,
                cache_dir=self.cache_dir,
                low_cpu_mem_usage=True,
                torch_dtype=torch.float32
            )
            self.model.to('cpu')
            self.model.eval()
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise RuntimeError("Failed to load model")

    def unload_model(self):
        """Unload the model to free memory"""
        if self.model is not None:
            del self.model
            self.model = None
            gc.collect()
            torch.cuda.empty_cache() if torch.cuda.is_available() else None
            logger.info("Model unloaded")

    def preprocess_text(self, text: str) -> str:
        """Preprocess text for Arabic language handling"""
        return ' '.join(text.split())

    def predict_emotion(self, text: str) -> Dict[str, float]:
        """Predict emotions with dynamic model loading"""
        try:
            # Load model if not loaded
            if self.model is None:
                self.load_model()

            # Preprocess and tokenize
            text = self.preprocess_text(text)
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=128  # Reduced from 512 to save memory
            )

            # Get predictions
            with torch.no_grad():
                outputs = self.model(**inputs)
                probs = F.softmax(outputs.logits, dim=1)

            # Create predictions dictionary
            predictions = {
                emotion: float(probs[0][idx])
                for idx, emotion in enumerate(self.emotion_labels)
            }

            # Unload model to free memory
            self.unload_model()

            return predictions

        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            if self.model is not None:
                self.unload_model()
            raise RuntimeError(f"Failed to predict emotions: {str(e)}")

    def get_dominant_emotion(self, text: str) -> str:
        """Get the emotion with highest confidence score"""
        predictions = self.predict_emotion(text)
        return max(predictions.items(), key=lambda x: x[1])[0]

    def get_emotion_summary(self, text: str) -> dict:
        """Get comprehensive emotion analysis"""
        predictions = self.predict_emotion(text)
        dominant_emotion = max(predictions.items(), key=lambda x: x[1])[0]
        
        return {
            "text": text,
            "emotions": predictions,
            "dominant_emotion": dominant_emotion,
            "confidence": predictions[dominant_emotion]
        }
