import unittest
from PIL import Image
from image_hashing import dhash_vertical, marr_hildreth_hash

class TestAddedAlgorithms(unittest.TestCase):
    def setUp(self):
        # Create a simple image: black on left, white on right
        self.image = Image.new('RGB', (100, 100), color='black')
        for x in range(50, 100):
            for y in range(100):
                self.image.putpixel((x, y), (255, 255, 255))

        # Create another image: white on top, black on bottom
        self.image2 = Image.new('RGB', (100, 100), color='white')
        for x in range(100):
            for y in range(50, 100):
                self.image2.putpixel((x, y), (0, 0, 0))

    def test_dhash_vertical(self):
        h1 = dhash_vertical(self.image)
        self.assertIsInstance(h1, str)
        self.assertEqual(len(h1), 16) # 8x8 = 64 bits = 16 hex chars

        h2 = dhash_vertical(self.image)
        self.assertEqual(h1, h2)

        # The two images should produce different hashes
        h3 = dhash_vertical(self.image2)
        self.assertNotEqual(h1, h3)

    def test_marr_hildreth_hash(self):
        h1 = marr_hildreth_hash(self.image)
        self.assertIsInstance(h1, str)
        self.assertEqual(len(h1), 16) # 8x8 = 64 bits = 16 hex chars

        h2 = marr_hildreth_hash(self.image)
        self.assertEqual(h1, h2)

        h3 = marr_hildreth_hash(self.image2)
        self.assertNotEqual(h1, h3)

if __name__ == '__main__':
    unittest.main()
