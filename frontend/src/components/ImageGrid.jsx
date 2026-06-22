import React from 'react';

const ImageGrid = ({ images }) => {
  const imageSections = [
    { key: 'original', title: 'Original Image' },
    { key: 'blur', title: 'Smoothing' },
    { key: 'threshold', title: 'Threshold' },
    { key: 'boundary', title: 'Boundary' }
  ];

  return (
    <div className="image-grid">
      {imageSections.map(section => (
        <div key={section.key} className="image-card">
          <h3>{section.title}</h3>
          {images[section.key] && (
            <img
              src={`data:image/jpeg;base64,${images[section.key]}`}
              alt={section.title}
            />
          )}
        </div>
      ))}
    </div>
  );
};

export default ImageGrid;