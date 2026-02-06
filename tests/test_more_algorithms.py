import unittest
from PIL import Image
import numpy as np
from image_hashing import dhash, dhash_vertical, crop_resistant_hash, hamming_distance

class TestMoreAlgorithms(unittest.TestCase):
    def setUp(self):
        # Create a simple image: vertical stripes
        self.image_stripes = Image.new('RGB', (100, 100), color='black')
        for x in range(0, 100, 10):
            for y in range(100):
                self.image_stripes.putpixel((x, y), (255, 255, 255))

        # Create an image with two distinct blobs
        self.image_blobs = Image.new('RGB', (300, 300), color='black')
        # Blob 1
        for x in range(50, 100):
            for y in range(50, 100):
                self.image_blobs.putpixel((x, y), (255, 255, 255))
        # Blob 2
        for x in range(200, 250):
            for y in range(200, 250):
                self.image_blobs.putpixel((x, y), (255, 255, 255))

    def test_dhash_vertical(self):
        h = dhash_vertical(self.image_stripes)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 16)

        # dhash_vertical on horizontal stripes
        image_h_stripes = Image.new('RGB', (100, 100), color='black')
        for y in range(0, 100, 10):
            for x in range(100):
                image_h_stripes.putpixel((x, y), (255, 255, 255))

        h_vertical = dhash_vertical(image_h_stripes)
        h_horizontal = dhash(image_h_stripes)

        # They should be different
        self.assertNotEqual(h_vertical, h_horizontal)

    def test_crop_resistant_hash(self):
        # We use a smaller min_segment_size to ensure our blobs are picked up
        # Blobs are 50x50 = 2500 pixels. min_segment_size default is 500. So it should be fine.
        hashes = crop_resistant_hash(self.image_blobs, min_segment_size=500, segmentation_image_size=300)
        self.assertIsInstance(hashes, list)
        self.assertTrue(len(hashes) >= 1) # Should have at least the full image hash

        # Since we have blobs, we expect segments found.
        self.assertTrue(len(hashes) > 1, f"Expected more than 1 hash, got {len(hashes)}")

        # Check elements are strings
        for h in hashes:
            self.assertIsInstance(h, str)
            self.assertEqual(len(h), 16)

if __name__ == '__main__':
    unittest.main()
