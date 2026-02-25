import unittest
from PIL import Image
import numpy as np
from image_hashing.algorithms import dhash_vertical, marr_hildreth_hash

class TestAddedAlgorithms(unittest.TestCase):
    def setUp(self):
        # Create a simple image: horizontal stripes
        # Size 100x100
        self.image_stripes = Image.new('RGB', (100, 100), color='black')
        # Stripes
        for y in range(0, 100, 10):
            for x in range(100):
                self.image_stripes.putpixel((x, y), (255, 255, 255))

        # Another image: solid color
        self.image_solid = Image.new('RGB', (100, 100), color='blue')

    def test_dhash_vertical(self):
        h = dhash_vertical(self.image_stripes)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 16) # 8x8 = 64 bits = 16 hex chars

        # Consistent
        h2 = dhash_vertical(self.image_stripes)
        self.assertEqual(h, h2)

        # Different from solid
        h_solid = dhash_vertical(self.image_solid)
        self.assertNotEqual(h, h_solid)

        # Since image has horizontal stripes, vertical gradients exist.
        # So hash should not be 0.
        self.assertNotEqual(h, "0" * 16)

    def test_marr_hildreth_hash(self):
        h = marr_hildreth_hash(self.image_stripes)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 16)

        h2 = marr_hildreth_hash(self.image_stripes)
        self.assertEqual(h, h2)

        h_solid = marr_hildreth_hash(self.image_solid)
        self.assertNotEqual(h, h_solid)

if __name__ == '__main__':
    unittest.main()
