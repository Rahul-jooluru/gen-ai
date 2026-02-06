import React, { useState, useEffect } from "react";
import { getShareHistory, openWhatsAppShare } from "../services/api";

const ShareHistory = () => {
  const [shares, setShares] = useState([]);
  const [isExpanded, setIsExpanded] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const loadShareHistory = async () => {
    setIsLoading(true);
    try {
      const data = await getShareHistory();
      setShares(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Failed to load share history", err);
      setShares([]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (isExpanded) {
      loadShareHistory();
    }
  }, [isExpanded]);

  const generateWhatsAppLink = (share) => {
    if (!share.to_phone) return null;
    const phone = share.to_phone.replace(/\s|-/g, "");
    const withCountry = phone.startsWith("+") ? phone.replace("+", "") : (phone.length === 10 ? `91${phone}` : phone);
    const message = `📸 Share History: ${share.from} shared ${share.photo_count} photo(s) with you!\n⏰ ${new Date(share.shared_at).toLocaleDateString()}`;
    return `https://wa.me/${withCountry}?text=${encodeURIComponent(message)}`;
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-4">
      {/* Header */}
      <div className="flex justify-between items-center mb-4">
        <h3 className="font-semibold text-gray-800">📤 Share History</h3>
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-sm bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded transition"
        >
          {isExpanded ? "Hide" : "View"}
        </button>
      </div>

      {/* Share History List */}
      {isExpanded && (
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {isLoading ? (
            <p className="text-sm text-gray-500">Loading...</p>
          ) : shares.length === 0 ? (
            <p className="text-sm text-gray-400">No shares yet</p>
          ) : (
            shares
              .filter(s => s.type === "sent")
              .map((share) => (
                <div
                  key={share.id}
                  className="p-3 bg-blue-50 rounded-lg border border-blue-200"
                >
                  {/* Share Info */}
                  <div className="mb-2">
                    <p className="text-sm font-semibold text-gray-800">
                      👤 {share.to}
                    </p>
                    {share.to_phone && (
                      <p className="text-xs text-gray-500">{share.to_phone}</p>
                    )}
                    <p className="text-xs text-gray-500 mt-1">
                      📸 {share.photo_count} photo{share.photo_count !== 1 ? "s" : ""} •{" "}
                      {new Date(share.shared_at).toLocaleDateString()}
                    </p>
                  </div>

                  {/* Shared Photos Preview */}
                  {share.photos && share.photos.length > 0 && (
                    <div className="mt-2">
                      <p className="text-xs font-medium text-gray-600 mb-2">
                        Shared Photos:
                      </p>
                      <div className="flex gap-2 flex-wrap">
                        {share.photos.slice(0, 4).map((photo) => (
                          <img
                            key={photo.id}
                            src={photo.url}
                            alt="Shared photo"
                            className="w-12 h-12 rounded object-cover border border-blue-300"
                            title={photo.tags?.join(", ")}
                          />
                        ))}
                        {share.photos.length > 4 && (
                          <div className="w-12 h-12 rounded bg-blue-200 flex items-center justify-center text-xs font-semibold text-blue-700">
                            +{share.photos.length - 4}
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  {/* WhatsApp Button */}
                  {share.to_phone && (
                    <button
                      onClick={() => {
                        const link = generateWhatsAppLink(share);
                        if (link) openWhatsAppShare(link);
                      }}
                      className="mt-2 w-full px-2 py-1 bg-green-500 hover:bg-green-600 text-white text-xs rounded transition font-semibold"
                    >
                      💬 Open WhatsApp
                    </button>
                  )}
                </div>
              ))
          )}
        </div>
      )}
    </div>
  );
};

export default ShareHistory;
