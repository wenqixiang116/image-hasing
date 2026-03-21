# Image Hashing

This repository contains implementations of common image hashing algorithms in Python. These algorithms are useful for image similarity, duplicate detection, and reverse image search.

## Algorithms Implemented

*   **Average Hash (aHash)**: Fast and suitable for finding strictly identical or near-identical images.
*   **Difference Hash (dHash)**: More robust to color shifts and minor edits than aHash.
*   **Vertical Difference Hash (dHash Vertical)**: Similar to dHash, but compares adjacent rows instead of adjacent columns.
*   **Perceptual Hash (pHash)**: Robust to scaling, aspect ratio changes, and minor coloring/brightness changes. Uses Discrete Cosine Transform (DCT).
*   **Wavelet Hash (wHash)**: Uses Discrete Wavelet Transform (DWT), operating similarly to pHash but with wavelets.
*   **Color Hash**: Computes the average hash for each color channel.
*   **Marr-Hildreth Hash**: Uses the Marr-Hildreth operator (Laplacian of Gaussian) for edge detection, followed by zero-crossing extraction.

## Installation

1.  Clone the repository.
2.  Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```python
from PIL import Image
from image_hashing import average_hash, difference_hash, phash, hamming_distance, hash_to_hex

# Load an image
image_path = 'path/to/image.jpg'
# or using PIL directly: image = Image.open(...)

# Compute hashes
a_hash = average_hash(image_path)
d_hash = difference_hash(image_path)
p_hash = phash(image_path)

print(f"Average Hash: {hash_to_hex(a_hash)}")
print(f"Difference Hash: {hash_to_hex(d_hash)}")
print(f"Perceptual Hash: {hash_to_hex(p_hash)}")

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
