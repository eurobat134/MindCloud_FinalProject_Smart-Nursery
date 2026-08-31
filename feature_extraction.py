import numpy as np
import librosa


def extract_features(file_path):

    # Load audio
    audio, sr = librosa.load(
        file_path,
        sr=16000,
        mono=True
    )

    # Amplitude Envelope Mean
    amplitude_envelope = np.abs(audio)
    amplitude_envelope_mean = np.mean(amplitude_envelope)

    # RMS Mean
    rms = librosa.feature.rms(y=audio)
    RMS_Mean = np.mean(rms)

    # ZCR Mean
    zcr = librosa.feature.zero_crossing_rate(audio)
    ZCR_Mean = np.mean(zcr)

    # STFT Mean
    stft = librosa.stft(audio)
    stft_magnitude = np.abs(stft)
    STFT_Mean = np.mean(stft_magnitude)

    # Spectral Centroid Mean
    spectral_centroid = librosa.feature.spectral_centroid(
        y=audio,
        sr=sr
    )
    SC_Mean = np.mean(spectral_centroid)

    # Spectral Bandwidth Mean
    spectral_bandwidth = librosa.feature.spectral_bandwidth(
        y=audio,
        sr=sr
    )
    SBAN_Mean = np.mean(spectral_bandwidth)

    # Spectral Contrast Mean
    spectral_contrast = librosa.feature.spectral_contrast(
        y=audio,
        sr=sr
    )
    SCON_Mean = np.mean(spectral_contrast)

    # 13 MFCCs
    mfcc13 = librosa.feature.mfcc(
        y=audio,
        sr=sr,
        n_mfcc=13
    )

    # MFCCs13 Mean
    MFCCs13Mean = np.mean(mfcc13)

    # Delta MFCC 13
    delta_mfcc13 = librosa.feature.delta(mfcc13)
    delMFCCs13 = np.mean(delta_mfcc13[12])

    # Delta-Delta MFCC 13
    delta2_mfcc13 = librosa.feature.delta(
        mfcc13,
        order=2
    )
    del2MFCCs13 = np.mean(delta2_mfcc13[12])

    # Mel Spectrogram
    mel_spec = librosa.feature.melspectrogram(
        y=audio,
        sr=sr
    )
    MelSpec = str(mel_spec.tolist())

    # 20 MFCCs
    mfcc20 = librosa.feature.mfcc(
        y=audio,
        sr=sr,
        n_mfcc=20
    )
    MFCCs20 = str(mfcc20.tolist())

    # Individual MFCCs 1-13
    MFCCs1 = np.mean(mfcc13[0])
    MFCCs2 = np.mean(mfcc13[1])
    MFCCs3 = np.mean(mfcc13[2])
    MFCCs4 = np.mean(mfcc13[3])
    MFCCs5 = np.mean(mfcc13[4])
    MFCCs6 = np.mean(mfcc13[5])
    MFCCs7 = np.mean(mfcc13[6])
    MFCCs8 = np.mean(mfcc13[7])
    MFCCs9 = np.mean(mfcc13[8])
    MFCCs10 = np.mean(mfcc13[9])
    MFCCs11 = np.mean(mfcc13[10])
    MFCCs12 = np.mean(mfcc13[11])
    MFCCs13 = np.mean(mfcc13[12])

    # Put all features into one list
    features = [
        amplitude_envelope_mean,
        RMS_Mean,
        ZCR_Mean,
        STFT_Mean,
        SC_Mean,
        SBAN_Mean,
        SCON_Mean,
        MFCCs13Mean,
        delMFCCs13,
        del2MFCCs13,
        MelSpec,
        MFCCs20,
        MFCCs1,
        MFCCs2,
        MFCCs3,
        MFCCs4,
        MFCCs5,
        MFCCs6,
        MFCCs7,
        MFCCs8,
        MFCCs9,
        MFCCs10,
        MFCCs11,
        MFCCs12,
        MFCCs13
    ]

    return features