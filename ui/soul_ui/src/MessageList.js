import React from 'react';
import Message from './Message';
import './MessageList.css';

const MessageList = ({ messages }) => {
  return (
    <div className="message-list">
      {messages.map((msg, index) => (
        <Message key={index} text={msg.text} user={msg.user} />
      ))}
    </div>
  );
};

export default MessageList;
