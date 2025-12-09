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
    def test_read_moisture_higher_than_500(self, moisture_sensor: Mock):
        greenhouse = Greenhouse()
        moisture_sensor.return_value = 501
        self.assertRaises(GreenhouseError, greenhouse.measure_soil_moisture)

    @patch.object(GPIO, "output")
    def test_sprinkler_is_turned_on(self, sprinkler: Mock):
        #variabile di stato -> output diretto
        #assert called -> output indiretto
        greenhouse = Greenhouse()
        greenhouse.sprinkler_on = False
        greenhouse.turn_on_sprinkler()
        self.assertTrue(greenhouse.sprinkler_on)
        sprinkler.assert_called_once_with(greenhouse.SPRINKLER_PIN, True)

    @patch.object(GPIO, "output")
    def test_sprinkler_is_turned_off(self, sprinkler: Mock):
        greenhouse = Greenhouse()
        greenhouse.sprinkler_on = True
        greenhouse.turn_off_sprinkler()
        self.assertFalse(greenhouse.sprinkler_on)
        sprinkler.assert_called_once_with(greenhouse.SPRINKLER_PIN, False)

    @patch.object(GPIO, "output")
    @patch.object(Seesaw, "moisture_read")
    def test_sprinkler_is_turned_on_when_moisture_level_is_lower_than_375(self, moisture_sensor: Mock, sprinkler: Mock):
        greenhouse = Greenhouse()
        moisture_sensor.return_value = 374
        greenhouse.sprinkler_on = False
        greenhouse.manage_sprinkler()
        self.assertTrue(greenhouse.sprinkler_on)
        sprinkler.assert_called_once_with(greenhouse.SPRINKLER_PIN, True)

    @patch.object(GPIO, "output")
    @patch.object(Seesaw, "moisture_read")
    def test_sprinkler_is_turned_off_when_moisture_level_is_higher_than_425(self, moisture_sensor: Mock, sprinkler: Mock):
        greenhouse = Greenhouse()
        moisture_sensor.return_value = 426
        greenhouse.sprinkler_on = True
        greenhouse.manage_sprinkler()
        self.assertFalse(greenhouse.sprinkler_on)
        sprinkler.assert_called_once_with(greenhouse.SPRINKLER_PIN, False)

    @patch.object(GPIO, "output")
    @patch.object(Seesaw, "moisture_read")
    def test_sprinkler_remains_off_when_it_was_off_and_moisture_level_is_in_range_375_425(self, moisture_sensor: Mock, sprinkler: Mock):
        greenhouse = Greenhouse()
        moisture_sensor.return_value = 375
        greenhouse.sprinkler_on = False
        greenhouse.manage_sprinkler()
        self.assertFalse(greenhouse.sprinkler_on)
        sprinkler.assert_called_once_with(greenhouse.SPRINKLER_PIN, False)

