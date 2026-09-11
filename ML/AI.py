import os
import time
import threading
import joblib
import pandas as pd

from .feature_extraction import extract_features, FEATURE_NAMES

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "cry_classifier.joblib")
WAV_FOLDER = os.path.join(BASE_DIR, "wav_files")

prediction = "3"

_running = False
_thread = None


def detect_cry():
    global prediction

    model = joblib.load(MODEL_PATH)

    while _running:

        wav_files = [
            file
            for file in os.listdir(WAV_FOLDER)
            if file.lower().endswith(".wav")
        ]

        if not wav_files:
            prediction = "3"

        else:
            file = wav_files[0]
            file_path = os.path.join(WAV_FOLDER, file)

            try:
                features = extract_features(file_path)

                features = pd.DataFrame(
                    [features],
                    columns=FEATURE_NAMES
                )

                result = model.predict(features)[0]

                prediction = str(result)

                print(file, "->", prediction)

            except Exception as e:
                print(f"Error processing {file}: {e}")
                prediction = "3"

        time.sleep(5)


def start():
    global _running, _thread

    if _running:
        return

    _running = True

    _thread = threading.Thread(
        target=detect_cry,
        daemon=True
    )

    _thread.start()


def stop():
    global _running

    _running = False


def get_prediction():
    return prediction