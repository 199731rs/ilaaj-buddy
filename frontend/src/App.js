import React, { useState } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hey! Main hoon Ilaaj Buddy 💊 Tera sehat ka bestie! Bata, kya hua? 😊' }
  ]);
  const [input, setInput] = useState('');
  const [patientId] = useState(1);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState('friendly');
  const [language, setLanguage] = useState('english');
  const [showSettings, setShowSettings] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    try {
      const response = await fetch(
        `https://ilaaj-buddy-backend.onrender.com/chat/message?patient_id=${patientId}&message=${encodeURIComponent(input)}&mode=${mode}&language=${language}`,
        { method: 'POST', headers: { 'accept': 'application/json' } }
      );
      const data = await response.json();
      setMessages(prev => [...prev, {
        sender: 'bot',
        text: data.response,
        sentiment: data.sentiment
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        sender: 'bot',
        text: 'Sorry, having trouble connecting. Please try again. 😔'
      }]);
    }
    setLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') sendMessage();
  };

  const getModeIcon = () => {
    if (mode === 'doctor') return '👨‍⚕️';
    if (mode === 'emergency') return '🚨';
    return '💊';
  };

  const getModeColor = () => {
    if (mode === 'doctor') return '#11998e';
    if (mode === 'emergency') return '#ff416c';
    return '#1976D2';
  };

  return (
    <div className="app">
      {/* HEADER */}
      <div className="header" style={{ borderBottom: `3px solid ${getModeColor()}` }}>
        <div className="header-left">
          <div className="avatar" style={{ background: getModeColor() }}>
            {getModeIcon()}
            <span className="online-dot"></span>
          </div>
          <div className="header-info">
            <h1>Ilaaj Buddy</h1>
            <p>AI Health Assistant • Online</p>
          </div>
        </div>
        <div className="header-right">
          <button className="icon-btn" onClick={() => setShowSettings(!showSettings)}>⚙️</button>
        </div>
      </div>

      {/* SETTINGS DROPDOWN */}
      {showSettings && (
        <div className="settings-panel">
          <div className="setting-item">
            <span>Mode</span>
            <select value={mode} onChange={(e) => { setMode(e.target.value); setShowSettings(false); }}>
              <option value="friendly">🤝 Friendly</option>
              <option value="doctor">👨‍⚕️ Doctor</option>
              <option value="emergency">🚨 Emergency</option>
            </select>
          </div>
          <div className="setting-item">
            <span>Language</span>
            <select value={language} onChange={(e) => { setLanguage(e.target.value); setShowSettings(false); }}>
              <option value="english">🇬🇧 English</option>
              <option value="hindi">🇮🇳 Hindi</option>
            </select>
          </div>
        </div>
      )}

      {/* MODE BADGE */}
      <div className="mode-badge" style={{ background: getModeColor() + '20', color: getModeColor() }}>
        {getModeIcon()} {mode.charAt(0).toUpperCase() + mode.slice(1)} Mode • {language === 'hindi' ? '🇮🇳 Hindi' : '🇬🇧 English'}
      </div>

      {/* CHAT */}
      <div className="chat-container">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.sender === 'bot' && (
              <div className="bot-avatar" style={{ background: getModeColor() }}>
                {getModeIcon()}
              </div>
            )}
            <div className="bubble-wrapper">
              <div className={`bubble ${msg.sender}`}>
                {msg.text}
              </div>
              {/* /* {msg.sentiment && (
                <span className="sentiment">{msg.sentiment}</span>
              )} */ }
              {msg.sender === 'user' && <span className="read-receipt">Read</span>}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message bot">
            <div className="bot-avatar" style={{ background: getModeColor() }}>
              {getModeIcon()}
            </div>
            <div className="bubble bot">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* INPUT */}
      <div className="input-container">
        <div className="input-wrapper">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Write a message..."
          />
          <button className="emoji-btn">😊</button>
        </div>
        <button
          className="send-btn"
          onClick={sendMessage}
          style={{ background: getModeColor() }}
        >
          ➤
        </button>
      </div>

      {/* FOOTER */}
      <div className="footer">
        Powered by <strong>Ilaaj Buddy AI</strong> 💊
      </div>
    </div>
  );
}

export default App;