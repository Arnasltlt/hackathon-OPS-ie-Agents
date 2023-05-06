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
    <form onSubmit={handleSubmit}>
      <label>
        Message:
        <input type="text" value={message} onChange={handleChange} />
      </label>
      <button type="submit">Send</button>
    </form>
  );
}

MessageForm.propTypes = {
  onSubmit: PropTypes.func.isRequired,
};

export default MessageForm;
