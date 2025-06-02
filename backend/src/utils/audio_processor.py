import librosa
import numpy as np
from typing import Tuple, Optional
from pydub import AudioSegment
import os
import tempfile
import speech_recognition as sr

class AudioProcessor:
    def __init__(self):
        self.sample_rate = 16000
        self.supported_formats = ['.wav', '.mp3', '.ogg', '.m4a']
        self.error_messages = {
            'format': 'صيغة الملف غير مدعومة. الرجاء استخدام WAV, MP3, OGG, or M4A.',
            'processing': 'حدث خطأ أثناء معالجة الملف الصوتي.',
            'speech_recognition': 'لم نتمكن من التعرف على الكلام في الملف الصوتي.',
            'empty': 'الملف الصوتي فارغ أو تالف.'
        }
        
    def convert_audio(self, file_path: str) -> str:
        """Convert audio to WAV format for processing"""
        try:
            # Get file extension
            _, ext = os.path.splitext(file_path)
            if ext.lower() not in self.supported_formats:
                raise ValueError(self.error_messages['format'])

            if ext.lower() != '.wav':
                # Load audio using pydub
                audio = AudioSegment.from_file(file_path)
                
                # Create temporary WAV file
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav:
                    wav_path = temp_wav.name
                    audio.export(wav_path, format='wav')
                return wav_path
            
            return file_path
        except Exception as e:
            raise ValueError(self.error_messages['processing'])

    def process_audio(self, audio_file: str) -> Tuple[np.ndarray, int]:
        """Process audio file and extract MFCC features"""
        try:
            # Convert audio to WAV if needed
            wav_file = self.convert_audio(audio_file)
            
            # Load audio file
            y, sr = librosa.load(wav_file, sr=self.sample_rate)
            
            # Clean up temporary file if created
            if wav_file != audio_file:
                os.unlink(wav_file)
            
            if len(y) == 0:
                raise ValueError(self.error_messages['empty'])
            
            # Extract MFCC features
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            
            return y, sr
        except Exception as e:
            raise ValueError(self.error_messages['processing'])

    def audio_to_text(self, audio_file: str, language: str = 'ar-AR') -> str:
        """Convert audio to text using speech recognition with Arabic support"""
        try:
            # Convert audio to WAV if needed
            wav_file = self.convert_audio(audio_file)
            
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_file) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio, language=language)
                
                # Clean up temporary file if created
                if wav_file != audio_file:
                    os.unlink(wav_file)
                    
                return text
        except sr.UnknownValueError:
            raise ValueError(self.error_messages['speech_recognition'])
        except Exception as e:
            raise ValueError(self.error_messages['processing'])

    def validate_audio_file(self, file_path: str) -> bool:
        """Validate audio file format and content"""
        try:
            _, ext = os.path.splitext(file_path)
            if ext.lower() not in self.supported_formats:
                return False
            
            # Try to load the file
            wav_file = self.convert_audio(file_path)
            y, sr = librosa.load(wav_file, sr=self.sample_rate, duration=1)  # Load just 1 second to check
            
            # Clean up
            if wav_file != file_path:
                os.unlink(wav_file)
                
            return len(y) > 0
        except:
            return False
