from PIL import Image
import numpy as np
import scipy.fftpack
import scipy.ndimage
import pywt

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

def whash(image, hash_size=8):
    """
    Wavelet Hash computation.
    """
    image_scale = hash_size * 2
    # Resize to image_scale x image_scale
    image = image.resize((image_scale, image_scale), Image.Resampling.LANCZOS)

    # Grayscale
    image = image.convert("L")

    pixels = np.asarray(image) / 255.0

    # Compute DWT
    coeffs = pywt.dwt2(pixels, 'haar')
    LL, (LH, HL, HH) = coeffs

    # Compute median
    med = np.median(LL)

    # Compute bits
    diff = LL > med

    return _binary_array_to_hex(diff.flatten())

def colorhash(image, hash_size=8):
    """
    Color Hash computation.
    """
    image = image.convert("RGB")
    hashes = []
    for band in image.split():
        hashes.append(average_hash(band, hash_size=hash_size))
    return "".join(hashes)

def dhash_vertical(image, hash_size=8):
    """
    Vertical Difference Hash computation.
    """
    # Resize to hash_size x (hash_size + 1)
    image = image.resize((hash_size, hash_size + 1), Image.Resampling.LANCZOS)

    # Grayscale
    image = image.convert("L")

    # Compute differences
    pixels = np.asarray(image)
    # Compare pixel[x, y] to pixel[x, y+1]
    diff = pixels[1:, :] > pixels[:-1, :]

    return _binary_array_to_hex(diff.flatten())

def marr_hildreth_hash(image, hash_size=8, scale=4, sigma=2.5):
    """
    Marr-Hildreth Hash computation.
    """
    img_size = hash_size * scale

    # Resize
    image = image.resize((img_size, img_size), Image.Resampling.LANCZOS)

    # Grayscale
    image = image.convert("L")
    pixels = np.asarray(image).astype(float)

    # Apply Laplacian of Gaussian
    blocks = scipy.ndimage.gaussian_laplace(pixels, sigma=sigma)

    # Subsample to get final hash bits
    # Subsampling by taking every 'scale'-th pixel
    blocks = blocks[::scale, ::scale]

    diff = blocks < 0
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
