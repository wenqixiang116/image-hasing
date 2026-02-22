import unittest
from PIL import Image
import numpy as np
from image_hashing import dhash_vertical, marr_hildreth_hash

class TestAddedAlgorithms(unittest.TestCase):
    def setUp(self):
        # Create a simple image: black on left, white on right (vertical line)
        # Adjacent rows are identical.
        self.image_horizontal_diff = Image.new('RGB', (100, 100), color='black')
        for x in range(50, 100):
            for y in range(100):
                self.image_horizontal_diff.putpixel((x, y), (255, 255, 255))

        # Create an image with vertical variation (horizontal stripes)
        # Black on top, white on bottom.
        # Adjacent columns are identical.
        self.image_vertical_diff = Image.new('RGB', (100, 100), color='black')
        for y in range(50, 100):
            for x in range(100):
                self.image_vertical_diff.putpixel((x, y), (255, 255, 255))

        # Image for consistency test
        self.image = self.image_horizontal_diff

    def test_dhash_vertical(self):
        h = dhash_vertical(self.image_vertical_diff)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 16) # 64 bits = 16 hex chars

        # Should be non-zero for vertical diff image
        self.assertNotEqual(h, "0000000000000000")

        # Test consistency
        h2 = dhash_vertical(self.image_vertical_diff)
        self.assertEqual(h, h2)

        # Test on horizontal diff image (should have little vertical diff)
        # Pure horizontal diff image (vertical lines) has 0 vertical diff
        h_horiz = dhash_vertical(self.image_horizontal_diff)
        self.assertEqual(h_horiz, "0000000000000000")

    def test_marr_hildreth_hash(self):
        h = marr_hildreth_hash(self.image)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 16)

        # Test consistency
        h2 = marr_hildreth_hash(self.image)
        self.assertEqual(h, h2)

        # Test distinctness
        h3 = marr_hildreth_hash(self.image_vertical_diff)
        self.assertNotEqual(h, h3)

if __name__ == '__main__':
    unittest.main()
