import React, { useEffect, useState } from "react";
import UploadBox from "../components/UploadBox";
import PhotoGrid from "../components/PhotoGrid";
import { uploadPhoto, fetchPhotos } from "../services/api";

const Dashboard = () => {
  const [photos, setPhotos] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch photos on load
  useEffect(() => {
    loadPhotos();
  }, []);

  const loadPhotos = async () => {
    setLoading(true);
    try {
      const data = await fetchPhotos();
      setPhotos(data);
    } catch (err) {
      console.error("Failed to load photos", err);
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (file) => {
    await uploadPhoto(file);
    loadPhotos(); // refresh grid after upload
  };

  const handlePhotoClick = (photo) => {
    console.log("Clicked photo:", photo);
    // later → open modal
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-semibold">DrishyaMitra</h1>
        <span className="text-sm text-gray-500">
          AI Photo Dashboard
        </span>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto p-6 space-y-6">
        {/* Upload */}
        <UploadBox onUpload={handleUpload} />

        {/* Gallery */}
        <PhotoGrid
          photos={photos}
          isLoading={loading}
          onPhotoClick={handlePhotoClick}
        />
      </main>
    </div>
  );
};

export default Dashboard;
