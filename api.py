from fastapi import FastAPI, File, UploadFile, HTTPException
import shutil
import os
import uuid
from inference import GenderPredictor

app = FastAPI(title="Gender Recognition API")

MODEL_PATH = 'gender_model.h5'
TEMP_DIR = 'temp_uploads'
os.makedirs(TEMP_DIR, exist_ok=True)

try:
    predictor = GenderPredictor(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {e}")

@app.post("/predict")
async def predict_gender(file: UploadFile = File(...)):
    """
    Endpoint is collecting an image, saving it temporarily,
    passing it to the predictor and returning the result.
    """
    try:
        # Save uploaded file to a unique temporary path
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        temp_file_path = os.path.join(TEMP_DIR, unique_filename)

        # Save uploaded file to temporary location
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Predict
        result = predictor.predict(temp_file_path)

        # Delete temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

        # Return result
        if result['status'] == 'success':
            return result['gender']
        else:
            raise HTTPException(status_code=500, detail=result['message'])

    except Exception as e:
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=str(e))

