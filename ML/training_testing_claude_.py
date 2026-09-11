import numpy as np
import librosa

def extract_features(file_path):
    audio, sr = librosa.load(file_path, sr=8000, mono=True)

    # Trim silence
    trimmed, _ = librosa.effects.trim(audio, top_db=25)
    if len(trimmed) > 0:
        audio = trimmed

    features = []

    # 1. Amplitude Envelope
    features.append(np.mean(np.abs(audio)))

    # 2. RMS
    features.append(np.mean(librosa.feature.rms(y=audio)))

    # 3. Zero Crossing Rate
    features.append(np.mean(librosa.feature.zero_crossing_rate(y=audio)))

    # 4. STFT
    features.append(np.mean(np.abs(librosa.stft(audio))))

    # 5. Spectral Centroid
    features.append(np.mean(
        librosa.feature.spectral_centroid(y=audio, sr=sr)
    ))

    # 6. Spectral Bandwidth
    features.append(np.mean(
        librosa.feature.spectral_bandwidth(y=audio, sr=sr)
    ))

    # 7. Spectral Contrast
    features.append(np.mean(
        librosa.feature.spectral_contrast(
            y=audio,
            sr=sr,
            n_bands=5
        )
    ))

    # 8. Spectral Rolloff
    features.append(np.mean(
        librosa.feature.spectral_rolloff(y=audio, sr=sr)
    ))

    # 9. Fundamental Frequency
    f0 = librosa.yin(
        audio,
        fmin=50,
        fmax=1000,
        sr=sr
    )

    features.append(
        np.mean(f0[f0 > 0]) if np.any(f0 > 0) else 0
    )

    # 10-22. MFCCs
    mfcc = librosa.feature.mfcc(
        y=audio,
        sr=sr,
        n_mfcc=13
    )

    for x in mfcc:
        features.append(np.mean(x))

    # 23. Duration
    features.append(len(audio) / sr)

    return np.array(features)


FEATURE_NAMES = [
    "Amplitude_Envelope", "RMS", "ZCR", "STFT_Mean",
    "Spectral_Centroid", "Spectral_Bandwidth",
    "Spectral_Contrast", "Spectral_Rolloff", "F0",
    "MFCC_1", "MFCC_2", "MFCC_3", "MFCC_4", "MFCC_5",
    "MFCC_6", "MFCC_7", "MFCC_8", "MFCC_9", "MFCC_10",
    "MFCC_11", "MFCC_12", "MFCC_13", "Duration"
]