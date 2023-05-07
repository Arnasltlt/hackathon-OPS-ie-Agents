import React, { useState } from "react";
import PropTypes from "prop-types";

function MessageForm(props) {
  const [message, setMessage] = useState("");

  function handleChange(event) {
    setMessage(event.target.value);
  }

  function handleSubmit(event) {
    event.preventDefault();
    props.onSubmit(message);
    setMessage("");
  }

  return (
    <form onSubmit={handleSubmit} className="mt-auto p-4 bg-gray-100">
      <div className="flex items-center space-x-4">
        <label className="m-5">
          <input type="text" value={message} onChange={handleChange} className="w-full px-10 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:border-blue-300" placeholder="Type your message here..." />
        </label>
        <button type="submit" className="px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg">
          Send
        </button>
      </div>
    </form>
  );
}

MessageForm.propTypes = {
  onSubmit: PropTypes.func.isRequired,
};

export default MessageForm;
