from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from backend.src.models.emotion_classifier import EmotionClassifier
from backend.src.utils.audio_processor import AudioProcessor
import tempfile
import os

class TextRequest(BaseModel):
    text: str

app = FastAPI(
    title="نظام تحليل المشاعر",
    description="تحليل المشاعر من النصوص والملفات الصوتية",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "https://emotion-detection-frontend.vercel.app",  # Add your Vercel domain
    "https://*.vercel.app"  # Allow all Vercel preview deployments
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize our models
emotion_classifier = EmotionClassifier()
audio_processor = AudioProcessor()

# Error messages
ERROR_MESSAGES = {
    "text_empty": "النص فارغ. الرجاء إدخال نص للتحليل.",
    "text_too_long": "النص طويل جداً. الحد الأقصى هو 512 حرف.",
    "file_empty": "لم يتم تحميل أي ملف صوتي.",
    "file_invalid": "صيغة الملف غير صالحة.",
    "processing_error": "حدث خطأ أثناء معالجة الطلب."
}

@app.get("/")
async def read_root():
    return {
        "status": "Emotion Detection API is running",
        "version": "1.0.0",
        "designer": "Abdullah Alawiss"
    }

@app.post("/predict/text")
async def predict_emotion_from_text(request: TextRequest):
    text = request.text.strip()
    
    if not text:
        raise HTTPException(status_code=400, detail=ERROR_MESSAGES["text_empty"])
    
    if len(text) > 512:
        raise HTTPException(status_code=400, detail=ERROR_MESSAGES["text_too_long"])

    try:
        analysis = emotion_classifier.get_emotion_summary(text)
        return {
            "text": text,
            "emotions": analysis["emotions"],
            "dominant_emotion": analysis["dominant_emotion"],
            "confidence": analysis["confidence"],
            "designer": "Abdullah Alawiss"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["processing_error"])

@app.post("/predict/audio")
async def predict_emotion_from_audio(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail=ERROR_MESSAGES["file_empty"])

    temp_file_path = ""
    try:
        # Save uploaded file temporarily
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        # Validate audio file
        if not audio_processor.validate_audio_file(temp_file_path):
            raise HTTPException(status_code=400, detail=ERROR_MESSAGES["file_invalid"])

        # Convert audio to text
        text = audio_processor.audio_to_text(temp_file_path)
        
        # Get emotion predictions
        analysis = emotion_classifier.get_emotion_summary(text)
        
        return {
            "text": text,
            "emotions": analysis["emotions"],
            "dominant_emotion": analysis["dominant_emotion"],
            "confidence": analysis["confidence"],
            "designer": "Abdullah Alawiss"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=ERROR_MESSAGES["processing_error"])
    finally:
        # Cleanup
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
