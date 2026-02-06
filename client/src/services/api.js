const BASE_URL = "http://localhost:5000";

/* -----------------------------
   Fetch all photos
-------------------------------- */
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
    throw new Error("Upload failed");
  }

  return res.json();
};

/* -----------------------------
   Chat / Natural language search
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

  return res.json();
};

/* -----------------------------
   (Optional) Share photos
-------------------------------- */
export const sharePhotos = async ({ photoIds, platform, recipient }) => {
  const res = await fetch(`${BASE_URL}/api/share`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      photo_ids: photoIds,
      platform,      // "email" | "whatsapp"
      recipient,     // email or phone
    }),
  });

  if (!res.ok) {
    throw new Error("Share failed");
  }

  return res.json();
};
