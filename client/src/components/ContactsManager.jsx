import React, { useState, useEffect } from "react";
import { fetchContacts, addContact, deleteContact } from "../services/api";

const ContactsManager = () => {
  const [contacts, setContacts] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [newContactName, setNewContactName] = useState("");
  const [newContactPhone, setNewContactPhone] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    loadContacts();
  }, []);

  const loadContacts = async () => {
    try {
      const data = await fetchContacts();
      setContacts(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Failed to load contacts", err);
    }
  };

  const handleAddContact = async (e) => {
    e.preventDefault();
    if (!newContactName.trim()) return;

    setIsLoading(true);
    try {
      await addContact(newContactName, newContactPhone);
      setNewContactName("");
      setNewContactPhone("");
      loadContacts();
    } catch (err) {
      alert(`Failed to add contact: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteContact = async (contactId) => {
    if (!window.confirm("Delete this contact?")) return;

    try {
      await deleteContact(contactId);
      loadContacts();
    } catch (err) {
      alert(`Failed to delete contact: ${err.message}`);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-4">
      {/* Header */}
      <div className="flex justify-between items-center mb-4">
        <h3 className="font-semibold text-gray-800">👥 Contacts</h3>
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="text-sm bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded transition"
        >
          {isOpen ? "Done" : "Manage"}
        </button>
      </div>

      {/* Contacts List */}
      <div className="space-y-2 max-h-48 overflow-y-auto">
        {contacts.length === 0 ? (
          <p className="text-sm text-gray-400">No contacts yet</p>
        ) : (
          contacts.map((contact) => (
            <div
              key={contact.id}
              className="flex justify-between items-center p-2 bg-gray-50 rounded-lg"
            >
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-800">
                  {contact.name}
                </p>
                {contact.phone && (
                  <p className="text-xs text-gray-500">{contact.phone}</p>
                )}
              </div>
              {isOpen && (
                <button
                  onClick={() => handleDeleteContact(contact.id)}
                  className="ml-2 text-red-500 hover:text-red-700 text-sm"
                >
                  ✕
                </button>
              )}
            </div>
          ))
        )}
      </div>

      {/* Add Contact Form */}
      {isOpen && (
        <form onSubmit={handleAddContact} className="mt-4 pt-4 border-t space-y-3">
          <input
            type="text"
            placeholder="Contact name"
            value={newContactName}
            onChange={(e) => setNewContactName(e.target.value)}
            className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="tel"
            placeholder="Phone (optional)"
            value={newContactPhone}
            onChange={(e) => setNewContactPhone(e.target.value)}
            className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={isLoading || !newContactName.trim()}
            className="w-full px-3 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg text-sm font-semibold transition disabled:bg-gray-300"
          >
            {isLoading ? "Adding..." : "Add Contact"}
          </button>
        </form>
      )}
    </div>
  );
};

export default ContactsManager;
