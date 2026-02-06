import React, { useRef, useState, useEffect } from "react";

const UploadBox = ({ onUpload }) => {
  const fileInputRef = useRef(null);
  const [preview, setPreview] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  // Cleanup preview URL to avoid memory leak
  useEffect(() => {
    return () => {
      if (preview) URL.revokeObjectURL(preview);
    };
  }, [preview]);

  const handleFile = async (file) => {
    if (!file || !file.type.startsWith("image/")) return;

    const previewUrl = URL.createObjectURL(file);
    setPreview(previewUrl);
    setIsUploading(true);

    try {
      await onUpload(file);
    } catch (err) {
      console.error("Upload failed", err);
      setPreview(null);
    } finally {
      setIsUploading(false);
    }
  };

  const handleChange = (e) => {
    const file = e.target.files[0];
    handleFile(file);
    e.target.value = ""; // allow re-upload same file
  };

  const handleDrop = (e) => {
    e.preventDefault();
    handleFile(e.dataTransfer.files[0]);
  };

  return (
    <div
      onClick={() => fileInputRef.current?.click()}
      onDragOver={(e) => e.preventDefault()}
      onDrop={handleDrop}
      className="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center cursor-pointer hover:border-gray-400 transition"
    >
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleChange}
        hidden
      />

      {preview ? (
        <div className="flex flex-col items-center gap-2">
          <img
            src={preview}
            alt="Preview"
            className="w-32 h-32 object-cover rounded-lg"
          />
          {isUploading ? (
            <p className="text-sm text-gray-500">Uploading...</p>
          ) : (
            <p className="text-sm text-green-600">Upload complete</p>
          )}
        </div>
      ) : (
        <div>
          <p className="text-gray-600 font-medium">
            Click or drag image to upload
          </p>
          <p className="text-sm text-gray-400">
            JPG, PNG supported
          </p>
        </div>
      )}
    </div>
  );
};

export default UploadBox;
