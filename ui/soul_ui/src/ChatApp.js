import React, { useState } from 'react';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import './ChatApp.css';

const ChatApp = () => {
  const [messages, setMessages] = useState([]);

  const addMessage = (message) => {
    const newMessage = { text: message, user: 'user' };
    setMessages([...messages, newMessage]);
    generateBotResponse();
  };

  const generateBotResponse = () => {
    const botMessage = { text: "This is an automatic response from Soul Canvas Bot.", user: 'bot' };
    setTimeout(() => {
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    }, 1000); // Delay of 1 second
  };

  return (
    <div className="chat-app">
      <header className="chat-header">
        <h1>Soul Canvas</h1>
      </header>
      <MessageList messages={messages} />
      <MessageInput addMessage={addMessage} />
    </div>
  );
};

export default ChatApp;
