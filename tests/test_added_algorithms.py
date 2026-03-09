import unittest
from PIL import Image
from image_hashing import dhash_vertical, marr_hildreth_hash

class TestAddedAlgorithms(unittest.TestCase):
    def setUp(self):
        # Create an image that's split vertically: black on top, white on bottom
        self.vertical_image = Image.new('RGB', (100, 100), color='black')
        for x in range(100):
            for y in range(50, 100):
                self.vertical_image.putpixel((x, y), (255, 255, 255))

        # Create an image that's split horizontally: black on left, white on right
        self.horizontal_image = Image.new('RGB', (100, 100), color='black')
        for x in range(50, 100):
            for y in range(100):
                self.horizontal_image.putpixel((x, y), (255, 255, 255))

    def test_dhash_vertical(self):
        h = dhash_vertical(self.vertical_image)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 16) # 8x8 = 64 bits = 16 hex chars

        h2 = dhash_vertical(self.vertical_image)
        self.assertEqual(h, h2)

        # Test diff - vertical and horizontal split images should have different dhash_vertical
        h3 = dhash_vertical(self.horizontal_image)
        self.assertNotEqual(h, h3)

    def test_marr_hildreth_hash(self):
        h = marr_hildreth_hash(self.horizontal_image)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 16) # 8x8 = 64 bits = 16 hex chars

        h2 = marr_hildreth_hash(self.horizontal_image)
        self.assertEqual(h, h2)

        # Test diff
        h3 = marr_hildreth_hash(self.vertical_image)
        self.assertNotEqual(h, h3)

if __name__ == '__main__':
    unittest.main()
