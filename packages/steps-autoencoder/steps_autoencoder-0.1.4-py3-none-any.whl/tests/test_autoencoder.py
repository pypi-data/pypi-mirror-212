import unittest
from steps_autoencoder.models import AutoEncoder

class TestAutoencoder(unittest.TestCase):
    def test_initialization(self):
        autoencoder = AutoEncoder()
        self.assertIsNotNone(autoencoder)

if __name__ == "__main__":
    unittest.main()
