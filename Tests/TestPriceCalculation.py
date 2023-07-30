# Import the necessary modules
import unittest
from app import convert_to_block, PriceQuery, price_calculation, get_day_of_month_and_week, get_distance
from marshmallow import ValidationError
from unittest.mock import patch, Mock


# Create a test class that inherits from unittest.TestCase
class TestPriceCalculation(unittest.TestCase):
    # Test the date validation
    def test_date_validation(self):
        # Create a PriceQuery instance
        price_query = PriceQuery()

        # Assert that the function raises a ValidationError for invalid dates
        with self.assertRaises(ValidationError):
            price_query.validate_date("2023-15-08")
        with self.assertRaises(ValidationError):
            price_query.validate_date("2019-13-30")
        with self.assertRaises(ValidationError):
            price_query.validate_date("2018-12-15")
        with self.assertRaises(ValidationError):
            price_query.validate_date("2023-02-30")
        with self.assertRaises(ValidationError):
            price_query.validate_date("AAAA-BB-CC")

        # Assert that the function returns None for valid dates
        self.assertIsNone(price_query.validate_date("2023-12-15"))

    # Test the get_day_of_month_and_week function
    def test_get_day_of_month_and_week(self):
        # Assert that the function returns the expected result
        self.assertEqual(get_day_of_month_and_week("2023-08-15"), (15, 2))
        self.assertEqual(get_day_of_month_and_week("2023-02-28"), (28, 2))
        self.assertEqual(get_day_of_month_and_week("2023-07-30"), (30, 7))
        self.assertEqual(get_day_of_month_and_week("2023-07-31"), (31, 1))

    # Test the date validation
    def test_time_validation(self):
        # Create a PriceQuery instance
        price_query = PriceQuery()

        # Assert that the function raises a ValidationError for invalid dates
        with self.assertRaises(ValidationError):
            price_query.validate_date("2023-15-08")
        with self.assertRaises(ValidationError):
            price_query.validate_date("2019-13-30")
        with self.assertRaises(ValidationError):
            price_query.validate_date("2018-12-15")
        with self.assertRaises(ValidationError):
            price_query.validate_date("2023-02-30")
        with self.assertRaises(ValidationError):
            price_query.validate_date("AAAA-BB-CC")

        # Assert that the function returns None for valid dates
        self.assertIsNone(price_query.validate_date("2023-12-15"))

    # Test the convert_to_block function
    def test_convert_to_block(self):
        # Assert that the function returns the expected results
        self.assertEqual(convert_to_block("00:00"), "0000-0559")
        self.assertEqual(convert_to_block("12:15"), "1200-1259")
        self.assertEqual(convert_to_block("23:59"), "2300-2359")

    # Test the date validation
    def test_validate_location_origin(self):
        # Create a PriceQuery instance
        price_query = PriceQuery()

        # Assert that the function raises a ValidationError for invalid dates
        with self.assertRaises(ValidationError):
            price_query.validate_date("2023-15-08")
        with self.assertRaises(ValidationError):
            price_query.validate_date("2019-13-30")
        with self.assertRaises(ValidationError):
            price_query.validate_date("2018-12-15")
        with self.assertRaises(ValidationError):
            price_query.validate_date("2023-02-30")
        with self.assertRaises(ValidationError):
            price_query.validate_date("AAAA-BB-CC")

        # Assert that the function returns None for valid dates
        self.assertIsNone(price_query.validate_date("2023-12-15"))

    # Test the date validation
    def test_validate_location_dest(self):
        # Create a PriceQuery instance
        price_query = PriceQuery()

        # Assert that the function raises a ValidationError for invalid dates
        with self.assertRaises(ValidationError):
            price_query.validate_date("2023-15-08")
        with self.assertRaises(ValidationError):
            price_query.validate_date("2019-13-30")
        with self.assertRaises(ValidationError):
            price_query.validate_date("2018-12-15")
        with self.assertRaises(ValidationError):
            price_query.validate_date("2023-02-30")
        with self.assertRaises(ValidationError):
            price_query.validate_date("AAAA-BB-CC")

        # Assert that the function returns None for valid dates
        self.assertIsNone(price_query.validate_date("2023-12-15"))

    # Test the date validation
    def test_validate_carrier(self):
        # Create a PriceQuery instance
        price_query = PriceQuery()

        # Assert that the function raises a ValidationError for invalid dates
        with self.assertRaises(ValidationError):
            price_query.validate_date("2023-15-08")
        with self.assertRaises(ValidationError):
            price_query.validate_date("2019-13-30")
        with self.assertRaises(ValidationError):
            price_query.validate_date("2018-12-15")
        with self.assertRaises(ValidationError):
            price_query.validate_date("2023-02-30")
        with self.assertRaises(ValidationError):
            price_query.validate_date("AAAA-BB-CC")

        # Assert that the function returns None for valid dates
        self.assertIsNone(price_query.validate_date("2023-12-15"))

    # Test the get_distance function
    def test_get_distance(self):
        # Use the patch function to mock sqlite3.connect
        with patch('sqlite3.connect') as mock_connect:
            # Mock for valid airport codes
            mock_connect.return_value = Mock()
            mock_connect.return_value.cursor.return_value = Mock()
            mock_connect.return_value.cursor.return_value.fetchone.return_value = (422,)
            # Assert that the function returns the expected result
            self.assertEqual(get_distance('ATL', 'GNV'), 422)

            # Mock for invalid airport codes
            mock_connect.return_value.cursor.return_value.fetchone.return_value = None
            # Assert that the function raises a ValidationError
            with self.assertRaises(ValidationError):
                get_distance('ABC', 'DEF')

    # Use the patch decorator to mock certain functions that are called within the function being tested
    @patch('joblib.load')
    @patch('app.get_distance')
    @patch('app.get_day_of_month_and_week')
    @patch('app.convert_to_block')
    def test_price_calculation(self, mock_convert_to_block, mock_get_day_of_month_and_week, mock_get_distance,
                               mock_load):
        # Set return values for the mocked functions
        mock_get_day_of_month_and_week.return_value = (15, 3)
        mock_convert_to_block.return_value = '1500-1559'
        mock_get_distance.return_value = 500

        # Assert that the function returns the expected result
        self.assertEqual(price_calculation('2023-08-15', 'ATL', 'GNV', '15:00', '9E'), {'price': 18.79})


# This line allows the script to be run as a standalone program, executing the tests
if __name__ == "__main__":
    unittest.main()
