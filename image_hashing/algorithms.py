from PIL import Image
import numpy as np
import scipy.fftpack

def average_hash(image, hash_size=8):
    """
    Average Hash computation
    """
    # Resize to hash_size x hash_size
    image = image.resize((hash_size, hash_size), Image.Resampling.LANCZOS)

    # Grayscale
    image = image.convert("L")

    # Compute average
    pixels = np.asarray(image)
    avg = pixels.mean()

    # Compute bits
    diff = pixels > avg

    return _binary_array_to_hex(diff.flatten())

def dhash(image, hash_size=8):
    """
    Difference Hash computation.
    """
    # Resize to (hash_size + 1) x hash_size
    image = image.resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)

    # Grayscale
    image = image.convert("L")

    # Compute differences
    pixels = np.asarray(image)
    # Compare pixel[x, y] to pixel[x+1, y]
    diff = pixels[:, 1:] > pixels[:, :-1]

    return _binary_array_to_hex(diff.flatten())

def phash(image, hash_size=8, highfreq_factor=4):
    """
    Perceptual Hash computation.
    """
    img_size = hash_size * highfreq_factor

    # Resize
    image = image.resize((img_size, img_size), Image.Resampling.LANCZOS)

    # Grayscale
    image = image.convert("L")

    # DCT
    pixels = np.asarray(image)
    dct = scipy.fftpack.dct(scipy.fftpack.dct(pixels, axis=0), axis=1)

    # Reduce DCT
    dctlowfreq = dct[:hash_size, :hash_size]

    # Average
    # Exclude the first term (DC term) from average computation
    dctlowfreq_flat = dctlowfreq.flatten()
    avg = (np.sum(dctlowfreq_flat) - dctlowfreq_flat[0]) / (dctlowfreq_flat.size - 1)

    # Compute bits
    diff = dctlowfreq > avg

    return _binary_array_to_hex(diff.flatten())

def _binary_array_to_hex(arr):
    """
    Convert a binary array to a hex string.
    """
    bit_string = "".join(str(int(b)) for b in arr)
    return "{:0>{width}x}".format(int(bit_string, 2), width=len(arr)//4)

def hamming_distance(hash1, hash2):
    """
    Compute Hamming distance between two hex hash strings.
    """
    h1 = int(hash1, 16)
    h2 = int(hash2, 16)

    x = h1 ^ h2
    return bin(x).count('1')
