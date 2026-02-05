# Image Hashing

This repository contains implementations of common image hashing algorithms in Python. These algorithms are useful for image similarity, duplicate detection, and reverse image search.

## Algorithms Implemented

*   **Average Hash (aHash)**: Fast and suitable for finding strictly identical or near-identical images.
*   **Difference Hash (dHash)**: More robust to color shifts and minor edits than aHash.
*   **Difference Hash Vertical (dHash Vertical)**: Vertical variation of dHash.
*   **Perceptual Hash (pHash)**: Robust to scaling, aspect ratio changes, and minor coloring/brightness changes. Uses Discrete Cosine Transform (DCT).
*   **Wavelet Hash (wHash)**: Similar to pHash but uses Discrete Wavelet Transform (DWT).
*   **Color Hash**: Hashes based on color distribution.
*   **Marr-Hildreth Hash**: Uses Marr-Hildreth operator (Laplacian of Gaussian) to detect edges.

## Installation

1.  Clone the repository.
2.  Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```python
from PIL import Image
from image_hashing import average_hash, difference_hash, phash, whash, colorhash, dhash_vertical, marr_hildreth_hash, hamming_distance

# Load an image
image_path = 'path/to/image.jpg'
# or using PIL directly: image = Image.open(...)

# Compute hashes
a_hash = average_hash(image_path)
d_hash = difference_hash(image_path)
p_hash = phash(image_path)
w_hash = whash(image_path)
c_hash = colorhash(image_path)
dv_hash = dhash_vertical(image_path)
mh_hash = marr_hildreth_hash(image_path)

print(f"Average Hash: {a_hash}")
print(f"Difference Hash: {d_hash}")
print(f"Perceptual Hash: {p_hash}")
print(f"Wavelet Hash: {w_hash}")
print(f"Color Hash: {c_hash}")
print(f"Difference Hash Vertical: {dv_hash}")
print(f"Marr-Hildreth Hash: {mh_hash}")

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
