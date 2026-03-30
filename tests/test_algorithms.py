import unittest
from PIL import Image
import numpy as np
from image_hashing import average_hash, dhash, phash, hamming_distance, dhash_vertical

class TestHashing(unittest.TestCase):
    def setUp(self):
        # Create a simple image: black on left, white on right
        self.image = Image.new('RGB', (100, 100), color='black')
        for x in range(50, 100):
            for y in range(100):
                self.image.putpixel((x, y), (255, 255, 255))

        # Create an image that is vertically split: black on top, white on bottom
        self.image_vertical = Image.new('RGB', (100, 100), color='black')
        for x in range(100):
            for y in range(50, 100):
                self.image_vertical.putpixel((x, y), (255, 255, 255))

    def test_average_hash(self):
        h = average_hash(self.image)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 16) # 64 bits = 16 hex chars

        # Test consistency
        h2 = average_hash(self.image)
        self.assertEqual(h, h2)

    def test_dhash(self):
        h = dhash(self.image)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 16)

        h2 = dhash(self.image)
        self.assertEqual(h, h2)

    def test_dhash_vertical(self):
        h = dhash_vertical(self.image_vertical)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 16)

        h2 = dhash_vertical(self.image_vertical)
        self.assertEqual(h, h2)

    def test_phash(self):
        h = phash(self.image)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 16)

        h2 = phash(self.image)
        self.assertEqual(h, h2)

    def test_hamming_distance(self):
        h1 = "0000000000000000"
        h2 = "0000000000000001"
        self.assertEqual(hamming_distance(h1, h2), 1)

        h3 = "ffffffffffffffff"
        self.assertEqual(hamming_distance(h1, h3), 64)

    def test_hashes_are_different(self):
        # Create another image
        image2 = Image.new('RGB', (100, 100), color='white')

        h_ahash = average_hash(self.image)
        h_ahash2 = average_hash(image2)

        # They should be different
        self.assertNotEqual(h_ahash, h_ahash2)

        h_dhash = dhash(self.image)
        h_dhash2 = dhash(image2)
        self.assertNotEqual(h_dhash, h_dhash2)

        h_dhash_v = dhash_vertical(self.image_vertical)
        h_dhash_v2 = dhash_vertical(image2)
        self.assertNotEqual(h_dhash_v, h_dhash_v2)

        h_phash = phash(self.image)
        h_phash2 = phash(image2)
        self.assertNotEqual(h_phash, h_phash2)
