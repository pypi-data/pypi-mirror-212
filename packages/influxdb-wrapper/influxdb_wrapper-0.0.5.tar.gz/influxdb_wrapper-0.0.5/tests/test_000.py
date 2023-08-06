""" unittesting """
import unittest

from influxdb_wrapper import influxdb_factory


class Testing(unittest.TestCase):
    """ Unittesting
    """
    db = influxdb_factory(db_type='mock')
    db.open_conn(None)

    def test_insert(self):
        """ Test insert
        """
        points = [
                    {"tags": {"sensorid": 0}, "fields": {"temp": 20.0, "humidity": 50.0}},
                    {"tags": {"sensorid": 0}, "fields": {"temp": 21.0, "humidity": 50.1}},
                    {"tags": {"sensorid": 1}, "fields": {"temp": 10.0, "humidity": 100.0}}
                 ]
        self.db.insert('DHT22', points)

    def test_select(self):
        """ Test select
        """
        points = self.db. select('DHT22', [('sensorid', 0)], order_by='time', order_asc=False, limit=1)
        self.assertEqual(len(points), 1)


if __name__ == '__main__':
    unittest.main()
