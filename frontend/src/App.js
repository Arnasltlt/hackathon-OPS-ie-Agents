import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [userInput, setUserInput] = useState('');

  const handleUserInputChange = (event) => {
    setUserInput(event.target.value);
  };

  const handleClick = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/converse', {
        user_input: userInput,
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      console.log(response.data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      <h1>Assistant</h1>
      <input
        type="text"
        value={userInput}
        onChange={handleUserInputChange}
        placeholder="Type your message here..."
      />
      <button onClick={handleClick}>Send</button>
    </div>
  );
}

export default App;
