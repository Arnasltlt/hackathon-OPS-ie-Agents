import React from "react";
import PropTypes from "prop-types";

const MessageList = ({ messages }) => {
  return (
    <div className="flex-grow overflow-auto mb-4">
      <h2 className="text-2xl font-bold mb-2">Messages:</h2>
      <ul className="space-y-2">
        {messages.map((message, index) => (
          <li key={index} className={`p-3 rounded-lg ${message.role === "user" ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-900"}`}>
            {message.text}
          </li>
        ))}
      </ul>
    </div>
  );
};

MessageList.propTypes = {
  messages: PropTypes.arrayOf(
    PropTypes.shape({
      text: PropTypes.string.isRequired,
      role: PropTypes.string.isRequired,
    })
  ).isRequired,
};

export default MessageList;
