import React, { useState, useEffect } from "react";
import { fetchContacts, sharePhotos, openWhatsAppShare } from "../services/api";

const PhotoModal = ({ photo, onClose, onShare }) => {
  const [contacts, setContacts] = useState([]);
  const [selectedContact, setSelectedContact] = useState("");
  const [isSharing, setIsSharing] = useState(false);
  const [shareMessage, setShareMessage] = useState("");
  const [whatsappLink, setWhatsappLink] = useState("");

  useEffect(() => {
    loadContacts();
  }, [photo]);

  const loadContacts = async () => {
    try {
      const data = await fetchContacts();
      setContacts(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Failed to load contacts", err);
    }
  };

  const handleShare = async () => {
    if (!selectedContact) {
      setShareMessage("Please select a contact");
      return;
    }

    setIsSharing(true);
    try {
      const contact = contacts.find(c => c.id === selectedContact);
      const response = await sharePhotos([photo.id], contact.name);
      
      // Get WhatsApp link from response
      const link = response.whatsapp_link;
      setWhatsappLink(link);
      
      setShareMessage(`✅ Shared with ${contact.name}!`);
      onShare?.(photo.id, contact.name);
      
      // Auto-open WhatsApp after 1 second
      setTimeout(() => {
        if (link) {
          openWhatsAppShare(link);
        }
      }, 1000);
      
      setTimeout(() => {
        setShareMessage("");
        setSelectedContact("");
      }, 2000);
    } catch (err) {
      setShareMessage(`❌ Failed: ${err.message}`);
    } finally {
      setIsSharing(false);
    }
  };

  if (!photo) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
      {/* Backdrop */}
      <div className="absolute inset-0" onClick={onClose} />

      {/* Modal */}
      <div className="relative bg-white rounded-xl shadow-xl max-w-4xl w-full mx-4 overflow-hidden">
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-gray-500 hover:text-gray-800 z-10"
        >
          ✕
        </button>

        <div className="grid grid-cols-1 md:grid-cols-2">
          {/* Image */}
          <div className="bg-black flex items-center justify-center">
            <img
              src={photo.url}
              alt="Photo preview"
              className="max-h-[80vh] object-contain"
            />
          </div>

          {/* Info panel */}
          <div className="p-6 space-y-4 overflow-y-auto max-h-[80vh]">
            <h2 className="text-lg font-semibold">Photo Details</h2>

            {/* Tags */}
            <div>
              <p className="text-sm font-medium text-gray-600 mb-2">Tags</p>
              <div className="flex flex-wrap gap-2">
                {Array.isArray(photo.tags) && photo.tags.length > 0 ? (
                  photo.tags.map((tag, idx) => (
                    <span
                      key={idx}
                      className="bg-blue-100 text-blue-800 text-sm px-3 py-1 rounded-full"
                    >
                      {tag}
                    </span>
                  ))
                ) : (
                  <span className="text-sm text-gray-400">No tags detected</span>
                )}
              </div>
            </div>

            {/* Date */}
            {photo.date && (
              <div>
                <p className="text-sm font-medium text-gray-600">Date</p>
                <p className="text-sm text-gray-800">
                  {new Date(photo.date).toLocaleDateString()}
                </p>
              </div>
            )}

            {/* Share Section */}
            <div className="pt-4 border-t space-y-3">
              <p className="text-sm font-medium text-gray-700">📱 Share Photo</p>
              
              <select
                value={selectedContact}
                onChange={(e) => setSelectedContact(e.target.value)}
                className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Select a contact...</option>
                {contacts.map((contact) => (
                  <option key={contact.id} value={contact.id}>
                    {contact.name} {contact.phone ? `(${contact.phone})` : ""}
                  </option>
                ))}
              </select>

              <div className="flex gap-2">
                <button
                  onClick={handleShare}
                  disabled={!selectedContact || isSharing}
                  className={`flex-1 px-4 py-2 rounded-lg text-sm font-semibold transition ${
                    selectedContact && !isSharing
                      ? "bg-blue-500 hover:bg-blue-600 text-white"
                      : "bg-gray-200 text-gray-500 cursor-not-allowed"
                  }`}
                >
                  {isSharing ? "Sharing..." : "📤 Share"}
                </button>

                <button
                  onClick={handleShare}
                  disabled={!selectedContact || isSharing}
                  className={`flex-1 px-4 py-2 rounded-lg text-sm font-semibold transition flex items-center justify-center gap-1 ${
                    selectedContact && !isSharing
                      ? "bg-green-500 hover:bg-green-600 text-white"
                      : "bg-gray-200 text-gray-500 cursor-not-allowed"
                  }`}
                >
                  💬 WhatsApp
                </button>
              </div>

              {shareMessage && (
                <p className="text-sm text-center font-medium text-gray-700">
                  {shareMessage}
                </p>
              )}
            </div>

            {/* Download */}
            <div className="pt-2">
              <a
                href={photo.url}
                download
                className="block w-full px-4 py-2 text-center text-sm border rounded-lg hover:bg-gray-100 transition"
              >
                ⬇️ Download
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PhotoModal;

