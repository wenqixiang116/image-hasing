import unittest
from PIL import Image, ImageDraw
from image_hashing import dhash_vertical, marr_hildreth_hash, hamming_distance

class TestAddedAlgorithms(unittest.TestCase):
    def setUp(self):
        # Create a simple image: black on top, white on bottom
        self.image = Image.new('RGB', (100, 100), color='black')
        d = ImageDraw.Draw(self.image)
        d.rectangle([0, 50, 100, 100], fill='white')

        # Another image
        self.image2 = Image.new('RGB', (100, 100), color='blue')

    def test_dhash_vertical(self):
        h = dhash_vertical(self.image)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 16) # 8x8 = 64 bits = 16 hex chars

        h2 = dhash_vertical(self.image)
        self.assertEqual(h, h2)

        # Test diff
        h3 = dhash_vertical(self.image2)
        self.assertNotEqual(h, h3)

    def test_marr_hildreth_hash(self):
        h = marr_hildreth_hash(self.image)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 16) # 8x8 = 64 bits = 16 hex chars

        h2 = marr_hildreth_hash(self.image)
        self.assertEqual(h, h2)

        # Test diff
        h3 = marr_hildreth_hash(self.image2)
        self.assertNotEqual(h, h3)

    def test_hamming_distance_added(self):
        h1 = dhash_vertical(self.image)
        h2 = dhash_vertical(self.image)
        self.assertEqual(hamming_distance(h1, h2), 0)

        h3 = dhash_vertical(self.image2)
        dist = hamming_distance(h1, h3)
        self.assertGreater(dist, 0)

if __name__ == '__main__':
    unittest.main()
