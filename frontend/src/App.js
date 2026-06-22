import React, { useState } from 'react';
import './App.css';
import Header from './components/Header';
import Upload from './components/Upload';
import ImageGrid from './components/ImageGrid';
import Result from './components/Result';

function App() {
  const [images, setImages] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImageUpload = async (file) => {
    setLoading(true);
    const formData = new FormData();
    formData.append('image', file);

    try {
      const response = await fetch('http://localhost:5000/process', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setImages(data.processedImages);
      setResult(data.prediction);
    } catch (error) {
      console.error('Error processing image:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <Header />
      <div className="container">
        <Upload onImageUpload={handleImageUpload} loading={loading} />
        {loading && <div className="loading">Processing Image...</div>}
        {Object.keys(images).length > 0 && <ImageGrid images={images} />}
        {result && <Result result={result} />}
      </div>
    </div>
  );
}

export default App;