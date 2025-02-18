import unittest
from datetime import date
from src.data_generator import generate_data

class TestDataGenerator(unittest.TestCase):
    def test_generate_data(self):
        data_config = {
            "Col1": ("Same Value", "Test"),
            "Col2": ("Number Range", 1, 100),
            "Col3": ("Date", date(2023, 1, 1), date(2023, 12, 31))
        }
        df = generate_data(5, data_config)
        self.assertEqual(len(df), 5)
        self.assertEqual(df["Col1"].iloc[0], "Test")
        self.assertTrue(1 <= df["Col2"].iloc[0] <= 100)

if __name__ == '__main__':
    unittest.main()
