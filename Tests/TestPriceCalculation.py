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
            price_query.validate_date("2019-13-30")
        with self.assertRaises(ValidationError):
            price_query.validate_date("2018-12-15")
        with self.assertRaises(ValidationError):
            price_query.validate_date("2023-02-30")
        with self.assertRaises(ValidationError):
            price_query.validate_date("AAAA-BB-CC")
        with self.assertRaises(ValidationError):
            price_query.validate_date("13FEBRUARY2023")

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
            price_query.validate_time("ABC")
        with self.assertRaises(ValidationError):
            price_query.validate_time("00:000")
        with self.assertRaises(ValidationError):
            price_query.validate_time("AB:CD")
        with self.assertRaises(ValidationError):
            price_query.validate_time("00:7A")
        with self.assertRaises(ValidationError):
            price_query.validate_time("67:68")
        with self.assertRaises(ValidationError):
            price_query.validate_time("DREIZEHNUHRDREI")
        with self.assertRaises(ValidationError):
            price_query.validate_time("-4:-4")
        with self.assertRaises(ValidationError):
            price_query.validate_time("-4:00")
        with self.assertRaises(ValidationError):
            price_query.validate_time("22:-2")

        # Assert that the function returns None for valid dates
        self.assertIsNone(price_query.validate_time("12:33"))

    # Test the convert_to_block function
    def test_convert_to_block(self):
        # Assert that the function returns the expected results
        self.assertEqual(convert_to_block("00:00"), "0000-0559")
        self.assertEqual(convert_to_block("06:05"), "0600-0659")
        self.assertEqual(convert_to_block("06:25"), "0600-0659")
        self.assertEqual(convert_to_block("12:15"), "1200-1259")
        self.assertEqual(convert_to_block("12:05"), "1200-1259")
        self.assertEqual(convert_to_block("23:59"), "2300-2359")

    # Test the date validation
    def test_validate_location_origin(self):
        # Create a PriceQuery instance
        price_query = PriceQuery()

        # Assert that the function raises a ValidationError for invalid dates
        with self.assertRaises(ValidationError):
            price_query.validate_location_origin("Boston")
        with self.assertRaises(ValidationError):
            price_query.validate_location_origin("9E")

        # Assert that the function returns None for valid dates
        self.assertIsNone(price_query.validate_location_origin("JFK"))

    # Test the date validation
    def test_validate_location_dest(self):
        # Create a PriceQuery instance
        price_query = PriceQuery()

        # Assert that the function raises a ValidationError for invalid dates
        with self.assertRaises(ValidationError):
            price_query.validate_location_dest("Boston")
        with self.assertRaises(ValidationError):
            price_query.validate_location_dest("9E")

        # Assert that the function returns None for valid dates
        self.assertIsNone(price_query.validate_location_dest("JFK"))

    # Test the date validation
    def test_validate_carrier(self):
        # Create a PriceQuery instance
        price_query = PriceQuery()

        # Assert that the function raises a ValidationError for invalid dates
        with self.assertRaises(ValidationError):
            price_query.validate_carrier("Deutsche Bahn")
        with self.assertRaises(ValidationError):
            price_query.validate_carrier("GNV")
        with self.assertRaises(ValidationError):
            price_query.validate_carrier("AB")
        with self.assertRaises(ValidationError):
            price_query.validate_carrier("Endeavor Air")

        # Assert that the function returns None for valid dates
        self.assertIsNone(price_query.validate_carrier("9E"))

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
                get_distance('jfk', 'atl')
            with self.assertRaises(ValidationError):
                get_distance('ABC', 'DEF')

    # Use Python's built-in patch decorator from the unittest.mock library
    # to replace certain functions (joblib.load, app.get_distance, app.get_day_of_month_and_week, app.convert_to_block)
    # with mock objects during the test.
    @patch('joblib.load')
    @patch('app.get_distance')
    @patch('app.get_day_of_month_and_week')
    @patch('app.convert_to_block')
    # Define the test case function, the mock objects are automatically passed as arguments.
    def test_price_calculation(self, mock_convert_to_block, mock_get_day_of_month_and_week, mock_get_distance,
                               mock_load):
        # Set return values for the mocked functions
        # When app.get_day_of_month_and_week() is called, it will return (15, 2)
        mock_get_day_of_month_and_week.return_value = (15, 2)
        # When app.convert_to_block() is called, it will return '1500-1559'
        mock_convert_to_block.return_value = '1500-1559'
        # When app.get_distance() is called, it will return 500
        mock_get_distance.return_value = 500

        # Call the function under test with specific parameters and store the result
        result = price_calculation('2023-08-15', 'ATL', 'GNV', '15:00', '9E')

        # Assert that the function returns a dictionary (result must be a dict)
        self.assertIsInstance(result, dict)
        # Assert that the dictionary contains a 'price' key
        self.assertIn('price', result)
        # Assert that the value associated with the 'price' key is a number (either an integer or a floating point
        # number)
        self.assertIsInstance(result['price'], (int, float))


# This line allows the script to be run as a standalone program, executing the tests
if __name__ == "__main__":
    unittest.main()
