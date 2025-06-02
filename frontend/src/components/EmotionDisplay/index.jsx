import React, { useState } from 'react';
import axios from 'axios';
import {
  Container,
  Header,
  Avatar,
  DesignerName,
  EmotionLabel,
  EmotionsContainer,
  AudioInput,
  Button,
  Input,
  ErrorMessage,
  LoadingSpinner
} from './styles';

const API_URL = 'http://localhost:8000';
const DEFAULT_AVATAR = 'https://ui-avatars.com/api/?name=Abdullah+Alawiss&background=random';

// English emotion mapping
const emotionMapping = {
  'فرح': 'Joy',
  'حزن': 'Sadness',
  'غضب': 'Anger',
  'خوف': 'Fear',
  'مفاجأة': 'Surprise',
  'حب': 'Love',
  'محايد': 'Neutral'
};

const EmotionDisplay = () => {
  const [text, setText] = useState('');
  const [audioFile, setAudioFile] = useState(null);
  const [emotions, setEmotions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleTextSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) {
      setError('Please enter text to analyze');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const response = await axios.post(`${API_URL}/predict/text`, { text });
      if (response.data.emotions) {
        const translatedEmotions = {};
        Object.entries(response.data.emotions).forEach(([emotion, score]) => {
          translatedEmotions[emotionMapping[emotion] || emotion] = score;
        });
        setEmotions(translatedEmotions);
      } else {
        throw new Error('Invalid response format');
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Error analyzing text');
      console.error('Error:', err);
    }
    setLoading(false);
  };

  const handleAudioSubmit = async (e) => {
    e.preventDefault();
    if (!audioFile) {
      setError('Please select an audio file');
      return;
    }

    const formData = new FormData();
    formData.append('file', audioFile);

    setLoading(true);
    setError('');
    try {
      const response = await axios.post(`${API_URL}/predict/audio`, formData);
      if (response.data.emotions) {
        const translatedEmotions = {};
        Object.entries(response.data.emotions).forEach(([emotion, score]) => {
          translatedEmotions[emotionMapping[emotion] || emotion] = score;
        });
        setEmotions(translatedEmotions);
      } else {
        throw new Error('Invalid response format');
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Error analyzing audio file');
      console.error('Error:', err);
    }
    setLoading(false);
  };

  const handleAudioChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 10 * 1024 * 1024) {
        setError('File size too large. Maximum size is 10MB');
        return;
      }
      setAudioFile(file);
      setError('');
    }
  };

  return (
    <Container>
      <Header>
        <Avatar 
          src={DEFAULT_AVATAR}
          alt="Designer Avatar"
        />
        <DesignerName>Abdullah Alawiss</DesignerName>
      </Header>

      <form onSubmit={handleTextSubmit}>
        <Input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter text to analyze emotions..."
          disabled={loading}
        />
        <Button type="submit" disabled={loading || !text.trim()}>
          {loading ? <LoadingSpinner /> : 'Analyze Text'}
        </Button>
      </form>

      <AudioInput>
        <input
          type="file"
          accept="audio/*"
          onChange={handleAudioChange}
          style={{ display: 'none' }}
          id="audio-input"
          disabled={loading}
        />
        <Button as="label" htmlFor="audio-input" disabled={loading}>
          {loading ? <LoadingSpinner /> : 'Select Audio File'}
        </Button>
        {audioFile && (
          <>
            <div style={{ margin: '10px 0' }}>
              Selected: {audioFile.name}
            </div>
            <Button onClick={handleAudioSubmit} disabled={loading}>
              {loading ? <LoadingSpinner /> : 'Analyze Audio'}
            </Button>
          </>
        )}
      </AudioInput>

      {error && <ErrorMessage>{error}</ErrorMessage>}

      {emotions && (
        <EmotionsContainer>
          {Object.entries(emotions).map(([emotion, score]) => (
            <EmotionLabel key={emotion} emotion={emotion}>
              {emotion}: {(score * 100).toFixed(1)}%
            </EmotionLabel>
          ))}
        </EmotionsContainer>
      )}
    </Container>
  );
};

export default EmotionDisplay;
