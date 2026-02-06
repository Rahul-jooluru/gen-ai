import React from "react";

const PhotoModal = ({ photo, onClose }) => {
  if (!photo) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
      {/* Backdrop click */}
      <div
        className="absolute inset-0"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="relative bg-white rounded-xl shadow-xl max-w-4xl w-full mx-4 overflow-hidden">
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-gray-500 hover:text-gray-800"
        >
          ✕
        </button>

        <div className="grid grid-cols-1 md:grid-cols-2">
          {/* Image */}
          <div className="bg-black flex items-center justify-center">
            <img
              src={photo.url}
              alt="Preview"
              className="max-h-[80vh] object-contain"
            />
          </div>

          {/* Info panel */}
          <div className="p-6 space-y-4">
            <h2 className="text-lg font-semibold">
              Photo Details
            </h2>

            {/* Tags */}
            <div>
              <p className="text-sm font-medium text-gray-600 mb-1">
                Tags
              </p>
              <div className="flex flex-wrap gap-2">
                {photo.tags?.length ? (
                  photo.tags.map((tag, idx) => (
                    <span
                      key={idx}
                      className="bg-gray-100 text-sm px-3 py-1 rounded-full"
                    >
                      {tag}
                    </span>
                  ))
                ) : (
                  <span className="text-sm text-gray-400">
                    No tags detected
                  </span>
                )}
              </div>
            </div>

            {/* Date */}
            {photo.date && (
              <div>
                <p className="text-sm font-medium text-gray-600">
                  Date
                </p>
                <p className="text-sm text-gray-800">
                  {photo.date}
                </p>
              </div>
            )}

            {/* Future actions */}
            <div className="pt-4 border-t flex gap-3">
              <button className="px-4 py-2 text-sm border rounded-lg hover:bg-gray-100">
                Share
              </button>
              <button className="px-4 py-2 text-sm border rounded-lg hover:bg-gray-100">
                Download
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PhotoModal;
