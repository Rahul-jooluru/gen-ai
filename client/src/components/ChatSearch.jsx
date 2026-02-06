import React, { useState } from "react";
import { sendChatQuery } from "../services/api";

const ChatSearch = ({ onResults }) => {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Ask me about your photos 👋",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await sendChatQuery(input);

      const assistantMessage = {
        role: "assistant",
        content: res.message || "Here’s what I found",
      };

      setMessages((prev) => [...prev, assistantMessage]);

      // If backend returns photos
      if (res.photos && onResults) {
        onResults(res.photos);
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Something went wrong 😕" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white border rounded-xl shadow-sm">
      {/* Header */}
      <div className="px-4 py-3 border-b font-medium">
        AI Photo Assistant
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3 text-sm">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`max-w-[80%] px-3 py-2 rounded-lg ${
              msg.role === "user"
                ? "ml-auto bg-blue-600 text-white"
                : "bg-gray-100 text-gray-800"
            }`}
          >
            {msg.content}
          </div>
        ))}

        {loading && (
          <div className="bg-gray-100 text-gray-500 px-3 py-2 rounded-lg w-fit">
            Thinking…
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-3 border-t flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="e.g. Show photos with mom"
          className="flex-1 border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring"
        />
        <button
          onClick={handleSend}
          className="bg-blue-600 text-white px-4 rounded-lg text-sm hover:bg-blue-700 transition"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatSearch;
