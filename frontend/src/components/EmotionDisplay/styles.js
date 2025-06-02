import styled from 'styled-components';

export const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  background-color: #f5f5f5;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-family: 'Roboto', sans-serif;
`;

export const Header = styled.div`
  width: 100%;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  padding: 10px 0;
  border-bottom: 2px solid #eee;
  margin-bottom: 20px;
`;

export const Avatar = styled.img`
  width: 50px;
  height: 50px;
  border-radius: 25px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

export const DesignerName = styled.div`
  font-size: 1.2em;
  font-weight: bold;
  color: #333;
  margin-left: 10px;
`;

export const EmotionLabel = styled.div`
  padding: 12px 24px;
  margin: 5px;
  border-radius: 20px;
  font-weight: 600;
  background-color: ${props => {
    switch (props.emotion) {
      case 'Joy': return '#FFD700';
      case 'Sadness': return '#4682B4';
      case 'Anger': return '#FF4500';
      case 'Fear': return '#800080';
      case 'Surprise': return '#32CD32';
      case 'Love': return '#FF69B4';
      case 'Neutral': return '#808080';
      default: return '#808080';
    }
  }};
  color: white;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: transform 0.2s;
  
  &:hover {
    transform: scale(1.05);
  }
`;

export const EmotionsContainer = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 20px 0;
  justify-content: center;
  width: 100%;
`;

export const AudioInput = styled.div`
  margin: 20px 0;
  width: 100%;
  text-align: center;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
`;

export const Button = styled.button`
  padding: 12px 24px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 1em;
  font-weight: 600;
  transition: all 0.2s;
  font-family: 'Roboto', sans-serif;
  margin: 0 5px;

  &:hover {
    background-color: #0056b3;
    transform: translateY(-1px);
  }

  &:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
`;

export const Input = styled.input`
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1em;
  font-family: 'Roboto', sans-serif;

  &:focus {
    outline: none;
    border-color: #007bff;
  }
`;

export const ErrorMessage = styled.div`
  color: #dc3545;
  text-align: center;
  margin: 1rem 0;
  padding: 10px;
  border-radius: 4px;
  background-color: #fff;
  border: 1px solid #dc3545;
`;

export const LoadingSpinner = styled.div`
  border: 3px solid #f3f3f3;
  border-radius: 50%;
  border-top: 3px solid #007bff;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
  margin: 0 auto;

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;
