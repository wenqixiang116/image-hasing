import unittest
from PIL import Image
from image_hashing import whash, colorhash, dhash_vertical, marr_hildreth_hash

class TestNewAlgorithms(unittest.TestCase):
    def setUp(self):
        # Create a simple image: black on left, white on right
        self.image = Image.new('RGB', (100, 100), color='black')
        for x in range(50, 100):
            for y in range(100):
                self.image.putpixel((x, y), (255, 255, 255))

        # Create a vertically split image for testing dhash_vertical
        self.image_vert = Image.new('RGB', (100, 100), color='white')
        for x in range(100):
            for y in range(50, 100):
                self.image_vert.putpixel((x, y), (0, 0, 0))

        # Another image
        self.image2 = Image.new('RGB', (100, 100), color='blue')

    def test_whash(self):
        h = whash(self.image)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 16) # 8x8 = 64 bits = 16 hex chars

        h2 = whash(self.image)
        self.assertEqual(h, h2)

        # Test diff
        h3 = whash(self.image2)
        self.assertNotEqual(h, h3)

    def test_colorhash(self):
        h = colorhash(self.image)
        self.assertIsInstance(h, str)
        # 3 bands * 16 chars = 48 chars
        self.assertEqual(len(h), 48)

        h2 = colorhash(self.image)
        self.assertEqual(h, h2)

        # Test diff
        h3 = colorhash(self.image2)
        self.assertNotEqual(h, h3)

    def test_dhash_vertical(self):
        h = dhash_vertical(self.image_vert)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 16) # 8x8 = 64 bits = 16 hex chars

        # Ensure the hash isn't all zeros
        self.assertNotEqual(h, "0000000000000000")

        h2 = dhash_vertical(self.image_vert)
        self.assertEqual(h, h2)

        # Test diff
        h3 = dhash_vertical(self.image2)
        self.assertNotEqual(h, h3)

    def test_marr_hildreth_hash(self):
        h = marr_hildreth_hash(self.image)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 64) # 16x16 = 256 bits = 64 hex chars

        h2 = marr_hildreth_hash(self.image)
        self.assertEqual(h, h2)

        # Test diff
        h3 = marr_hildreth_hash(self.image2)
        self.assertNotEqual(h, h3)

if __name__ == '__main__':
    unittest.main()
