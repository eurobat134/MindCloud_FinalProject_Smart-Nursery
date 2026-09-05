import os
from datetime import datetime
import pandas as pd
import sounddevice as sd
import soundfile as sf
import joblib
from feature_extraction import extract_features

SAMPLE_RATE = 16000
RECORD_SECONDS = 5

RECORDINGS_FOLDER = "recordings"

MODEL1_PATH = "cry_detector.pkl"
MODEL2_PATH = "cry_classifier.pkl"

os.makedirs(RECORDINGS_FOLDER, exist_ok=True)

# Load models
model1 = joblib.load(MODEL1_PATH)
model2 = joblib.load(MODEL2_PATH)

print("Models loaded successfully.")
print("Starting baby cry detection...")
print()


columns = [
    "Amplitude_Envelope_Mean",
    "RMS_Mean",
    "ZCR_Mean",
    "STFT_Mean",
    "SC_Mean",
    "SBAN_Mean",
    "SCON_Mean",
    "MFCCs13Mean",
    "delMFCCs13",
    "del2MFCCs13",
    "MelSpec",
    "MFCCs20",
    "MFCCs1",
    "MFCCs2",
    "MFCCs3",
    "MFCCs4",
    "MFCCs5",
    "MFCCs6",
    "MFCCs7",
    "MFCCs8",
    "MFCCs9",
    "MFCCs10",
    "MFCCs11",
    "MFCCs12",
    "MFCCs13"
]

def prepare_features(file_path):

    features = extract_features(file_path)

    data = pd.DataFrame(
        [features],
        columns=columns
    )

    # These two were not used when training
    X = data.drop(
        columns=["MelSpec", "MFCCs20"]
    )

    return X

def record_audio():

    print("Recording for 5 seconds...")

    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    print("Recording finished.")

    return audio.flatten()



def detect_cry(X):

    prediction = model1.predict(X)[0]

    probabilities = model1.predict_proba(X)[0]

    if prediction == 1:

        confidence = probabilities[1] * 100

        return "CRY", confidence

    else:

        confidence = probabilities[0] * 100

        return "NOT CRY", confidence


def detect_cry_reason(X):

    prediction = model2.predict(X)[0]

    probabilities = model2.predict_proba(X)[0]

    class_names = {
        0: "Discomfort",
        1: "Hungry",
        2: "Tired"
    }

    reason = class_names[prediction]

    confidence = probabilities[prediction] * 100

    return reason, confidence


try:

    while True:

        audio = record_audio()

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        file_path = os.path.join(
            RECORDINGS_FOLDER,
            timestamp + ".wav"
        )

        sf.write(
            file_path,
            audio,
            SAMPLE_RATE
        )

        print("Saved:", file_path)


        X_new = prepare_features(file_path)

        print("Feature shape:", X_new.shape)


        cry_result, cry_confidence = detect_cry(X_new)

        print(
            f"Model 1: {cry_result} "
            f"({cry_confidence:.2f}%)"
        )

        if cry_result == "CRY":

            reason, reason_confidence = detect_cry_reason(
                X_new
            )

            print(
                f"Model 2: {reason} "
                f"({reason_confidence:.2f}%)"
            )

            print(
                f"\nFINAL VERDICT: {reason}\n"
            )

        else:

            print(
                "\nFINAL VERDICT: NOT CRY\n"
            )

        print("=" * 50)


except KeyboardInterrupt:

    print("\nDetection stopped.")