import tensorflow as tf
from preprocessing import prepare_image_for_model
import os

# Model path
MODEL_PATH = 'gender_model.h5'

class GenderPredictor:
    def __init__(self, model_path):
        print("Model loading...")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"No model found: {model_path}")

        self.model = tf.keras.models.load_model(model_path)
        print("Model loaded correctly.")

    def predict(self, image_path):
        """
        Input: image path
        Output: dictionary with prediction results
        """
        try:
            # 1. Preprocessing
            img_input, features_input = prepare_image_for_model(image_path)

            # 2. Model Prediction
            # 0 -> Male, 1 -> Female
            prediction_score = self.model.predict([img_input, features_input], verbose=0)[0][0]

            # 3. Interpretation
            gender = "Female" if prediction_score > 0.5 else "Male"
            confidence = prediction_score if gender == "Female" else 1 - prediction_score

            return {
                "status": "success",
                "gender": gender,
                "confidence": f"{confidence:.2%}",
                "raw_score": float(prediction_score)
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }