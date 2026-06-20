import unittest
import numpy as np
from PIL import Image, ImageDraw
from image_hashing.hashing import average_hash, difference_hash, dhash_vertical, phash, marr_hildreth_hash, hamming_distance, hash_to_hex, hex_to_hash

class TestHashing(unittest.TestCase):
    def setUp(self):
        # Create a simple image (100x100, white background, black square in middle)
        self.img1 = Image.new('RGB', (100, 100), color='white')
        d = ImageDraw.Draw(self.img1)
        d.rectangle([25, 25, 75, 75], fill='black')

        # Create a slightly modified image (noise or slight shift)
        # Here I just make it slightly smaller
        self.img2 = self.img1.resize((90, 90))

        # Create a completely different image
        self.img3 = Image.new('RGB', (100, 100), color='black')

    def test_average_hash(self):
        h1 = average_hash(self.img1)
        h2 = average_hash(self.img2)
        h3 = average_hash(self.img3)

        self.assertTrue(h1.shape == (8, 8))
        # Hash of image and its resized version should be very similar
        self.assertLess(hamming_distance(h1, h2), 5)
        # Hash of different images should be different
        self.assertGreater(hamming_distance(h1, h3), 10)

    def test_difference_hash(self):
        h1 = difference_hash(self.img1)
        h2 = difference_hash(self.img2)
        h3 = difference_hash(self.img3)

        self.assertTrue(h1.shape == (8, 8))
        self.assertLess(hamming_distance(h1, h2), 5)
        self.assertGreater(hamming_distance(h1, h3), 10)

    def test_dhash_vertical(self):
        # Create an image with vertical split
        img_vert = Image.new('RGB', (100, 100), color='white')
        d = ImageDraw.Draw(img_vert)
        d.rectangle([0, 50, 100, 100], fill='black')

        h1 = dhash_vertical(img_vert)
        self.assertTrue(h1.shape == (8, 8))
        # Should not be all zeros since there is vertical variation
        self.assertTrue(np.any(h1))

        h2 = dhash_vertical(self.img3) # all black image
        self.assertFalse(np.any(h2))

    def test_phash(self):
        h1 = phash(self.img1)
        h2 = phash(self.img2)
        h3 = phash(self.img3)

        self.assertTrue(h1.shape == (8, 8))
        self.assertLess(hamming_distance(h1, h2), 5)
        self.assertGreater(hamming_distance(h1, h3), 10)

    def test_marr_hildreth_hash(self):
        h1 = marr_hildreth_hash(self.img1)
        h2 = marr_hildreth_hash(self.img2)
        h3 = marr_hildreth_hash(self.img3)

        self.assertTrue(h1.shape == (8, 8))
        self.assertLess(hamming_distance(h1, h2), 5)
        self.assertGreater(hamming_distance(h1, h3), 10)

    def test_hex_conversion(self):
        h1 = average_hash(self.img1)
        hex_str = hash_to_hex(h1)
        h_back = hex_to_hash(hex_str)

        self.assertTrue(np.array_equal(h1, h_back))

    def test_hamming_distance(self):
        h1 = np.zeros((8, 8), dtype=bool)
        h2 = np.zeros((8, 8), dtype=bool)
        h2[0, 0] = True

        self.assertEqual(hamming_distance(h1, h2), 1)

    def test_non_byte_aligned_hex_conversion(self):
        # 9 bits: 11111111 1 -> ff 01
        arr = np.ones((1, 9), dtype=bool)
        hex_str = hash_to_hex(arr)
        self.assertEqual(hex_str, "ff01")

if __name__ == '__main__':
    unittest.main()
