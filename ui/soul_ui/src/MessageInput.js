import React, { useState } from 'react';
import './MessageInput.css';

const MessageInput = ({ addMessage }) => {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim()) {
      addMessage(input);
      setInput('');
    }
  };

  return (
    <div className="message-input">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type a message..."
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
};

export default MessageInput;
