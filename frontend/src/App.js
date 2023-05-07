import React, { useState } from "react";
import axios from "axios";
import MessageForm from "./components/MessageForm";
import MessageList from "./components/MessageList";

function App() {
  const [messages, setMessages] = useState([{ id: 0, text: "The order is late - what would you like to do?", role: "assistant" }]);

  const handleSendMessage = async (message) => {
    const userMessage = { id: messages.length, text: message, role: "user" };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    const payload = {
      user_input: message,
      conversation_history: messages.map((msg) => ({ text: msg.text, role: msg.role })),
    };

    try {
      const response = await axios.post("http://localhost:5000/api/converse", payload, {
        headers: {
          "Content-Type": "application/json",
        },
      });

      console.log("Response:", response);

      const assistantMessage = {
        id: messages.length + 1,
        text: response.data.assistant_response,
        role: "assistant",
      };
      setMessages((prevMessages) => [...prevMessages, assistantMessage]);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <header className="bg-white p-4 shadow-md">
        <h1 className="text-3xl font-semibold">Assistant</h1>
      </header>
      <main className="container mx-auto flex-grow flex flex-col p-4">
        <MessageList messages={messages} />
        <MessageForm onSubmit={handleSendMessage} />
      </main>
    </div>
  );
}

export default App;
