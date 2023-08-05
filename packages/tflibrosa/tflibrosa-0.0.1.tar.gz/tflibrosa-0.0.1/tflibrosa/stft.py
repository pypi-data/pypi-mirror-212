import librosa 
import tensorflow as tf 
import numpy as np 

PI_ = np.pi

class DFTBase(tf.keras.layers.Layer):
    def __init__(self,**kwargs):
        r"""Base class for DFT and IDFT matrix.
        """
        super(DFTBase, self).__init__(**kwargs)
    def dft_matrix(self, n):
        (x, y) = tf.meshgrid(tf.range(0, limit=n), tf.range(0, limit=n))
        omega = tf.math.exp(  -2 * PI_ * 1j  / n) # const
 
        W = tf.math.pow(omega, tf.cast(x * y, tf.complex128))  # shape: (n, n)
        #print(W.dtype)
        return W

    def idft_matrix(self, n):
        (x, y) = tf.meshgrid(tf.range(0, limit=n), tf.range(0, limit=n))
        x = tf.cast(x , dtype=tf.float32)
        y = tf.cast(y , dtype=tf.float32)
        omega = tf.math.exp(2.0 * PI_ * 1j  / n) # const
        W = tf.math.pow(omega, tf.cast(x * y,   tf.complex128))  # shape: (n, n)
        return W
    
class DFT(DFTBase):
    def __init__(self, n, norm, **kwargs):
        r"""Calculate discrete Fourier transform (DFT), inverse DFT (IDFT, 
        right DFT (RDFT) RDFT, and inverse RDFT (IRDFT.) 
        Args:
          n: fft window size
          norm: None | 'ortho'
        """
        super(DFT, self).__init__(**kwargs)

        self.W = self.dft_matrix(n)
        self.inv_W = self.idft_matrix(n)

        self.W_real = tf.math.real(self.W)
        self.W_imag = tf.math.imag(self.W)
        self.inv_W_real = tf.math.real(self.inv_W)
        self.inv_W_imag = tf.math.imag(self.inv_W)

        self.n = n
        self.norm = norm

    def dft(self, x_real, x_imag):
        r"""Calculate DFT of a signal.
        Args:
            x_real: (n,), real part of a signal
            x_imag: (n,), imag part of a signal
        Returns:
            z_real: (n,), real part of output
            z_imag: (n,), imag part of output
        """
        x_real = tf.cast(x_real, dtype=tf.float32)
        
        z_real = tf.linalg.matmul(x_real, self.W_real) - tf.linalg.matmul(x_imag, self.W_imag)#torch.matmul(x_real, self.W_real) - torch.matmul(x_imag, self.W_imag)
        z_imag = tf.linalg.matmul(x_imag, self.W_real) + tf.linalg.matmul(x_real, self.W_imag)
        # shape: (n,)

        if self.norm is None:
            pass
        elif self.norm == 'ortho':
            z_real = z_real / tf.math.sqrt(self.n)
            z_imag = z_imag / tf.math.sqrt(self.n)

        return z_real, z_imag

    def idft(self, x_real, x_imag):
        r"""Calculate IDFT of a signal.
        Args:
            x_real: (n,), real part of a signal
            x_imag: (n,), imag part of a signal
        Returns:
            z_real: (n,), real part of output
            z_imag: (n,), imag part of output
        """
        z_real = tf.linalg.matmul(x_real, self.inv_W_real) - tf.linalg.matmul(x_imag, self.inv_W_imag)
        z_imag = tf.linalg.matmul(x_imag, self.inv_W_real) + tf.linalg.matmul(x_real, self.inv_W_imag)
        # shape: (n,)

        if self.norm is None:
            z_real = z_real / self.n
        elif self.norm == 'ortho':
            z_real = z_real / tf.math.sqrt(n)
            z_imag = z_imag / tf.math.sqrt(n)

        return z_real, z_imag

    def rdft(self, x_real):
        r"""Calculate right RDFT of signal.
        Args:
            x_real: (n,), real part of a signal
            x_imag: (n,), imag part of a signal
        Returns:
            z_real: (n // 2 + 1,), real part of output
            z_imag: (n // 2 + 1,), imag part of output
        """
        n_rfft = self.n // 2 + 1
        z_real = tf.linalg.matmul(x_real, self.W_real[..., 0 : n_rfft])
        z_imag = tf.linalg.matmul(x_real, self.W_imag[..., 0 : n_rfft])
        # shape: (n // 2 + 1,)

        if self.norm is None:
            pass
        elif self.norm == 'ortho':
            z_real = z_real / tf.math.sqrt(self.n)
            z_imag = z_imag / tf.math.sqrt(self.n)

        return z_real, z_imag

    def irdft(self, x_real, x_imag):
        r"""Calculate IRDFT of signal.
        
        Args:
            x_real: (n // 2 + 1,), real part of a signal
            x_imag: (n // 2 + 1,), imag part of a signal
        Returns:
            z_real: (n,), real part of output
            z_imag: (n,), imag part of output
        """
        n_rfft = self.n // 2 + 1

        flip_x_real = tf.reverse(x_real, axis=(-1,))
        flip_x_imag = tf.reverse(x_imag, axis=(-1,))
        # shape: (n // 2 + 1,)

        x_real = tf.cat((x_real, flip_x_real[..., 1 : n_rfft - 1]), axis=-1)
        x_imag = tf.cat((x_imag, -1. * flip_x_imag[..., 1 : n_rfft - 1]), axis=-1)
        # shape: (n,)

        z_real = tf.linalg.matmul(x_real, self.inv_W_real) - tf.linalg.matmul(x_imag, self.inv_W_imag)
        # shape: (n,)

        if self.norm is None:
            z_real = z_real/self.n
        elif self.norm == 'ortho':
            z_real = z_real / tf.math.sqrt(self.n)

        return z_real

