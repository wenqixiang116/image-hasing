from PIL import Image
import numpy as np
import scipy.fftpack
import scipy.ndimage

def _binary_array_to_hex(arr):
    """
    internal function to convert a binary array to a hex string.
    """
    h = 0
    s = []
    for i, v in enumerate(arr.flatten()):
        if v:
            h += 2**(i % 8)
        if (i % 8) == 7:
            s.append(hex(h)[2:].rjust(2, '0'))
            h = 0
    if (len(arr.flatten()) % 8) != 0:
        s.append(hex(h)[2:].rjust(2, '0'))
    return "".join(s)

def hash_to_hex(hash_array):
    """
    Convert a hash array to a hex string.
    """
    return _binary_array_to_hex(hash_array)

def hex_to_hash(hexstr):
    """
    Convert a hex string to a hash array.
    """
    l = []
    if len(hexstr) % 2 != 0:
        raise ValueError('Hex string must have even length')
    for i in range(0, len(hexstr), 2):
        h = int(hexstr[i:i+2], 16)
        for j in range(8):
            l.append((h >> j) & 1)

    # Assuming square hash
    size = int(len(l)**0.5)
    return np.array(l, dtype=bool).reshape((size, size))

def average_hash(image, hash_size=8):
    """
    Compute the average hash of the given image.
    """
    if isinstance(image, str):
        image = Image.open(image)

    image = image.convert("L").resize((hash_size, hash_size), Image.Resampling.LANCZOS)
    pixels = np.asarray(image)
    avg = pixels.mean()
    diff = pixels > avg
    return diff

def difference_hash(image, hash_size=8):
    """
    Compute the difference hash of the given image.
    """
    if isinstance(image, str):
        image = Image.open(image)

    image = image.convert("L").resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    pixels = np.asarray(image)
    # compare to pixel to the right
    diff = pixels[:, 1:] > pixels[:, :-1]
    return diff

def dhash_vertical(image, hash_size=8):
    """
    Compute the vertical difference hash of the given image.
    """
    if isinstance(image, str):
        image = Image.open(image)

    image = image.convert("L").resize((hash_size, hash_size + 1), Image.Resampling.LANCZOS)
    pixels = np.asarray(image)
    # compare pixel to the one below it
    diff = pixels[1:, :] > pixels[:-1, :]
    return diff

def marr_hildreth_hash(image, hash_size=8, alpha=2.5, scale=4):
    """
    Compute the Marr-Hildreth hash of the given image.
    """
    if isinstance(image, str):
        image = Image.open(image)

    image = image.convert("L").resize((hash_size * scale, hash_size * scale), Image.Resampling.LANCZOS)
    pixels = np.asarray(image, dtype=np.float32)

    blocks = scipy.ndimage.gaussian_laplace(pixels, sigma=alpha)

    # Subsample
    subsampled = blocks[::scale, ::scale]

    diff = subsampled < 0
    return diff

def phash(image, hash_size=8, highfreq_factor=4):
    """
    Compute the perceptual hash of the given image.
    """
    if isinstance(image, str):
        image = Image.open(image)

    img_size = hash_size * highfreq_factor
    image = image.convert("L").resize((img_size, img_size), Image.Resampling.LANCZOS)
    pixels = np.asarray(image)

    dct = scipy.fftpack.dct(scipy.fftpack.dct(pixels, axis=0), axis=1)
    dctlowfreq = dct[:hash_size, :hash_size]
    med = np.median(dctlowfreq)
    diff = dctlowfreq > med
    return diff

def hamming_distance(hash1, hash2):
    """
    Compute the hamming distance between two hashes.
    """
    if hash1.shape != hash2.shape:
         raise ValueError("Hash shapes must match")
    return np.count_nonzero(hash1 != hash2)
