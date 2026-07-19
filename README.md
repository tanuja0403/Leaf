# Leaf Recognition System

A complete machine learning application for identifying leaf species using image processing and classification.

## Features

- **Image Upload**: Upload leaf images through a clean web interface
- **Image Processing**: Automatic preprocessing including smoothing, thresholding, and boundary extraction
- **ML Classification**: Naive Bayes classification trained on the Flavia leaf dataset
- **Results Display**: Shows processed images and identification results with Wikipedia links
- **Modern UI**: Clean, responsive design with smooth animations

## Project Structure

```
leaf-recognition-system/
├── frontend/          # React application
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── Upload.jsx
│   │   │   ├── ImageGrid.jsx
│   │   │   └── Result.jsx
│   │   ├── App.js
│   │   └── App.css
│   └── package.json
├── backend/           # Flask API
│   ├── app.py
│   └── requirements.txt
├── ml/               # Machine Learning code
│   └── leaf_classifier.py
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask server:
   ```bash
   python app.py
   ```

The backend will start on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```

The frontend will start on `http://localhost:3000`

## Usage

1. Open the application in your browser
2. Click "Search Image" to upload a leaf image
3. Wait for processing (you'll see a loading indicator)
4. View the processed images in the 4-column grid:
   - Original: Your uploaded image
   - Smoothing: Blurred version
   - Threshold: Binary image
   - Boundary: Edge detection
5. See the identified leaf species name
6. Click the Wikipedia link to learn more about the species

## Technical Details

### Image Processing Pipeline
1. **Background Subtraction**: Remove background noise
2. **Gaussian Blur**: Smooth the image
3. **Thresholding**: Convert to binary image
4. **Boundary Extraction**: Detect leaf edges
5. **Feature Extraction**: Calculate shape, color, and texture features

### Machine Learning
- **Algorithm**: Multinomial Naive Bayes
- **Features**: 17 features including area, perimeter, color statistics, and texture metrics
- **Dataset**: Flavia leaf dataset with 32 species
- **Training**: Automatic model training on startup

### API Endpoints
- `POST /process`: Process uploaded image and return classification
- `GET /health`: Health check endpoint

## Dependencies

### Backend
- Flask
- OpenCV
- NumPy
- Pandas
- Scikit-learn
- Pillow
- Mahotas

### Frontend
- React
- Axios
- Bootstrap

## Dataset

The system uses the Flavia leaf dataset which should be located at:
- `../Flavia py files/Flavia_features.csv` (features)
- `../Flavia leaves dataset/` (images)
- 
# Homepage

![Homepage Screenshot](assets/homepage.jpeg)

# Sample Leaf 1

![Leaf 1](assets/leaf1.jpeg)

# Sample Leaf 2

![Leaf 2](assets/leaf2.jpeg)

# Sample Leaf 3

![Leaf 3](assets/leaf3.jpeg)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes.