class STFT(DFTBase):
    def __init__(self, n_fft=2048, hop_length=None, win_length=None,
        window='hann', center=True, pad_mode='reflect', freeze_parameters=True, **kwargs):
        r"""PyTorch implementation of STFT with Conv1d. The function has the 
        same output as librosa.stft.
        Args:
            n_fft: int, fft window size, e.g., 2048
            hop_length: int, hop length samples, e.g., 441
            win_length: int, window length e.g., 2048
            window: str, window function name, e.g., 'hann'
            center: bool
            pad_mode: str, e.g., 'reflect'
            freeze_parameters: bool, set to True to freeze all parameters. Set
                to False to finetune all parameters.
        """
        super(STFT, self).__init__(**kwargs)

        assert pad_mode in ['constant', 'reflect']

        self.n_fft = n_fft
        self.hop_length = hop_length
        self.win_length = win_length
        self.window = window
        self.center = center
        self.pad_mode = pad_mode
        self.freeze_parameters = freeze_parameters

        # By default, use the entire frame.
        if self.win_length is None:
            self.win_length = n_fft

        # Set the default hop, if it's not already specified.
        if self.hop_length is None:
            self.hop_length = int(self.win_length // 4)

        fft_window = librosa.filters.get_window(window, self.win_length, fftbins=True)

        # Pad the window out to n_fft size.
        fft_window = librosa.util.pad_center(fft_window, size=n_fft)

        # DFT & IDFT matrix.
        self.W = self.dft_matrix(n_fft)

        out_channels = n_fft // 2 + 1

        self.conv_real = tf.keras.layers.Conv1D(filters=out_channels,
            kernel_size=n_fft, strides=self.hop_length, padding="VALID", dilation_rate=1,
            groups=1, use_bias=False, dtype=tf.float32)

        self.conv_imag = tf.keras.layers.Conv1D(filters=out_channels,
            kernel_size=n_fft, strides=self.hop_length, padding="VALID", dilation_rate=1,
            groups=1, use_bias=False, dtype=tf.float32)
        self.init_conv()
        #print(self.conv_real.weights[0].shape ,   tf.math.real(self.W[:, 0 : out_channels] * fft_window[:, None])[:, None, :].shape)
        self.conv_real.set_weights([tf.math.real(self.W[:, 0 : out_channels] * fft_window[:, None])[:, None, :]])
        
        # (n_fft // 2 + 1, 1, n_fft)
     
        self.conv_imag.set_weights([tf.math.imag(self.W[:, 0 : out_channels] * fft_window[:, None])[:, None, :]])
        # (n_fft // 2 + 1, 1, n_fft)

        if self.freeze_parameters:
            self.conv_real.trainable = False
            self.conv_imag.trainable = False
 
 

    def init_conv(self):
        s = tf.constant(np.random.uniform(0,1,(1, 32000*5, 1)).astype(np.float32))
        self.conv_real(s)
        self.conv_imag(s)
        
    def call(self, input):
        r"""Calculate STFT of batch of signals.
        Args: 
            input: (batch_size, data_length), input signals.
        Returns:
            real: (batch_size, 1, time_steps, n_fft // 2 + 1)
            imag: (batch_size, 1, time_steps, n_fft // 2 + 1)
        """
        input = tf.cast(input, tf.float32)
        x = input[:,  :]   # (batch_size, data_length, channels_num,)

        if self.center:
            padding = tf.constant([[0, 0], [self.n_fft // 2, self.n_fft // 2]])
            #print(padding.shape)
            x = tf.pad(x, paddings=padding, mode=self.pad_mode)
        x = x[:, :, None]
        #print(x.shape)
        
        real = self.conv_real(x)
        imag = self.conv_imag(x)
        # (batch_size, n_fft // 2 + 1, time_steps)
        #print(x.dtype, real.dtype, imag.dtype, real.shape, imag.shape)
        real =  real[:, :, :]#.transpose(2, 3)
        imag = imag[:, :, :]#.transpose(2, 3)
        # (batch_size, 1, time_steps, n_fft // 2 + 1)

        return real, imag

class Spectrogram(tf.keras.layers.Layer):
    def __init__(self, n_fft=2048, hop_length=None, win_length=None,
        window='hann', center=True, pad_mode='reflect', power=2.0,
        freeze_parameters=True,  **kwargs):
        r"""Calculate spectrogram using tensorflow following torchlibrosa. The STFT is implemented with 
        Conv1d. The function has the same output of librosa.stft
        """
        super(Spectrogram, self).__init__( **kwargs)

        self.power = power

        self.stft = STFT(n_fft=n_fft, hop_length=hop_length,
            win_length=win_length, window=window, center=center,
            pad_mode=pad_mode, freeze_parameters=True, **kwargs)
        

    def call(self, input):
        r"""Calculate spectrogram of input signals.
        Args: 
            input: (batch_size, data_length)
        Returns:
            spectrogram: (batch_size, 1, time_steps, n_fft // 2 + 1)
        """
        dtype = tf.float32
        input = tf.cast(input, tf.float32)
        (real, imag) = self.stft(input)
        # (batch_size, n_fft // 2 + 1, time_steps)
        spectrogram = real ** 2 + imag ** 2

        if self.power == 2.0:
            pass
        else:
            spectrogram = spectrogram ** (self.power / 2.0)

        return tf.cast(spectrogram, dtype=dtype)


class LogmelFilterBank(tf.keras.layers.Layer):
    def __init__(self, sr=22050, n_fft=2048, n_mels=64, fmin=0.0, fmax=None, 
        is_log=True, ref=1.0, amin=1e-10, top_db=80.0, freeze_parameters=True,  **kwargs):
        r"""Calculate logmel spectrogram using pytorch. The mel filter bank is 
        the pytorch implementation of as librosa.filters.mel 
        """
        super(LogmelFilterBank, self).__init__(  **kwargs)

        self.is_log = is_log
        self.ref = ref
        self.amin = amin
        self.top_db = top_db
        if fmax == None:
            fmax = sr//2

        self.melW = librosa.filters.mel(sr=sr, n_fft=n_fft, n_mels=n_mels,
            fmin=fmin, fmax=fmax).T
        # (n_fft // 2 + 1, mel_bins)

        self.melW = tf.Variable(self.melW, dtype=tf.float32)

        if freeze_parameters:
            self.non_trainable_weights.append(self.melW)
        else:
            self.trainable_weights.append(self.melW)

    def call(self, input):
        r"""Calculate (log) mel spectrogram from spectrogram.
        Args:
            input: (*, n_fft), spectrogram
        
        Returns: 
            output: (*, mel_bins), (log) mel spectrogram
        """

        # Mel spectrogram
        input = tf.cast(input, dtype=self.melW.dtype)
        mel_spectrogram = tf.matmul(input, self.melW)
        #print("input mel: ",mel_spectrogram.dtype, input.dtype, self.melW.dtype)

        # (*, mel_bins)

        # Logmel spectrogram
        if self.is_log:
            output = self.power_to_db(mel_spectrogram)
        else:
            output = mel_spectrogram
        #+print(output.dtype)
        return output

    def _tf_log10(self, x):
        numerator =  tf.math.log(x) 
        denominator = tf.cast(tf.math.log(tf.constant(10.0)), dtype=numerator.dtype)
        return numerator / denominator

    def power_to_db(self, input):
        r"""Power to db, this function is the pytorch implementation of 
        librosa.power_to_lb
        """
        ref_value = self.ref
        # print(input.dtype)
        # print(tf.reduce_max(input))
        # print(tf.clip_by_value(tf.cast(input, tf.float32), self.amin, 10 ))

        log_spec = 10.0 * self._tf_log10(tf.maximum(self.amin, input))
        log_spec -= 10.0 * self._tf_log10(tf.maximum(self.amin, ref_value))

        if self.top_db is not None:
            if self.top_db < 0:
                raise librosa.util.exceptions.ParameterError('top_db must be non-negative')
            log_spec = tf.math.maximum(log_spec, tf.math.reduce_max(log_spec) - self.top_db) #tf.clip_by_value(log_spec, min=log_spec.max().item() - self.top_db, max=np.inf)

        return log_spec



def magphase(real, imag):
    r"""Calculate magnitude and phase from real and imag part of signals.

    Args:
        real: tensor, real part of signals
        imag: tensor, imag part of signals

    Returns:
        mag: tensor, magnitude of signals
        cos: tensor, cosine of phases of signals
        sin: tensor, sine of phases of signals
    """
    mag = (real ** 2 + imag ** 2) ** 0.5
    cos = real / tf.clip_by_value(mag, 1e-10, np.inf)
    sin = imag / tf.clip_by_value(mag, 1e-10, np.inf)

    return mag, cos, sin


'''
class ISTFT(DFTBase):
    def __init__(self, n_fft=2048, hop_length=None, win_length=None,
        window='hann', center=True, pad_mode='reflect', freeze_parameters=True, 
        frames_num=None):
        """Tensorflow implementation of ISTFT with Conv1d. The function has the 
        same output as librosa.istft.
        torch.nn.Fold has no equivalent in TF for the moment.

        Args:
            n_fft: int, fft window size, e.g., 2048
            hop_length: int, hop length samples, e.g., 441
            win_length: int, window length e.g., 2048
            window: str, window function name, e.g., 'hann'
            center: bool
            pad_mode: str, e.g., 'reflect'
            freeze_parameters: bool, set to True to freeze all parameters. Set
                to False to finetune all parameters.
             
            frames_num: None | int, number of frames of audio clips to be 
                inferneced. Only useable when onnx=True.
            device: None | str, device of ONNX. Only useable when onnx=True.
        """
        super(ISTFT, self).__init__()

        assert pad_mode in ['constant', 'reflect']

        self.n_fft = n_fft
        self.hop_length = hop_length
        self.win_length = win_length
        self.window = window
        self.center = center
        self.pad_mode = pad_mode
      

        # By default, use the entire frame.
        if self.win_length is None:
            self.win_length = self.n_fft

        # Set the default hop, if it's not already specified.
        if self.hop_length is None:
            self.hop_length = int(self.win_length // 4)

        # Initialize Conv1d modules for calculating real and imag part of DFT.
        self.init_real_imag_conv()

        # Initialize overlap add window for reconstruct time domain signals.
        self.init_overlap_add_window()

        if freeze_parameters:
            self.non_trainable_weights.append(self.W)
            self.non_trainable_weights.append(self.conv_real)
            self.non_trainable_weights.append(self.conv_imag)

    def init_conv(self, input_size):
        s = tf.constant(np.random.uniform(0,1,(1,  5000, input_size)).astype(np.float32))
        self.conv_real(s)
        self.conv_imag(s)

    def init_real_imag_conv(self):
        r"""Initialize Conv1d for calculating real and imag part of DFT.
        """
        self.W = self.idft_matrix(self.n_fft) / self.n_fft

        self.conv_real = tf.keras.layers.Conv1D(filters=self.n_fft,
            kernel_size=1, strides=1, padding='valid', dilation_rate=1,
            groups=1, use_bias=False) # in_channels=self.n_fft, 

        self.conv_imag = tf.keras.layers.Conv1D(filters=self.n_fft,
            kernel_size=1, strides=1, padding='valid', dilation_rate=1,
            groups=1, use_bias=False)
        self.init_conv(self.n_fft)
        ifft_window = librosa.filters.get_window(self.window, self.win_length, fftbins=True)
        # (win_length,)

        # Pad the window to n_fft
        ifft_window = librosa.util.pad_center(data=ifft_window, size=self.n_fft)
        #print(self.conv_real.get_weights()[0].shape, self.conv_imag.get_weights()[0].shape)
        self.conv_real.set_weights([np.real(self.W * ifft_window[None, :])[None, :, :]])
        # (n_fft // 2 + 1, 1, n_fft)
        
        #print(np.imag(self.W * ifft_window[None, :]).shape)
        self.conv_imag.set_weights([np.imag(self.W * ifft_window[None, :])[None, :, :]])
        # (n_fft // 2 + 1, 1, n_fft)

    def init_overlap_add_window(self):
        r"""Initialize overlap add window for reconstruct time domain signals.
        """
        
        ola_window = librosa.filters.get_window(self.window, self.win_length, fftbins=True)
        # (win_length,)

        ola_window = librosa.util.normalize(ola_window, norm=None) ** 2
        ola_window = librosa.util.pad_center(data=ola_window, size=self.n_fft)
        ola_window = tf.Variable(ola_window)

        #self.register_buffer('ola_window', ola_window)
        # (win_length,)
 

    def call(self, real_stft, imag_stft, length):
        r"""Calculate inverse STFT.

        Args:
            real_stft: (batch_size,   time_steps, n_fft // 2 + 1)
            imag_stft: (batch_size,   time_steps, n_fft // 2 + 1)
            length: int
        
        Returns:
            real: (batch_size, data_length), output signals.
        """
        assert len(real_stft.shape) == 3 and len(imag_stft.shape) == 3
        batch_size, _, frames_num = real_stft.shape

        #real_stft = real_stft[:,  :, :]#.transpose(1, 2)
        #imag_stft = imag_stft[:,  :, :]#.transpose(1, 2)
        # (batch_size, n_fft // 2 + 1, time_steps)

        # Get full stft representation from spectrum using symmetry attribute.
        full_real_stft, full_imag_stft = self._get_full_stft(real_stft, imag_stft)
        # full_real_stft: (batch_size, n_fft, time_steps)
        # full_imag_stft: (batch_size, n_fft, time_steps)

        # Calculate IDFT frame by frame.
        s_real = self.conv_real(full_real_stft) - self.conv_imag(full_imag_stft)
        # (batch_size, n_fft, time_steps)

        # Overlap add signals in frames to reconstruct signals.
        y = self._overlap_add_divide_window_sum(s_real, frames_num)
        # y: (batch_size, audio_samples + win_length,)
        
        y = self._trim_edges(y, length)
        # (batch_size, audio_samples,)
            
        return y

    def _get_full_stft(self, real_stft, imag_stft):
        r"""Get full stft representation from spectrum using symmetry attribute.

        Args:
            real_stft: (batch_size, n_fft // 2 + 1, time_steps)
            imag_stft: (batch_size, n_fft // 2 + 1, time_steps)

        Returns:
            full_real_stft: (batch_size, n_fft, time_steps)
            full_imag_stft: (batch_size, n_fft, time_steps)
        """
        batch_size, timesteps, num_channels = real_stft.shape
        print(batch_size, timesteps, num_channels)
        #full_real_stft = torch.cat((real_stft, torch.flip(real_stft[:, 1 : -1, :], dims=[1])), dim=1)
        #full_imag_stft = torch.cat((imag_stft, - torch.flip(imag_stft[:, 1 : -1, :], dims=[1])), dim=1)
        full_real_stft = tf.concat((real_stft, tf.reverse(tf.slice(real_stft, [0,0,1], [batch_size, timesteps, num_channels - 2]), axis=[2]) ), axis=2)
        full_imag_stft = tf.concat((imag_stft, - tf.reverse(tf.slice(imag_stft, [0,0,1],[batch_size, timesteps, num_channels - 2]),  axis=[2]) ), axis=2)

        return full_real_stft, full_imag_stft

     

    def _overlap_add_divide_window_sum(self, s_real, frames_num):
        r"""Overlap add signals in frames to reconstruct signals.

        Args:
            s_real: (batch_size, n_fft, time_steps), signals in frames
            frames_num: int

        Returns:
            y: (batch_size, audio_samples)
        """
        
        output_samples = (s_real.shape[-1] - 1) * self.hop_length + self.win_length
        # (audio_samples,)

        # Overlap-add signals in frames to signals. Ref: 
        # asteroid_filterbanks.torch_stft_fb.torch_stft_fb() from
        # https://github.com/asteroid-team/asteroid-filterbanks
        y = torch.nn.functional.fold(input=s_real, output_size=(1, output_samples), 
            kernel_size=(1, self.win_length), stride=(1, self.hop_length))
        # (batch_size, 1, 1, audio_samples,)
        
        y = y[:, 0, 0, :]
        # (batch_size, audio_samples)

        # Get overlap-add window sum to be divided.
        ifft_window_sum = self._get_ifft_window(frames_num)
        # (audio_samples,)

        # Following code is abandaned for divide overlap-add window, because
        # not supported by half precision training and ONNX.
        # min_mask = ifft_window_sum.abs() < 1e-11
        # y[:, ~min_mask] = y[:, ~min_mask] / ifft_window_sum[None, ~min_mask]
        # # (batch_size, audio_samples)

        ifft_window_sum = tf.clip_by_value(ifft_window_sum, 1e-11, np.inf)
        # (audio_samples,)

        y = y / ifft_window_sum[None, :]
        # (batch_size, audio_samples,)

        return y

    def _get_ifft_window(self, frames_num):
        r"""Get overlap-add window sum to be divided.

        Args:
            frames_num: int

        Returns:
            ifft_window_sum: (audio_samlpes,), overlap-add window sum to be 
            divided.
        """
        
        output_samples = (frames_num - 1) * self.hop_length + self.win_length
        # (audio_samples,)

        window_matrix = self.ola_window[None, :, None].repeat(1, 1, frames_num)
        # (batch_size, win_length, time_steps)

        ifft_window_sum = F.fold(input=window_matrix, 
            output_size=(1, output_samples), kernel_size=(1, self.win_length), 
            stride=(1, self.hop_length))
        # (1, 1, 1, audio_samples)
        
        ifft_window_sum = ifft_window_sum.squeeze()
        # (audio_samlpes,)

        return ifft_window_sum

    def _trim_edges(self, y, length):
        r"""Trim audio.

        Args:
            y: (audio_samples,)
            length: int

        Returns:
            (trimmed_audio_samples,)
        """
        # Trim or pad to length
        if length is None:
            if self.center:
                y = y[:, self.n_fft // 2 : -self.n_fft // 2]
        else:
            if self.center:
                start = self.n_fft // 2
            else:
                start = 0

            y = y[:, start : start + length]

        return y

'''






if __name__ == "__main__":
    stft = STFT(n_fft=2048, hop_length=512, win_length=None,
        window='hann', center=True, pad_mode='reflect') 
    istft = ISTFT(n_fft=2048, hop_length=512, win_length=None,
        window='hann', center=True, pad_mode='reflect', freeze_parameters=True, 
        frames_num=None)

    audio = np.random.uniform(0,1 , (32000 * 5, ))
    audio = audio.reshape(1,-1)

    real_frame, imag_frame = stft(audio)
    print(real_frame.shape)
    y = istft(real_frame, imag_frame, 32000 * 5)
