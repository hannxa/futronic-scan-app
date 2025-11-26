import tensorflow as tf
from preprocessing import prepare_image_for_model
import os
import numpy as np

# Model path
MODEL_PATH = 'gender_model.tflite'

class GenderPredictor:
    def __init__(self, model_path):
        print("Model loading...")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"No model found: {model_path}")

        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        self.img_index = None
        self.feat_index = None

        for i, detail in enumerate(self.input_details):
            shape = detail['shape']
            if len(shape) == 4:
                self.img_index = detail['index']
                print(f"Input image on index: {self.img_index} (shape: {shape})")
            elif len(shape) == 2:
                self.feat_index = detail['index']
                print(f"Input features on index: {self.feat_index} (shape: {shape})")

        if self.img_index is None or self.feat_index is None:
            raise ValueError("Couldn't find image and features vector.")

        print("TFLite ready to work.")

    def predict(self, image_path):
        """
        Input: image path
        Output: dictionary with prediction results
        """
        try:
            # 1. Preprocessing
            img_input, features_input = prepare_image_for_model(image_path)

            img_input = img_input.astype(np.float32)
            features_input = features_input.astype(np.float32)

            # 2. Setting interpreter input data
            self.interpreter.set_tensor(self.img_index, img_input)
            self.interpreter.set_tensor(self.feat_index, features_input)

            # 3. Running model
            self.interpreter.invoke()

            # 4. Getting output
            output_data = self.interpreter.get_tensor(self.output_details[0]['index'])

            prediction_score = output_data[0][0]

            # 5. Interpretation
            gender = "Female" if prediction_score > 0.5 else "Male"
            confidence = prediction_score if gender == "Female" else 1 - prediction_score

            return {
                "status": "success",
                "gender": gender,
                "confidence": f"{confidence:.2%}",
                "raw_score": float(prediction_score)
            }

        except Exception as e:
            import traceback
            traceback.print_exc()

            return {
                "status": "error",
                "message": str(e)
            }
