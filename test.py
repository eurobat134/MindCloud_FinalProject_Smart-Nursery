import pandas as pd
import joblib

from feature_extraction import extract_features


# =========================
# 1. LOAD MODEL
# =========================

model = joblib.load("cry_model.pkl")


# =========================
# 2. AUDIO FILE TO TEST
# =========================

audio_file = r"discomfort_1_speed_0.94.wav"


# =========================
# 3. EXTRACT FEATURES
# =========================

features = extract_features(audio_file)


# =========================
# 4. FEATURE NAMES
# =========================

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


# =========================
# 5. CREATE DATAFRAME
# =========================

new_data = pd.DataFrame([features], columns=columns)


# Remove features that weren't used during training
X_new = new_data.drop(columns=["MelSpec", "MFCCs20"])


print("Feature shape:", X_new.shape)


# =========================
# 6. PREDICT
# =========================

prediction = model.predict(X_new)[0]

probability = model.predict_proba(X_new)[0]


# =========================
# 7. RESULT
# =========================

if prediction == 1:

    print("RESULT: CRY")
    print("Confidence:", round(probability[1] * 100, 2), "%")

else:

    print("RESULT: NOT CRY")
    print("Confidence:", round(probability[0] * 100, 2), "%")