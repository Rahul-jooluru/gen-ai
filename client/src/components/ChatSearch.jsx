import React, { useState } from "react";
import { sendChatQuery } from "../services/api";

const ChatSearch = ({ onResults }) => {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "Ask me about your photos 👋" },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userText = input.trim();
    setInput("");

    setMessages((prev) => [
      ...prev,
      { role: "user", content: userText },
    ]);

    setLoading(true);

    try {
      const res = await sendChatQuery(userText);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: res?.message ?? "Here’s what I found 👇",
        },
      ]);

      if (Array.isArray(res?.photos) && onResults) {
        onResults(res.photos);
      }
    } catch (err) {
      console.error("Chat error:", err);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Something went wrong 😕 Try again.",
        },
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
          placeholder="e.g. show outdoor photos"
          className="flex-1 border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring"
        />
        <button
          onClick={handleSend}
          disabled={loading}
          className="bg-blue-600 text-white px-4 rounded-lg text-sm hover:bg-blue-700 transition disabled:opacity-50"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatSearch;
