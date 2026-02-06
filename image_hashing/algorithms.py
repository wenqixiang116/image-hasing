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

def dhash_vertical(image, hash_size=8):
    """
    Difference Hash computation (vertical).
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

def crop_resistant_hash(image, hash_func=dhash, min_segment_size=500, segmentation_image_size=300):
    """
    Computes a hash that is resistant to cropping.
    It splits the image into segments and computes the hash for each segment.
    Returns a list of hex strings.
    """
    # Resize for segmentation
    w, h = image.size
    scale = segmentation_image_size / max(w, h)
    seg_size = (int(w * scale), int(h * scale))
    image_seg = image.resize(seg_size, Image.Resampling.LANCZOS)

    # Convert to binary
    image_seg = image_seg.convert("L")
    pixels = np.asarray(image_seg)
    # Thresholding: using mean
    bw_pixels = pixels > pixels.mean()

    # Find connected components
    labeled_array, num_features = scipy.ndimage.label(bw_pixels)

    hashes = []

    # Also add the full image hash
    hashes.append(hash_func(image))

    if num_features > 0:
        find_objects = scipy.ndimage.find_objects(labeled_array)
        for i, slice_obj in enumerate(find_objects):
            # slice_obj is a tuple of slices (slice(row_start, row_end), slice(col_start, col_end))
            row_slice, col_slice = slice_obj

            # Check size
            height = row_slice.stop - row_slice.start
            width = col_slice.stop - col_slice.start
            if width * height < min_segment_size:
                continue

            # Map back to original image
            # row is y, col is x
            y1 = int(row_slice.start / scale)
            y2 = int(row_slice.stop / scale)
            x1 = int(col_slice.start / scale)
            x2 = int(col_slice.stop / scale)

            # Crop
            # Ensure within bounds
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(w, x2)
            y2 = min(h, y2)

            if x2 - x1 <= 0 or y2 - y1 <= 0:
                continue

            crop = image.crop((x1, y1, x2, y2))
            hashes.append(hash_func(crop))

    # Remove duplicates but preserve order
    return list(dict.fromkeys(hashes))

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
