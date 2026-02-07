import unittest
import os
from PIL import Image
from image_hashing import average_hash, dhash, dhash_vertical, phash, whash, colorhash, crop_resistant_hash

class TestStringInputs(unittest.TestCase):
    def setUp(self):
        # Create a temporary image file
        self.filename = 'test_image_temp.png'
        self.image = Image.new('RGB', (50, 50), color='red')
        self.image.save(self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_string_inputs(self):
        # Test all algorithms with string input
        h_avg = average_hash(self.filename)
        self.assertIsInstance(h_avg, str)

        h_dhash = dhash(self.filename)
        self.assertIsInstance(h_dhash, str)

        h_dhash_v = dhash_vertical(self.filename)
        self.assertIsInstance(h_dhash_v, str)

        h_phash = phash(self.filename)
        self.assertIsInstance(h_phash, str)

        h_whash = whash(self.filename)
        self.assertIsInstance(h_whash, str)

        h_color = colorhash(self.filename)
        self.assertIsInstance(h_color, str)

        h_crop = crop_resistant_hash(self.filename)
        self.assertIsInstance(h_crop, list)
        self.assertIsInstance(h_crop[0], str)

if __name__ == '__main__':
    unittest.main()
