import React, { useState } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hello! I am your AI Healthcare Assistant. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [patientId] = useState(1);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState('friendly');
  const [language, setLanguage] = useState('english');

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/chat/message?patient_id=${patientId}&message=${encodeURIComponent(input)}&mode=${mode}&language=${language}`,
        { method: 'POST', headers: { 'accept': 'application/json' } }
      );
      const data = await response.json();
      const botMessage = { 
        sender: 'bot', 
        text: data.response, 
        sentiment: data.sentiment,
        patientName: data.patient_name
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      setMessages(prev => [...prev, { sender: 'bot', text: 'Sorry, I am having trouble connecting. Please try again.' }]);
    }
    setLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') sendMessage();
  };

  const getModeIcon = () => {
    if (mode === 'doctor') return '👨‍⚕️';
    if (mode === 'emergency') return '🚨';
    return '🤖';
  };

  const getModeColor = () => {
    if (mode === 'doctor') return 'linear-gradient(135deg, #11998e, #38ef7d)';
    if (mode === 'emergency') return 'linear-gradient(135deg, #ff416c, #ff4b2b)';
    return 'linear-gradient(135deg, #667eea, #764ba2)';
  };

  return (
    <div className="app">
      <div className="header" style={{ background: getModeColor() }}>
        <h1>{getModeIcon()} इलाज BUDDY</h1>
      {/* <p>Powered by Groq AI • LLaMA 3.3 70B</p>*/}
      </div>

      <div className="controls">
        <div className="control-group">
          <label>Mode:</label>
          <select value={mode} onChange={(e) => setMode(e.target.value)}>
            <option value="friendly">🤝 Friendly</option>
            <option value="doctor">👨‍⚕️ Doctor</option>
            <option value="emergency">🚨 Emergency</option>
          </select>
        </div>
        <div className="control-group">
          <label>Language:</label>
          <select value={language} onChange={(e) => setLanguage(e.target.value)}>
            <option value="english">🇬🇧 English</option>
            <option value="hindi">🇮🇳 Hindi</option>
          </select>
        </div>
      </div>

      <div className="chat-container">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <div className="bubble">
              {msg.sender === 'bot' && <span className="bot-icon">{getModeIcon()} </span>}
              {msg.text}
              {msg.sentiment && <span className="sentiment"> [{msg.sentiment}]</span>}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message bot">
            <div className="bubble">{getModeIcon()} Thinking...</div>
          </div>
        )}
      </div>

      <div className="input-container">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your health question here..."
        />
        <button onClick={sendMessage} style={{ background: getModeColor() }}>Send</button>
      </div>
    </div>
  );
}

export default App;