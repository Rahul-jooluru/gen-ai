import React, { useEffect, useState } from "react";
import UploadBox from "../components/UploadBox";
import PhotoGrid from "../components/PhotoGrid";
import PhotoModal from "../components/PhotoModel";
import ChatSearch from "../components/ChatSearch";
import ContactsManager from "../components/ContactsManager";
import ShareHistory from "../components/ShareHistory";
import ReceivedShares from "../components/ReceivedShares";
import { uploadPhoto, fetchPhotos, deletePhoto, getUserProfile } from "../services/api";

const Dashboard = () => {
  const [photos, setPhotos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedPhoto, setSelectedPhoto] = useState(null);
  const [userProfile, setUserProfile] = useState(null);

  // Load all photos on mount
  useEffect(() => {
    loadPhotos();
    loadUserProfile();
  }, []);

  const loadUserProfile = async () => {
    try {
      const profile = await getUserProfile();
      setUserProfile(profile);
    } catch (err) {
      console.error("Failed to load user profile", err);
    }
  };

  const loadPhotos = async () => {
    setLoading(true);
    try {
      const data = await fetchPhotos();
      setPhotos(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Failed to load photos", err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (file) => {
    await uploadPhoto(file);
    loadPhotos();
  };

  const handleDelete = async (photoId) => {
    try {
      await deletePhoto(photoId);
      setSelectedPhoto(null);
      loadPhotos();
    } catch (err) {
      console.error("Failed to delete photo", err);
      alert("Failed to delete photo");
    }
  };

  const handleSearchResults = (results) => {
    setPhotos(results);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-semibold">DrishyaMitra</h1>
        <span className="text-sm text-gray-500">
          {userProfile ? `Hi ${userProfile.name}!` : "AI Photo Dashboard"}
        </span>
      </header>

      {/* Content */}
      <main className="max-w-7xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Left panel */}
        <div className="lg:col-span-1 space-y-6">
          <UploadBox onUpload={handleUpload} />
          <ChatSearch onResults={handleSearchResults} />
          <ContactsManager />
          <ReceivedShares />
          <ShareHistory />
        </div>

        {/* Right panel */}
        <div className="lg:col-span-3">
          <PhotoGrid
            photos={photos}
            isLoading={loading}
            onPhotoClick={setSelectedPhoto}
            onDelete={handleDelete}
          />
        </div>
      </main>

      {/* Modal */}
      <PhotoModal
        photo={selectedPhoto}
        onClose={() => setSelectedPhoto(null)}
      />
    </div>
  );
};

export default Dashboard;

