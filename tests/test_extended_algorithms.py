import unittest
from PIL import Image, ImageDraw
import numpy as np
from image_hashing import dhash, dhash_vertical, crop_resistant_hash

class TestExtendedAlgorithms(unittest.TestCase):
    def setUp(self):
        # Create a simple image: vertical stripes
        self.image = Image.new('RGB', (100, 100), color='black')
        for x in range(50, 100):
            for y in range(100):
                self.image.putpixel((x, y), (255, 255, 255))

        # Create an image for crop resistant hash
        # Two white circles on black background
        self.crop_image = Image.new('RGB', (300, 300), color='black')
        draw = ImageDraw.Draw(self.crop_image)
        draw.ellipse((50, 50, 100, 100), fill='white')
        draw.ellipse((200, 200, 250, 250), fill='white')

    def test_dhash_vertical(self):
        h = dhash_vertical(self.image)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 16)

        # Vertical stripes:
        # Left half black, Right half white.
        # Vertical difference should be zero everywhere.
        # So hash should be all zeros.
        self.assertEqual(h, "0000000000000000")

        # dhash (horizontal) should show difference at x=50.
        h_horiz = dhash(self.image)
        # Verify they are different
        self.assertNotEqual(h, h_horiz)

        # Create horizontal stripes image
        h_stripe_img = Image.new('RGB', (100, 100), color='black')
        for y in range(50, 100):
            for x in range(100):
                h_stripe_img.putpixel((x, y), (255, 255, 255))

        h_vert = dhash_vertical(h_stripe_img)
        # Should be non-zero
        self.assertNotEqual(h_vert, "0000000000000000")

    def test_crop_resistant_hash(self):
        # Use min_segment_size=10 to ensure small circles are caught
        hashes = crop_resistant_hash(self.crop_image, min_segment_size=10, segmentation_image_size=300)
        self.assertIsInstance(hashes, list)
        # Should detect 2 circles
        self.assertTrue(len(hashes) >= 2, f"Expected at least 2 hashes, got {len(hashes)}")

        for h in hashes:
            self.assertIsInstance(h, str)
            self.assertEqual(len(h), 16)

    def test_crop_resistant_hash_single(self):
        # Single object
        single_image = Image.new('RGB', (100, 100), color='black')
        draw = ImageDraw.Draw(single_image)
        draw.rectangle((20, 20, 80, 80), fill='white')

        hashes = crop_resistant_hash(single_image, min_segment_size=10, segmentation_image_size=100)
        self.assertEqual(len(hashes), 1)

if __name__ == '__main__':
    unittest.main()
