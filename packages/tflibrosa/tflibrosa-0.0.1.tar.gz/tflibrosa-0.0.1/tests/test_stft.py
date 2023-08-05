import numpy as np 
from tflibrosa import STFT, Spectrogram, LogmelFilterBank, magphase
import librosa
import pytest 

def mel_spectrogram_librosa(data, n_fft, hop_size, window, center, dtype, pad_mode, fmin, fmax, sample_rate, n_mels, top_db, ref, amin):
    np_stft_matrix = librosa.stft(y=data, n_fft=n_fft, hop_length=hop_size,
            win_length=n_fft, window=window, center=center, dtype=dtype,
            pad_mode=pad_mode)

 
    np_melW = librosa.filters.mel(sr=sample_rate, n_fft=n_fft, n_mels=n_mels,
        fmin=fmin, fmax=fmax).T

    np_mel_spectrogram = np.dot(np.abs(np_stft_matrix.T) ** 2, np_melW)

    np_logmel_spectrogram = librosa.power_to_db(
        np_mel_spectrogram, ref=ref, amin=amin, top_db=top_db)

    return np_logmel_spectrogram

@pytest.mark.unittest
def test_stft():
    sample_rate = 32000
    n_fft = 2048
    hop_size = 512
    window = 'hann'
    pad_mode = 'reflect'
    mel_bins = 64
    ref = 1.0
    amin = 1e-10
    fmin = 20
    fmax = 16000 
    top_db = None 
    center = True 
    dtype=None

    audio = np.random.uniform(0,1 ,(sample_rate * 5, ))
    spec = STFT(n_fft=n_fft, hop_length=hop_size, win_length=n_fft,
        window=window, center=center, pad_mode=pad_mode, freeze_parameters=True)


    frame_r, frame_i = spec(audio.reshape(1,-1))
    frame_r, frame_i =frame_r.numpy(), frame_i.numpy()
    frame_librosa =  librosa.stft(audio, n_fft=n_fft, hop_length=hop_size, win_length=n_fft, window=window, center=center, pad_mode=pad_mode).T
    frame_librosa_r, frame_librosa_i = np.real(frame_librosa), np.imag(frame_librosa)
    #print(frame_r.shape, frame_librosa_r.shape)
    assert frame_r.squeeze(0).shape == frame_librosa_r.shape and frame_i.squeeze(0).shape == frame_librosa_i.shape 
    assert np.abs(frame_r.squeeze(0) - frame_librosa_r).mean() < 1e-5
    assert np.abs(frame_i.squeeze(0) - frame_librosa_i).mean() < 1e-5
    #print(np.abs(frame_r.squeeze(0) - frame_librosa_r).mean())

@pytest.mark.unittest
def test_mel_spectrogram():
    sample_rate = 32000
    n_fft = 2048
    hop_size = 512
    window = 'hann'
    pad_mode = 'reflect'
    mel_bins = 64
    ref = 1.0
    amin = 1e-10
    fmin = 20
    fmax = 16000 
    top_db = None 
    center = True 
    dtype=None

    audio = np.random.uniform(0,1 ,(sample_rate * 5, ))

    spectrogram_extractor = Spectrogram(n_fft=n_fft, hop_length=hop_size, 
            win_length=n_fft, window=window, center=center, pad_mode=pad_mode, 
            freeze_parameters=True, dtype="float32")

    # Logmel feature extractor
    logmel_extractor = LogmelFilterBank(sr=sample_rate, n_fft=n_fft, is_log=True, 
        n_mels=mel_bins, fmin=fmin, fmax=fmax, ref=ref, amin=amin, top_db=top_db, 
        freeze_parameters=True, dtype="float32")

    np_mel_spectrogram = mel_spectrogram_librosa(data=audio, n_fft=n_fft, hop_size=hop_size, window=window, center=center, dtype=dtype, 
                                                pad_mode=pad_mode, fmin=fmin, fmax=fmax, sample_rate=sample_rate, n_mels=mel_bins, top_db=top_db, ref=ref, amin=amin)

    spectrogram = spectrogram_extractor(audio[None, :])
    mel_spectrogram = logmel_extractor(spectrogram).numpy().squeeze(0)

    #print(np_mel_spectrogram.shape, mel_spectrogram.shape)
    assert mel_spectrogram.shape == np_mel_spectrogram.shape
    assert np.abs(mel_spectrogram - np_mel_spectrogram).mean() < 1e-5

@pytest.mark.unittest
def test_magphase():
    sample_rate = 32000
    n_fft = 2048
    hop_size = 512
    window = 'hann'
    pad_mode = 'reflect'
    mel_bins = 64
    ref = 1.0
    amin = 1e-10
    fmin = 20
    fmax = 16000 
    top_db = None 
    center = True 
    dtype=None

    audio = np.random.uniform(0,1 ,(sample_rate * 5, ))
    spec = STFT(n_fft=n_fft, hop_length=hop_size, win_length=n_fft,
        window=window, center=center, pad_mode=pad_mode, freeze_parameters=True)


    frame_r, frame_i = spec(audio.reshape(1,-1))

    value = magphase(frame_r, frame_i) 

    assert type(value) == tuple 

if __name__ == "__main__":
    test_stft()
    test_mel_spectrogram()
    test_magphase()