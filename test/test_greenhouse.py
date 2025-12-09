from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock

from mock import GPIO
from mock.seesaw import Seesaw
from src.greenhouse import Greenhouse, GreenhouseError


class TestGreenhouse(TestCase):

    @patch.object(Seesaw, "moisture_read")
    def test_read_moisture_range_300_500(self, moisture_sensor: Mock):
        greenhouse = Greenhouse()
        moisture_sensor.return_value = 300
        moisture_level = greenhouse.measure_soil_moisture()
        self.assertEqual(moisture_level, 300)

    @patch.object(Seesaw, "moisture_read")
    def test_read_moisture_lower_than_300(self, moisture_sensor: Mock):
        greenhouse = Greenhouse()
        moisture_sensor.return_value = 250
        self.assertRaises(GreenhouseError, greenhouse.measure_soil_moisture)

    @patch.object(Seesaw, "moisture_read")
    def test_read_moisture_greater_than_500(self, moisture_sensor: Mock):
        greenhouse = Greenhouse()
        moisture_sensor.return_value = 501
        self.assertRaises(GreenhouseError, greenhouse.measure_soil_moisture)


