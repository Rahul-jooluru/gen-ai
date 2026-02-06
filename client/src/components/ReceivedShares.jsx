import React, { useEffect, useState } from "react";
import { getReceivedShares } from "../services/api";

export default function ReceivedShares() {
  const [receivedShares, setReceivedShares] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState(null);

  useEffect(() => {
    loadShares();
  }, []);

  const loadShares = async () => {
    try {
      const shares = await getReceivedShares();
      setReceivedShares(shares || []);
    } catch (err) {
      console.error("Failed to load received shares", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gradient-to-b from-blue-50 to-blue-100 border border-blue-300 rounded-lg p-4">
      <div className="flex justify-between items-center mb-3">
        <h3 className="text-lg font-bold text-blue-900">📥 Shared With Me</h3>
        <span className="bg-blue-200 px-3 py-1 rounded-full text-sm font-semibold">
          {receivedShares.length}
        </span>
      </div>

      {loading ? (
        <p className="text-center text-blue-700">Loading...</p>
      ) : receivedShares.length === 0 ? (
        <p className="text-center text-blue-600 py-4">
          No photos shared with you yet
        </p>
      ) : (
        <div className="space-y-2">
          {receivedShares.map((share, idx) => (
            <div key={idx} className="bg-white rounded border overflow-hidden">
              <button
                onClick={() => setExpanded(expanded === idx ? null : idx)}
                className="w-full px-3 py-2 flex justify-between hover:bg-blue-50"
              >
                <div className="text-left">
                  <p className="font-semibold text-blue-900">
                    {share.from || "Someone"} shared photos
                  </p>
                  <p className="text-xs text-gray-500">
                    {share.photo_count || share.photo_ids?.length || 0} photo(s)
                  </p>
                </div>
                <span>{expanded === idx ? "▲" : "▼"}</span>
              </button>

              {expanded === idx && (
                <div className="p-3 bg-blue-50 border-t">
                  <p className="text-xs text-gray-600 mb-2">
                    Status: <strong>{share.status || "unread"}</strong>
                  </p>

                  <button
                    onClick={() => {
                      const msg = "✨ Thanks for sharing the photos!";
                      window.open(
                        `https://wa.me/?text=${encodeURIComponent(msg)}`,
                        "_blank"
                      );
                    }}
                    className="w-full bg-green-500 hover:bg-green-600 text-white py-1 rounded text-xs font-semibold"
                  >
                    💬 Reply on WhatsApp
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
