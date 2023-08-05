# tflibrosa
re-implementation of torch librosa for tensorflow. It is usefull if you want to compute Spectrogram on GPU for faster inference instead of using librosa.

# Installation 

> pip install tflibrosa

# Example

To do some inference on single sample, you can use python script in examples/ folder or use as follows:

```
import numpy as np 
from tflibrosa import STFT, Spectrogram, LogmelFilterBank
import librosa
import tensorflow as tf 
audio = np.random.uniform(0,1 ,(32000 * 5))
print(audio.shape)

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
top_db = 80.0
center = True 
dtype=None

spectrogram_extractor = Spectrogram(n_fft=n_fft, hop_length=hop_size, 
                win_length=n_fft, window=window, center=center, pad_mode=pad_mode, 
                freeze_parameters=True, dtype="float32")

# Logmel feature extractor
logmel_extractor = LogmelFilterBank(sr=sample_rate, n_fft=n_fft, is_log=True, 
    n_mels=mel_bins, fmin=fmin, fmax=fmax, ref=ref, amin=amin, top_db=top_db, 
    freeze_parameters=True, dtype="float32")


spectrogram = spectrogram_extractor(audio[None, :])

mel_spectrogram = logmel_extractor(spectrogram)

print(mel_spectrogram) # (batch size, num_channels, timestamps)
```


# Acknowledgement

- librosa : https://librosa.org/doc/latest/index.html
- torchlibrosa : https://github.com/qiuqiangkong/torchlibrosa 