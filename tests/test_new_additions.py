import unittest
from PIL import Image
from image_hashing import dhash_vertical, marr_hildreth_hash, dhash

class TestNewAdditions(unittest.TestCase):
    def setUp(self):
        # Create a simple image: black on top, white on bottom
        self.image_vertical = Image.new('RGB', (100, 100), color='black')
        for x in range(100):
            for y in range(50, 100):
                self.image_vertical.putpixel((x, y), (255, 255, 255))

        # Another image: black on left, white on right (horizontal gradient)
        self.image_horizontal = Image.new('RGB', (100, 100), color='black')
        for x in range(50, 100):
            for y in range(100):
                self.image_horizontal.putpixel((x, y), (255, 255, 255))

    def test_dhash_vertical(self):
        h = dhash_vertical(self.image_vertical)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 16) # 8x8 = 64 bits = 16 hex chars

        h2 = dhash_vertical(self.image_vertical)
        self.assertEqual(h, h2)

        # Test diff with horizontal hash
        # dhash (horizontal) should detect horizontal gradients.
        # dhash_vertical should detect vertical gradients.

        h_horiz = dhash(self.image_vertical)
        # Vertical gradient image has no horizontal change (except at edges maybe if resized poorly, but ideally 0)
        # The image is constant along X.
        # So dhash should be all 0s?
        # dhash compares x and x+1. columns are identical. so diff is 0.
        self.assertEqual(h_horiz, "0000000000000000")

        # dhash_vertical on vertical gradient image should detect change.
        # rows 0-49 are black, 50-99 are white.
        # It resizes to 8x9.
        # The transition is in the middle.
        self.assertNotEqual(h, "0000000000000000")

    def test_marr_hildreth_hash(self):
        h = marr_hildreth_hash(self.image_vertical)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 16)

        h2 = marr_hildreth_hash(self.image_vertical)
        self.assertEqual(h, h2)

        # Test diff
        h3 = marr_hildreth_hash(self.image_horizontal)
        self.assertNotEqual(h, h3)

if __name__ == '__main__':
    unittest.main()
