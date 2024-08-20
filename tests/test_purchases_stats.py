from io import StringIO
import json
import unittest

# from src.purchase_stats import calculate_statistics, get_purchase_stats
import src.purchases_stats as src_ps

import pandas as pd
import pytest


class TestCLIApp(unittest.TestCase):
    """Class to represent unit testing of the src functions."""

    def setUp(self):
        """Sample data to use in tests."""
        self.sample_data = [
            {
                "brand": "newventure.co",
                "customer_id": "a45f2398-3f57-4d83-84bf-87afc31b483a",
                "items": [
                    {
                        "department": "Tools",
                        "price": "249.00",
                        "product_category": "Sausages",
                        "product_name": "Intelligent Fresh Pizza",
                        "quantity": 1,
                    },
                    {
                        "department": "Health",
                        "price": "366.00",
                        "product_category": "Mouse",
                        "product_name": "Refined Wooden Hat",
                        "quantity": 2,
                    },
                ],
                "purchase_id": "3655582c-4b0c-4db4-9b53-b2e0d06bba8d",
            }
        ]

    def test_calculate_statistics_valid_data(self):
        file_path = "tests/test_data/valid_purchases.json"
        expected_results = {
            "total_volume_of_spend": "$7895.00",
            "average_purchase_value": "$1315.83",
            "maximum_purchase_value": "$2413.00",
            "median_purchase_value": "$1170.50",
            "unique_products_purchased": 12,
        }
        results = src_ps.get_purchase_stats(file_path)

        assert json.loads(results) == expected_results

    def test_calculate_statistics_empty_file(self):
        file_path = "tests/test_data/empty_purchases.json"
        with pytest.raises(ValueError):  # , match="Input JSON file is empty or data is malformed. Expecting value: line 1 column 1 (char 0), None"):
            src_ps.get_purchase_stats(file_path)

    def test_calculate_statistics_invalid_file(self):
        # file_path = "tests/test_data/invalid_purchases.json"
        # with pytest.raises(ValueError):
        # #, match="Input JSON KeyError is empty or malformed. \"Key 'customer_id' not found. To replace missing values of 'customer_id' with np.nan, pass in errors='ignore'\", None"):
        #     src_ps.get_purchase_stats(file_path)
        # with pytest.raises(KeyError):
        # #, match="Input JSON KeyError is empty or malformed. \"Key 'customer_id' not found. To replace missing values of 'customer_id' with np.nan, pass in errors='ignore'\", None"):
        #     src_ps.get_purchase_stats(file_path)
        pass

    def test_convert_data_to_df(self):
        """Test that load_data correctly loads JSON data."""
        # expected_stats = {
        #     "total_volume_of_spend": "$981.00",
        #     "average_purchase_value": "$490.50",
        #     "max_purchase_value": "$732.00",
        #     "median_purchase_value": "$490.50",
        #     "number_of_unique_products": 2.0,
        # }
        # json_data = json.dumps(self.sample_data)
        # stats = src_ps.convert_data_to_df(src_ps.load_data(json_data))
        # self.assertEqual(stats, expected_stats)
        pass

    def test_calculate_statistics(self):
        """Test that calculate_statistics correctly computes the statistics."""
        # expected_stats = {
        #     "total_volume_of_spend": "$981.00",
        #     "average_purchase_value": "$490.50",
        #     "max_purchase_value": "$732.00",
        #     "median_purchase_value": "$490.50",
        #     "number_of_unique_products": 2.0,
        # }
        # df = pd.DataFrame(self.sample_data)
        # stats = src_ps.calculate_statistics(src_ps.transform_df(df))
        # self.assertEqual(stats, expected_stats)
        pass


if __name__ == "__main__":
    unittest.main()
