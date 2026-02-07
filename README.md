# Image Hashing

This repository contains implementations of common image hashing algorithms in Python. These algorithms are useful for image similarity, duplicate detection, and reverse image search.

## Algorithms Implemented

*   **Average Hash (aHash)**: Fast and suitable for finding strictly identical or near-identical images.
*   **Difference Hash (dHash)**: More robust to color shifts and minor edits than aHash. (Horizontal and Vertical variants available).
*   **Perceptual Hash (pHash)**: Robust to scaling, aspect ratio changes, and minor coloring/brightness changes. Uses Discrete Cosine Transform (DCT).
*   **Wavelet Hash (wHash)**: Uses Discrete Wavelet Transform (DWT).
*   **Color Hash**: Hashes color distribution.
*   **Crop Resistant Hash**: Robust to cropping by segmenting the image.

## Installation

1.  Clone the repository.
2.  Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```python
from PIL import Image
from image_hashing import average_hash, dhash, dhash_vertical, phash, whash, crop_resistant_hash, hamming_distance

# Load an image
image_path = 'path/to/image.jpg'
# or using PIL directly: image = Image.open(...)

# Compute hashes (functions return hex strings directly)
a_hash = average_hash(image_path)
d_hash_val = dhash(image_path)
d_hash_v = dhash_vertical(image_path)
p_hash = phash(image_path)
w_hash = whash(image_path)

print(f"Average Hash: {a_hash}")
print(f"Difference Hash: {d_hash_val}")
print(f"Vertical Difference Hash: {d_hash_v}")
print(f"Perceptual Hash: {p_hash}")
print(f"Wavelet Hash: {w_hash}")

# Crop Resistant Hash returns a list of hashes
crop_hashes = crop_resistant_hash(image_path)
print(f"Crop Resistant Hashes: {crop_hashes}")

# Compare two images
image1 = 'path/to/image1.jpg'
image2 = 'path/to/image2.jpg'

hash1 = phash(image1)
hash2 = phash(image2)

distance = hamming_distance(hash1, hash2)
print(f"Hamming distance: {distance}")

if distance < 5:
    print("Images are similar")
else:
    print("Images are different")
```

## Testing

Run unit tests with:

```bash
python -m unittest discover tests
```
