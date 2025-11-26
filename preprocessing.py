import cv2
import numpy as np
from skimage.morphology import skeletonize

IMG_SIZE = 200

def preprocess_basic(image):
    img_resized = cv2.resize(image, (IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_CUBIC)
    return img_resized

def denoise_image(image):
    if image.dtype != np.uint8:
        image = np.uint8(image * 255) if image.max() <= 1.0 else np.uint8(image)
    return cv2.bilateralFilter(image, 5, 50, 50)

def normalize_image(image):
    return image / 255.0

def enhance_contrast(image):
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    image_uint8 = np.uint8(image * 255) if image.max() <= 1.0 else np.uint8(image)
    enhanced = clahe.apply(image_uint8)
    return enhanced / 255.0

def sharpen_image(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(image, -1, kernel)
    return np.clip(sharpened, 0, 1)


def preprocess_pipeline(image):
    """Main preprocessing pipeline"""
    image = preprocess_basic(image)
    image = denoise_image(image)
    image = normalize_image(image)
    image = enhance_contrast(image)
    image = sharpen_image(image)
    return image


# Feature extraction (Ridges, Valleys, RTVTR)

def create_fingerprint_mask(image, threshold=0.05):
    img_float = image.astype(np.float32)
    mean = cv2.blur(img_float, (15, 15))
    sq_mean = cv2.blur(img_float ** 2, (15, 15))
    variance = sq_mean - mean ** 2
    variance = cv2.normalize(variance, None, 0, 1, cv2.NORM_MINMAX)
    mask = (variance > threshold).astype(np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    return mask


def remove_intersections(skeleton_img):
    skel = skeleton_img.copy()
    skel[skel > 0] = 1
    kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=np.uint8)
    neighbors_count = cv2.filter2D(skel, -1, kernel)
    intersections = (skel == 1) & (neighbors_count > 2)
    skel_clean = skeleton_img.copy()
    skel_clean[intersections] = 0
    return skel_clean


def extract_features(image, mask):
    """Output: ridges_count, ridge_density, rtvtr"""
    img_u8 = np.uint8(image * 255)
    binary = cv2.adaptiveThreshold(img_u8, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY_INV, 25, 5)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    binary_ridges = cv2.bitwise_and(binary, binary, mask=mask)
    binary_valleys_raw = cv2.bitwise_not(binary)
    binary_valleys = cv2.bitwise_and(binary_valleys_raw, binary_valleys_raw, mask=mask)

    ridge_pixels = np.count_nonzero(binary_ridges)
    valley_pixels = np.count_nonzero(binary_valleys)

    rtvtr = 0.0
    if valley_pixels > 0:
        rtvtr = ridge_pixels / float(valley_pixels)

    skel = skeletonize(binary_ridges > 0)
    skel_uint8 = (skel * 255).astype(np.uint8)
    skel_cut = remove_intersections(skel_uint8)

    min_line_length = 20
    nb_r, labels_r, stats_r, _ = cv2.connectedComponentsWithStats(skel_cut, connectivity=8)
    ridges_count = sum(1 for i in range(1, nb_r) if stats_r[i, cv2.CC_STAT_AREA] >= min_line_length)

    ridge_density = ridge_pixels / (np.count_nonzero(mask) + 1e-6)

    return ridges_count, ridge_density, rtvtr


def prepare_image_for_model(image_path):
    """
    Prepares the image and extracts features for model input.
    Input: image path
    Output: tuple (final_img, final_features)
    """
    original_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if original_img is None:
        raise ValueError("Cannot load image")

    # Image preprocessing
    processed_img = preprocess_pipeline(original_img)

    # Feature extraction
    mask = create_fingerprint_mask(processed_img)
    ridges, density, rtvtr = extract_features(processed_img, mask)

    # Formatting image
    final_img = processed_img.reshape(1, 200, 200, 1)

    # Features
    final_features = np.array([[ridges, density, rtvtr]])

    return final_img, final_features