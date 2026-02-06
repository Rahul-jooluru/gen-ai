const BASE_URL = "http://localhost:5000";


export const fetchPhotos = async () => {
  const res = await fetch(`${BASE_URL}/api/photos`);

  if (!res.ok) {
    throw new Error("Failed to fetch photos");
  }

  return res.json();
};

/* -----------------------------
   Upload a photo
-------------------------------- */
export const uploadPhoto = async (file) => {
  const formData = new FormData();
  formData.append("image", file);

  const res = await fetch(`${BASE_URL}/api/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || "Upload failed");
  }

  return res.json();
};

/* -----------------------------
   Delete a photo
-------------------------------- */
export const deletePhoto = async (photoId) => {
  const res = await fetch(`${BASE_URL}/api/photos/${photoId}`, {
    method: "DELETE",
  });

  if (!res.ok) {
    throw new Error("Failed to delete photo");
  }

  return res.json();
};

/* -----------------------------
   Chat / AI search
-------------------------------- */
export const sendChatQuery = async (query) => {
  const res = await fetch(`${BASE_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query }),
  });

  if (!res.ok) {
    throw new Error("Chat request failed");
  }

  const data = await res.json();

  // Normalize backend response
  return {
    message: data.message || data.response || "Here’s what I found",
    photos: Array.isArray(data.photos) ? data.photos : [],
  };
};
/* -----------------------------
   Contacts Management
-------------------------------- */


export const fetchContacts = async () => {
  const res = await fetch(`${BASE_URL}/api/contacts`);

  if (!res.ok) {
    throw new Error("Failed to fetch contacts");
  }

  return res.json();
};

export const addContact = async (name, phone = "") => {
  const res = await fetch(`${BASE_URL}/api/contacts`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name, phone }),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || "Failed to add contact");
  }

  return res.json();
};

export const deleteContact = async (contactId) => {
  const res = await fetch(`${BASE_URL}/api/contacts/${contactId}`, {
    method: "DELETE",
  });

  if (!res.ok) {
    throw new Error("Failed to delete contact");
  }

  return res.json();
};

/* -----------------------------
   Share photos
-------------------------------- */
export const sharePhotos = async (photoIds, contactName) => {
  const res = await fetch(`${BASE_URL}/api/share`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ photo_ids: photoIds, contact_name: contactName }),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || "Failed to share photos");
  }

  return res.json();
};

/* USER PROFILE - Know who you are in the sharing system */
export const getUserProfile = async () => {
  const res = await fetch(`${BASE_URL}/api/user/profile`);

  if (!res.ok) {
    throw new Error("Failed to fetch user profile");
  }

  return res.json();
};

export const setUserProfile = async (name) => {
  const res = await fetch(`${BASE_URL}/api/user/profile`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name }),
  });

  if (!res.ok) {
    throw new Error("Failed to set user profile");
  }

  return res.json();
};

/* OPEN WHATSAPP WITH SHARED PHOTOS MESSAGE */
export const openWhatsAppShare = (whatsappLink) => {
  if (!whatsappLink) return;
  window.open(whatsappLink, "_blank");
};

/* SENT SHARES - Photos I've shared with others */
export const getSentShares = async () => {
  const res = await fetch(`${BASE_URL}/api/shares/sent`);

  if (!res.ok) {
    throw new Error("Failed to fetch sent shares");
  }

  return res.json();
};

/* RECEIVED SHARES - Photos others have shared TO me */

export const getSharedPhotos = async (contactName) => {
  const res = await fetch(
    `${BASE_URL}/api/shares/contact/${encodeURIComponent(contactName)}`
  );

  if (!res.ok) {
    throw new Error("Failed to fetch shared photos");
  }

  return res.json();
};

export const getShareHistory = async () => {
  const res = await fetch(`${BASE_URL}/api/share/history`);

  if (!res.ok) {
    throw new Error("Failed to fetch share history");
  }

  return res.json();
};

export const getReceivedShares = async () => {
  const res = await fetch("http://localhost:5000/api/received-shares");

  if (!res.ok) {
    throw new Error("Failed to fetch received shares");
  }

  return res.json();
};

