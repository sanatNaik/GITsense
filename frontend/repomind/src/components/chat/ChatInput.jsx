import { useState } from "react";

const ChatInput = ({ onSend }) => {
  const [query, setQuery] = useState("");

  const handleSend = () => {
    if (!query.trim()) return;

    onSend(query);
    setQuery("");
  };

  return (
    <div className="flex p-4 bg-gray-200">

      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            handleSend();
          }
        }}
        placeholder="Ask about the repo..."
        className="flex-1 p-3 rounded-l-lg text-black text-lg outline-none"
      />

      <button
        onClick={handleSend}
        className="bg-blue-500 text-white font-semibold px-5 rounded-r-lg text-lg hover:bg-blue-600"
      >
        Send
      </button>

    </div>
  );
};

export default ChatInput;