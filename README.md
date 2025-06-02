# Emotion Detection System

A full-stack emotion analysis system that supports both text and audio input, built with FastAPI and React.

## Features

- Text-based emotion analysis
- Audio file processing
- Support for multiple emotion categories
- Real-time analysis
- Modern, responsive UI

## Tech Stack

### Backend
- Python 3.8+
- FastAPI
- PyTorch
- Transformers (BERT)
- librosa
- SpeechRecognition

### Frontend
- React
- styled-components
- axios
- HTML5 Audio Support

## Deployment

### Backend (Render)

1. Fork/Clone this repository
2. Sign up on [Render](https://render.com)
3. Create a new Web Service
4. Connect your GitHub repository
5. Use the following settings:
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd backend/src && uvicorn main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)

1. Sign up on [Vercel](https://vercel.com)
2. Import your GitHub repository
3. Configure the following:
   - Framework Preset: Create React App
   - Build Command: `npm run build`
   - Output Directory: build
   - Install Command: `npm install`

### Environment Variables

Backend (Render):
- `PORT`: Set automatically by Render
- `PYTHON_VERSION`: 3.8.10

Frontend (Vercel):
- `REACT_APP_API_URL`: Your Render backend URL

## Development

1. Clone the repository:
```bash
git clone https://github.com/Abdoolos/emotinal_analysis.git
cd emotion-detection
```

2. Backend setup:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
cd src
uvicorn main:app --reload
```

3. Frontend setup:
```bash
cd frontend
npm install
npm start
```

## API Documentation

- GET `/`: Health check
- POST `/predict/text`: Text emotion analysis
- POST `/predict/audio`: Audio file emotion analysis

## Author

- Abdullah Alawiss

## License

MIT
