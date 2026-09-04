import React from 'react'
import MarkdownMessage from './MarkdownMessage';

const Chat = ({ messages }) => {
  return (
    <div className="flex flex-col h-full bg-gray-900 text-white p-5 overflow-y-auto">

      {messages.map((msg, index) => (
        <div
          key={index}
          className={`mb-5 ${
            msg.role === "user"
              ? "text-right"
              : "text-left"
          }`}
        >
          <div
            className={`inline-block p-4 rounded-xl max-w-[85%] text-lg ${
              msg.role === "user"
                ? "bg-blue-200 text-black"
                : "bg-gray-300 text-black"
            }`}
          >
            <MarkdownMessage content={msg.text} />
          </div>
        </div>
      ))}

    </div>
  );
};

export default Chat;