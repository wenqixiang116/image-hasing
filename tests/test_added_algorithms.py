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

        # Another image
        self.image2 = Image.new('RGB', (100, 100), color='blue')

        # Vertically split image
        self.image3 = Image.new('RGB', (100, 100), color='black')
        for x in range(100):
            for y in range(50, 100):
                self.image3.putpixel((x, y), (255, 255, 255))

    def test_dhash_vertical(self):
        h = dhash_vertical(self.image3)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 16) # 8x8 = 64 bits = 16 hex chars

        h2 = dhash_vertical(self.image3)
        self.assertEqual(h, h2)

        # Test diff
        h_blue = dhash_vertical(self.image2)
        self.assertNotEqual(h, h_blue)

    def test_marr_hildreth_hash(self):
        h = marr_hildreth_hash(self.image)
        self.assertIsInstance(h, str)
        self.assertEqual(len(h), 16)

        h2 = marr_hildreth_hash(self.image)
        self.assertEqual(h, h2)

        # Test diff
        h3 = marr_hildreth_hash(self.image2)
        self.assertNotEqual(h, h3)

if __name__ == '__main__':
    unittest.main()
