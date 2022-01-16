import json
import sqlalchemy
from sqlalchemy.types import TypeDecorator

SIZE = 200


class DBList(TypeDecorator):
    """
    This class is used to store custom object in a mysql db.
    It is useful to convert a list in a string before the persistence and convert it back to a list when a query is performed
    """
    impl = sqlalchemy.Text(SIZE)

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value
