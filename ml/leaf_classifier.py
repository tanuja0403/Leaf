import cv2
import numpy as np
import pandas as pd
import mahotas as mt
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import os

class LeafClassifier:
    def __init__(self):
        self.model = None
        self.dataset = None
        self.breakpoints = [1001,1059,1060,1122,1552,1616,1123,1194,1195,1267,1268,1323,1324,1385,1386,1437,1497,1551,1438,1496,2001,2050,\
                           2051,2113,2114,2165,2166,2230,2231,2290,2291,2346,2347,2423,2424,2485,2486,2546,2547,2612,2616,2675,3001,3055,\
                           3056,3110,3111,3175,3176,3229,3230,3281,3282,3334,3335,3389,3390,3446,3447,3510,3511,3563,3566,3621]

    def load_dataset(self, csv_path, image_dir):
        """Load dataset and prepare features"""
        if os.path.exists(csv_path):
            self.dataset = pd.read_csv(csv_path)
        else:
            print(f"Dataset CSV not found at {csv_path}")
            return False

        if os.path.exists(image_dir):
            img_files = os.listdir(image_dir)
            target_list = []

            for file in img_files:
                target_num = int(file.split(".")[0])
                flag = 0
                i = 0
                for i in range(0, len(self.breakpoints), 2):
                    if (target_num >= self.breakpoints[i]) and (target_num <= self.breakpoints[i+1]):
                        flag = 1
                        break
                if flag == 1:
                    target = int((i/2))
                    target_list.append(target)

            self.y = np.array(target_list)
            self.X = self.dataset.iloc[:, 1:]
            return True
        else:
            print(f"Image directory not found at {image_dir}")
            return False

    def train_model(self):
        """Train the Naive Bayes model"""
        if self.X is None or self.y is None:
            print("Dataset not loaded")
            return False

        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)

        self.model = MultinomialNB()
        self.model.fit(X_train, y_train)

        # Evaluate model
        accuracy = self.model.score(X_test, y_test)
        predictions = self.model.predict(X_test)

        print(f"Model Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, predictions))

        return True

    def predict(self, features):
        """Make prediction on new features"""
        if self.model is None:
            return None

        prediction = self.model.predict([features])[0]
        confidence = self.model.predict_proba([features]).max()

        return {
            'class_index': int(prediction),
            'confidence': float(confidence)
        }

def extract_features(img):
    """Extract features from a single image"""
    names = ['area','perimeter','pysiological_length','pysiological_width','aspect_ratio','rectangularity','circularity',\
             'mean_r','mean_g','mean_b','stddev_r','stddev_g','stddev_b', \
             'contrast','correlation','inverse_difference_moments','entropy']

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
        red_channel = img[:,:,0]
        green_channel = img[:,:,1]
        blue_channel = img[:,:,2]
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

# Common names and Wikipedia links for leaf species
LEAF_SPECIES = [
    'pubescent bamboo', 'Chinese horse chestnut', 'Anhui Barberry',
    'Chinese redbud', 'true indigo', 'Japanese maple', 'Nanmu', 'castor aralia',
    'Chinese cinnamon', 'goldenrain tree', 'Big-fruited Holly', 'Japanese cheesewood',
    'wintersweet', 'camphortree', 'Japan Arrowwood', 'sweet osmanthus',
    'deodar', 'ginkgo, maidenhair tree', 'Crape myrtle, Crepe myrtle',
    'oleander', 'yew plum pine', 'Japanese Flowering Cherry', 'Glossy Privet',
    'Chinese Toon', 'peach', 'Ford Woodlotus', 'trident maple',
    'Beales barberry', 'southern magnolia', 'Canadian poplar',
    'Chinese tulip tree', 'tangerine'
]

WIKIPEDIA_LINKS = [
    'https://en.wikipedia.org/wiki/Pseudosasa_japonica',
    'https://en.wikipedia.org/wiki/Aesculus_chinensis',
    'https://en.wikipedia.org/wiki/Berberis',
    'https://sites.redlands.edu/trees/species-accounts/eastern-redbud/',
    'https://en.wikipedia.org/wiki/Indigofera_tinctoria',
    'https://en.wikipedia.org/wiki/Acer_palmatum',
    'https://en.wikipedia.org/wiki/Lauraceae',
    'http://hort.uconn.edu/detail.php?pid=238',
    'https://en.wikipedia.org/wiki/Cinnamomum_cassia',
    'https://en.wikipedia.org/wiki/Koelreuteria_paniculata',
    'https://en.wikipedia.org/wiki/Holly',
    'https://en.wikipedia.org/wiki/Pittosporum_tobira',
    'https://en.wikipedia.org/wiki/Chimonanthus',
    'https://en.wikipedia.org/wiki/Cinnamomum_camphora',
    'https://en.wikipedia.org/wiki/Viburnum',
    'https://en.wikipedia.org/wiki/Osmanthus_fragrans',
    'https://en.wikipedia.org/wiki/Cedrus_deodara',
    'https://en.wikipedia.org/wiki/Ginkgo_biloba',
    'https://en.wikipedia.org/wiki/Lagerstroemia',
    'https://en.wikipedia.org/wiki/Nerium',
    'https://en.wikipedia.org/wiki/Podocarpus_macrophyllus',
    'https://www.gardenia.net/plant-variety/Prunus-serrulata-Japanese-Flowering-Cherry',
    'https://en.wikipedia.org/wiki/Ligustrum_lucidum',
    'https://en.wikipedia.org/wiki/Toona_sinensis',
    'https://www.britannica.com/plant/peach',
    'https://ieeexplore.ieee.org/document/7294864',
    'https://en.wikipedia.org/wiki/Acer_buergerianum',
    'https://www.finegardening.com/plant/leatherleaf-mahonia-beales-barberry-mahonia-bealei',
    'https://en.wikipedia.org/wiki/Magnolia_grandiflora',
    'https://en.wikipedia.org/wiki/Populus_%C3%97_canadensis',
    'https://en.wikipedia.org/wiki/Liriodendron_chinense',
    'https://en.wikipedia.org/wiki/Tangerine'
]