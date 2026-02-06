import React from "react";

const PhotoGrid = ({ photos = [], isLoading = false, onPhotoClick }) => {
  if (isLoading) {
    return (
      <div className="w-full text-center py-10 text-gray-500">
        Loading photos...
      </div>
    );
  }

  if (!photos.length) {
    return (
      <div className="w-full text-center py-10 text-gray-400">
        No photos found
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
      {photos.map((photo) => (
        <div
          key={photo.id}
          onClick={() => onPhotoClick?.(photo)}
          className="relative cursor-pointer overflow-hidden rounded-xl shadow-sm hover:shadow-md transition"
        >
          <img
            src={photo.url}
            alt={photo.alt || "Photo"}
            className="w-full h-40 object-cover hover:scale-105 transition-transform duration-300"
          />

          {/* Optional overlay */}
          <div className="absolute inset-0 bg-black/0 hover:bg-black/20 transition" />
        </div>
      ))}
    </div>
  );
};

export default PhotoGrid;
