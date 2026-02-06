import React from "react";

const PhotoGrid = ({ photos = [], isLoading = false, onPhotoClick, onDelete }) => {
  if (isLoading) {
    return (
      <div className="w-full text-center py-10 text-gray-500">
        Loading photos...
      </div>
    );
  }

  if (!Array.isArray(photos) || photos.length === 0) {
    return (
      <div className="w-full text-center py-10 text-gray-400">
        No photos found
      </div>
    );
  }

  const handleDelete = (e, photo) => {
    e.stopPropagation();
    if (window.confirm("Delete this photo?")) {
      onDelete?.(photo.id);
    }
  };

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
      {photos.map((photo) => (
        <div
          key={photo.id}
          onClick={() => onPhotoClick?.(photo)}
          className="relative cursor-pointer overflow-hidden rounded-xl shadow-sm hover:shadow-md transition group"
        >
          <img
            src={photo.url}
            alt="Photo"
            className="w-full h-40 object-cover group-hover:scale-105 transition-transform duration-300"
            loading="lazy"
          />

          {/* Hover overlay with delete button */}
          <div className="absolute inset-0 bg-black/0 group-hover:bg-black/40 transition flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
            <button
              onClick={(e) => handleDelete(e, photo)}
              className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded-lg text-sm font-semibold transition"
            >
              Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default PhotoGrid;

