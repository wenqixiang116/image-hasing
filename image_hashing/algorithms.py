from PIL import Image
import numpy as np
import scipy.fftpack
import scipy.ndimage
import pywt

def _open_image(image):
    if not isinstance(image, Image.Image):
        return Image.open(image)
    return image

def average_hash(image, hash_size=8):
    """
    Average Hash computation
    """
    image = _open_image(image)
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
    image = _open_image(image)
    # Resize to (hash_size + 1) x hash_size
    image = image.resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)

    # Grayscale
    image = image.convert("L")

    # Compute differences
    pixels = np.asarray(image)
    # Compare pixel[x, y] to pixel[x+1, y]
    diff = pixels[:, 1:] > pixels[:, :-1]

    return _binary_array_to_hex(diff.flatten())

def dhash_vertical(image, hash_size=8):
    """
    Difference Hash computation (vertical).
    """
    image = _open_image(image)
    # Resize to hash_size x (hash_size + 1)
    image = image.resize((hash_size, hash_size + 1), Image.Resampling.LANCZOS)

    # Grayscale
    image = image.convert("L")

    # Compute differences
    pixels = np.asarray(image)
    # Compare pixel[x, y] to pixel[x, y+1]
    diff = pixels[1:, :] > pixels[:-1, :]

    return _binary_array_to_hex(diff.flatten())

def phash(image, hash_size=8, highfreq_factor=4):
    """
    Perceptual Hash computation.
    """
    image = _open_image(image)
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
    image = _open_image(image)
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
    image = _open_image(image)
    image = image.convert("RGB")
    hashes = []
    for band in image.split():
        hashes.append(average_hash(band, hash_size=hash_size))
    return "".join(hashes)

def crop_resistant_hash(image, hash_func=dhash, min_segment_size=500, segmentation_image_size=300):
    """
    Crop Resistant Hash computation.
    """
    image = _open_image(image)

    # To avoid modifying original image when doing segmentation
    orig_image = image.copy()

    # Segmentation
    image = image.resize((segmentation_image_size, segmentation_image_size), Image.Resampling.LANCZOS)
    image = image.convert("L")

    # Thresholding
    pixels = np.asarray(image)
    bw_image = pixels > 128

    # Find connected components
    labeled_image, nb_labels = scipy.ndimage.label(bw_image)

    # Find objects
    objects = scipy.ndimage.find_objects(labeled_image)

    hashes = []
    for i, slice_tuple in enumerate(objects):
        y_slice, x_slice = slice_tuple
        height = y_slice.stop - y_slice.start
        width = x_slice.stop - x_slice.start

        if width * height < min_segment_size:
            continue

        # Map back to original image
        scale_w = orig_image.width / segmentation_image_size
        scale_h = orig_image.height / segmentation_image_size

        x_start = int(x_slice.start * scale_w)
        y_start = int(y_slice.start * scale_h)
        x_end = int(x_slice.stop * scale_w)
        y_end = int(y_slice.stop * scale_h)

        # Ensure valid crop
        if x_end <= x_start or y_end <= y_start:
             continue

        orig_crop = orig_image.crop((x_start, y_start, x_end, y_end))

        hashes.append(hash_func(orig_crop))

    if not hashes:
        return [hash_func(orig_image)]

    return hashes

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
