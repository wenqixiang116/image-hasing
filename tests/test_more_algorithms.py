import unittest
from PIL import Image
from image_hashing import dhash_vertical, marr_hildreth_hash, dhash

class TestMoreAlgorithms(unittest.TestCase):
    def setUp(self):
        # Create a simple image
        self.image = Image.new('RGB', (100, 100), color='white')
        # Add a horizontal line
        for x in range(100):
            self.image.putpixel((x, 50), (0, 0, 0))

        # Add a vertical line
        for y in range(100):
            self.image.putpixel((50, y), (0, 0, 0))

        self.image2 = Image.new('RGB', (100, 100), color='black')

    def test_dhash_vertical(self):
        h = dhash_vertical(self.image)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 16)

        h2 = dhash_vertical(self.image)
        self.assertEqual(h, h2)

        # dhash_vertical should be different from dhash (horizontal) for this image
        # Because the image has both vertical and horizontal features but they are different.
        h_horiz = dhash(self.image)
        self.assertNotEqual(h, h_horiz)

    def test_marr_hildreth_hash(self):
        h = marr_hildreth_hash(self.image)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 16)

        h2 = marr_hildreth_hash(self.image)
        self.assertEqual(h, h2)

        h3 = marr_hildreth_hash(self.image2)
        self.assertNotEqual(h, h3)

if __name__ == '__main__':
    unittest.main()
