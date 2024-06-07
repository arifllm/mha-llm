import React from 'react';
import './Message.css';

const Message = ({ text, user }) => {
  return (
    <div className={`message ${user === 'bot' ? 'bot-message' : 'user-message'}`}>
      <p>{text}</p>
    </div>
  );
};

export default Message;
