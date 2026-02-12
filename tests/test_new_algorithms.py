import unittest
import numpy as np
import tempfile
import os
from PIL import Image, ImageDraw
from image_hashing.hashing import dhash_vertical as core_dhash_vertical, marr_hildreth_hash as core_marr_hildreth_hash, whash as core_whash, hamming_distance as core_hamming_distance
from image_hashing.algorithms import dhash_vertical, marr_hildreth_hash, whash, hamming_distance as hex_hamming_distance

class TestNewAlgorithms(unittest.TestCase):
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

    def test_dhash_vertical(self):
        # Test core implementation
        h1 = core_dhash_vertical(self.img1)
        h2 = core_dhash_vertical(self.img2)
        h3 = core_dhash_vertical(self.img3)

        self.assertTrue(h1.shape == (8, 8))
        self.assertLess(core_hamming_distance(h1, h2), 5)
        self.assertGreater(core_hamming_distance(h1, h3), 10)

        # Test wrapper implementation (hex string)
        hex1 = dhash_vertical(self.img1)
        hex2 = dhash_vertical(self.img2)
        hex3 = dhash_vertical(self.img3)
        self.assertIsInstance(hex1, str)
        self.assertEqual(len(hex1), 16) # 8x8 bits = 64 bits = 16 hex chars

        self.assertLess(hex_hamming_distance(hex1, hex2), 5)
        self.assertGreater(hex_hamming_distance(hex1, hex3), 10)

    def test_marr_hildreth_hash(self):
        # Test core implementation
        h1 = core_marr_hildreth_hash(self.img1)
        h2 = core_marr_hildreth_hash(self.img2)
        h3 = core_marr_hildreth_hash(self.img3)

        self.assertTrue(h1.shape == (8, 8))
        self.assertLess(core_hamming_distance(h1, h2), 5)
        self.assertGreater(core_hamming_distance(h1, h3), 10)

        # Test wrapper implementation
        hex1 = marr_hildreth_hash(self.img1)
        self.assertIsInstance(hex1, str)
        self.assertEqual(len(hex1), 16)

    def test_whash_core(self):
        # Test core implementation (wrapper was tested in verify_env.py and presumably elsewhere)
        h1 = core_whash(self.img1)
        h2 = core_whash(self.img2)
        h3 = core_whash(self.img3)

        self.assertTrue(h1.shape == (8, 8))
        self.assertLess(core_hamming_distance(h1, h2), 5)
        self.assertGreater(core_hamming_distance(h1, h3), 10)

    def test_string_inputs(self):
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            self.img1.save(f, format="PNG")
            temp_path = f.name

        try:
            # Test string input for new/modified algorithms
            h_dv = dhash_vertical(temp_path)
            self.assertIsInstance(h_dv, str)
            self.assertEqual(len(h_dv), 16)

            h_mh = marr_hildreth_hash(temp_path)
            self.assertIsInstance(h_mh, str)
            self.assertEqual(len(h_mh), 16)

            h_w = whash(temp_path)
            self.assertIsInstance(h_w, str)
            self.assertEqual(len(h_w), 16)

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

if __name__ == '__main__':
    unittest.main()
