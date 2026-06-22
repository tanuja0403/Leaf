import React, { useRef } from 'react';

const Upload = ({ onImageUpload, loading }) => {
  const fileInputRef = useRef(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
      onImageUpload(file);
    } else {
      alert('Please select a valid image file.');
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="upload-section">
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileSelect}
        accept="image/*"
        style={{ display: 'none' }}
      />
      <button
        className="upload-btn"
        onClick={handleButtonClick}
        disabled={loading}
      >
        {loading ? 'Processing...' : 'Search Image'}
      </button>
    </div>
  );
};

export default Upload;