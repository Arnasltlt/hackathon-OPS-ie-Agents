import React, { useState } from "react";
import axios from "axios";
import MessageForm from "./components/MessageForm";
import MessageList from "./components/MessageList";

function App() {
  const [messages, setMessages] = useState([
    {
      id: 0,
      text: "The order is late - what would you like to do?",
      role: "assistant",
    },
  ]);

  const handleSendMessage = async (message) => {
    const userMessage = { id: messages.length, text: message, role: "user" };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    try {
      const response = await axios.post(
        "http://localhost:5000/api/converse",
        {
          user_input: message,
          conversation_history: messages,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      const assistantMessage = {
        id: messages.length + 1, // Updated line
        text: response.data.assistant_response,
        role: "assistant",
      };
      setMessages((prevMessages) => [...prevMessages, assistantMessage]);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="App">
      <h1>Assistant</h1>
      <MessageList messages={messages} />
      <MessageForm onSubmit={handleSendMessage} />
    </div>
  );
}

export default App;
