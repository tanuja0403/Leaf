from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import mahotas as mt
import base64
import io
from sklearn.naive_bayes import MultinomialNB
import os

app = Flask(__name__)
CORS(app)

# Global variables for model and data
model = None
dataset = None

def load_model():
    global model, dataset

    # Load dataset
    dataset_path = '../../Flavia py files/Flavia_features.csv'
    if os.path.exists(dataset_path):
        dataset = pd.read_csv(dataset_path)
    else:
        # Create sample dataset if not found
        print("Dataset not found, using sample data")
        return

    # Load or train model
    ds_path = '../../Flavia leaves dataset'
    if os.path.exists(ds_path):
        img_files = os.listdir(ds_path)

        breakpoints = [1001,1059,1060,1122,1552,1616,1123,1194,1195,1267,1268,1323,1324,1385,1386,1437,1497,1551,1438,1496,2001,2050,\
                       2051,2113,2114,2165,2166,2230,2231,2290,2291,2346,2347,2423,2424,2485,2486,2546,2547,2612,2616,2675,3001,3055,\
                       3056,3110,3111,3175,3176,3229,3230,3281,3282,3334,3335,3389,3390,3446,3447,3510,3511,3563,3566,3621]

        target_list = []
        for file in img_files:
            target_num = int(file.split(".")[0])
            flag = 0
            i = 0
            for i in range(0,len(breakpoints),2):
                if((target_num >= breakpoints[i]) and (target_num <= breakpoints[i+1])):
                    flag = 1
                    break
            if(flag==1):
                target = int((i/2))
                target_list.append(target)

        y = np.array(target_list)
        X = dataset.iloc[:,1:]

        model = MultinomialNB()
        model.fit(X, y)
        print("Model trained successfully")
    else:
        print("Dataset directory not found")

def bg_sub(filename):
    """Background subtraction and preprocessing"""
    test_img_path = filename
    main_img = cv2.imread(test_img_path)

    img = cv2.cvtColor(main_img, cv2.COLOR_BGR2RGB)
    resized_image = cv2.resize(img, (1600, 1200))
    size_y, size_x, _ = img.shape

    gs = cv2.cvtColor(resized_image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gs, (55, 55), 0)

    ret_otsu, im_bw_otsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = np.ones((50, 50), np.uint8)
    closing = cv2.morphologyEx(im_bw_otsu, cv2.MORPH_CLOSE, kernel)

    contours, hierarchy = cv2.findContours(im_bw_otsu, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contains = []
    y_ri, x_ri, _ = resized_image.shape
    for cc in contours:
        yn = cv2.pointPolygonTest(cc, (x_ri//2, y_ri//2), False)
        contains.append(yn)

    val = [contains.index(temp) for temp in contains if temp > 0]
    if val:
        index = val[0]

        black_img = np.empty([1200, 1600, 3], dtype=np.uint8)
        black_img.fill(0)

        cnt = contours[index]
        mask = cv2.drawContours(black_img, [cnt], 0, (255, 255, 255), -1)

        maskedImg = cv2.bitwise_and(resized_image, mask)
        white_pix = [255, 255, 255]
        black_pix = [0, 0, 0]

        final_img = maskedImg
        h, w, channels = final_img.shape
        for x in range(0, w):
            for y in range(0, h):
                channels_xy = final_img[y, x]
                if all(channels_xy == black_pix):
                    final_img[y, x] = white_pix

        return final_img
    return resized_image

def feature_extract(img):
    """Extract features from processed image"""
    names = ['area', 'perimeter', 'pysiological_length', 'pysiological_width', 'aspect_ratio', 'rectangularity', 'circularity', \
             'mean_r', 'mean_g', 'mean_b', 'stddev_r', 'stddev_g', 'stddev_b', \
             'contrast', 'correlation', 'inverse_difference_moments', 'entropy']

    # Preprocessing
    gs = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gs, (25, 25), 0)
    ret_otsu, im_bw_otsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = np.ones((50, 50), np.uint8)
    closing = cv2.morphologyEx(im_bw_otsu, cv2.MORPH_CLOSE, kernel)

    # Shape features
    contours, image = cv2.findContours(im_bw_otsu, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        cnt = contours[0]
        M = cv2.moments(cnt)

        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = float(w)/h if h != 0 else 0
        rectangularity = w*h/area if area != 0 else 0
        circularity = ((perimeter)**2)/area if area != 0 else 0

        # Color features
        red_channel = img[:, :, 0]
        green_channel = img[:, :, 1]
        blue_channel = img[:, :, 2]
        blue_channel[blue_channel == 255] = 0
        green_channel[green_channel == 255] = 0
        red_channel[red_channel == 255] = 0

        red_mean = np.mean(red_channel)
        green_mean = np.mean(green_channel)
        blue_mean = np.mean(blue_channel)

        red_std = np.std(red_channel)
        green_std = np.std(green_channel)
        blue_std = np.std(blue_channel)

        # Texture features
        textures = mt.features.haralick(gs)
        ht_mean = textures.mean(axis=0)
        contrast = ht_mean[1]
        correlation = ht_mean[2]
        inverse_diff_moments = ht_mean[4]
        entropy = ht_mean[8]

        vector = [area, perimeter, w, h, aspect_ratio, rectangularity, circularity, \
                  red_mean, green_mean, blue_mean, red_std, green_std, blue_std, \
                  contrast, correlation, inverse_diff_moments, entropy]

        return vector
    return []

def image_to_base64(image):
    """Convert PIL Image to base64 string"""
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)

    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64

@app.route('/process', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400

    # Save uploaded file temporarily
    temp_path = 'temp_image.jpg'
    file.save(temp_path)

    try:
        # Process image
        processed_img = bg_sub(temp_path)

        # Extract features
        features = feature_extract(processed_img)

        if not features or model is None:
            return jsonify({'error': 'Feature extraction failed or model not loaded'}), 500

        # Make prediction
        prediction = model.predict([features])[0]

        # Generate processed images for display
        original_img = cv2.imread(temp_path)
        original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
        original_img = cv2.resize(original_img, (250, 250))

        # Blur image
        gs = cv2.cvtColor(original_img, cv2.COLOR_RGB2GRAY)
        blur_img = cv2.GaussianBlur(gs, (25, 25), 0)

        # Threshold image
        ret_otsu, thresh_img = cv2.threshold(blur_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Boundary image
        contours, _ = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        boundary_img = cv2.cvtColor(gs, cv2.COLOR_GRAY2RGB)
        if contours:
            cv2.drawContours(boundary_img, contours, -1, (0, 255, 0), 2)

        # Convert to base64
        processed_images = {
            'original': image_to_base64(original_img),
            'blur': image_to_base64(Image.fromarray(blur_img)),
            'threshold': image_to_base64(Image.fromarray(thresh_img)),
            'boundary': image_to_base64(boundary_img)
        }

        # Clean up
        os.remove(temp_path)

        return jsonify({
            'processedImages': processed_images,
            'prediction': {
                'classIndex': int(prediction),
                'confidence': float(model.predict_proba([features]).max())
            }
        })

    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    load_model()
    app.run(debug=True, port=5000)