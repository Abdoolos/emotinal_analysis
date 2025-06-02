import React from 'react';
import EmotionDisplay from './components/EmotionDisplay';
import styled, { createGlobalStyle } from 'styled-components';

const GlobalStyle = createGlobalStyle`
  @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
  
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: 'Roboto', sans-serif;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    min-height: 100vh;
  }
`;

const AppContainer = styled.div`
  min-height: 100vh;
  padding: 2rem;
`;

const Title = styled.h1`
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 2.5rem;
  font-weight: 700;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
`;

const Footer = styled.footer`
  text-align: center;
  padding: 1rem;
  color: #2c3e50;
  font-size: 0.9rem;
  margin-top: 2rem;
`;

function App() {
  return (
    <>
      <GlobalStyle />
      <AppContainer>
        <Title>Emotion Detection System</Title>
        <EmotionDisplay />
        <Footer>
          Designed by Abdullah Alawiss
        </Footer>
      </AppContainer>
    </>
  );
}

export default App;
