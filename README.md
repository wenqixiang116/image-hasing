# Image Hashing

This repository contains implementations of common image hashing algorithms in Python. These algorithms are useful for image similarity, duplicate detection, and reverse image search.

## Algorithms Implemented

*   **Average Hash (aHash)**: Fast and suitable for finding strictly identical or near-identical images.
*   **Difference Hash (dHash)**: More robust to color shifts and minor edits than aHash.
*   **Difference Hash Vertical (dHash Vertical)**: Variation of dHash that computes vertical differences.
*   **Perceptual Hash (pHash)**: Robust to scaling, aspect ratio changes, and minor coloring/brightness changes. Uses Discrete Cosine Transform (DCT).
*   **Wavelet Hash (wHash)**: Similar to pHash but uses Discrete Wavelet Transform (DWT).
*   **Marr-Hildreth Hash**: Edge-based hash using Marr-Hildreth operator (Laplacian of Gaussian).
*   **Color Hash**: Combines hashing of individual color channels.

## Installation

1.  Clone the repository.
2.  Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```python
from PIL import Image
from image_hashing import average_hash, dhash, phash, whash, colorhash, dhash_vertical, marr_hildreth_hash, hamming_distance

# Load an image
image_path = 'path/to/image.jpg'
# or using PIL directly:
img = Image.open(image_path)

# Compute hashes (returns hex strings)
a_hash = average_hash(img)
d_hash = dhash(img)
p_hash = phash(img)
w_hash = whash(img)
m_hash = marr_hildreth_hash(img)
dv_hash = dhash_vertical(img)
c_hash = colorhash(img)

print(f"Average Hash: {a_hash}")
print(f"Difference Hash: {d_hash}")
print(f"Perceptual Hash: {p_hash}")
print(f"Wavelet Hash: {w_hash}")
print(f"Marr-Hildreth Hash: {m_hash}")

# Compare two images
image1 = Image.open('path/to/image1.jpg')
image2 = Image.open('path/to/image2.jpg')

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
