""" Influx wrapper"""
from datetime import datetime
from copy import deepcopy
from influxdb import InfluxDBClient

from .db_conn import DBConn, DBOpenException, DBExceptionNotOpen

class InfluxDBConn(DBConn):
    """ Wrapper over influx API, to make easier to write and read information to/from a influx database
    """
    def __init__(self):
        super().__init__()
        self.conn = None

    def open_conn(self, params, autocommit=True):
        host = params['host']
        user = params['user']
        password = params['password']
        bucket = params['bucket']

        try:
            self.conn = InfluxDBClient(host=host, username=user, password=password, database=bucket)
        except Exception as ex:
            raise DBOpenException(f'Could not open database. \
                                    Host={host}, \
                                    user={user}, \
                                    password={password}, \
                                    bucket={bucket}. \
                                    Error:{ex}') from ex

    def close_conn(self):
        self.conn.close()

    def insert(self, table, rows):
        if not self.conn:
            raise DBExceptionNotOpen('Database not opened')

        points = deepcopy(rows)
        for point in points:
            point["measurement"] = table
            if 'time' not in point or not point['time']:
                point['time'] = datetime.utcnow()

        self.conn.write_points(points)

    def _get_condition_string(self, condition: tuple):
        ret = ''
        if isinstance(condition[0], str):
            ret = f"{condition[0]}='{condition[1]}'"
        elif isinstance(condition[0], int):
            ret = f"{condition[0]}={condition[1]}"
        return ret

    def select(self, table_name: str, tags_conds: tuple, order_by: str = None, order_asc: bool = True, limit: int = 0):
        """ Get db information
        Args:
            table_name (str): Name of the table to be queried
            tags_conds (tuple): Tuple with (fields, value) to filter the query
            order_by (str): Field to order by
            order_asc (bool): If sort order is ASC. DESC if false
            limit (int): Limit the number of queries retrieved
        """
        if self.conn is None:
            raise DBExceptionNotOpen('Database not opened')

        conds_string = ""

        if tags_conds:
            conds_string = " WHERE "

            conds_string += self._get_condition_string(tags_conds[0])

            for cond in tags_conds[1:]:
                conds_string += " AND " + self._get_condition_string(cond)

        query = f"""SELECT * from {table_name} {conds_string}
                ORDER BY {order_by} {'ASC' if order_asc else 'DESC'}
                LIMIT {limit}"""
        result_set = self.conn.query(query)
        points = list(result_set.get_points())

        return points
