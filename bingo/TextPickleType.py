import json
import sqlalchemy
from sqlalchemy.types import TypeDecorator
import numpy as np

SIZE = 400


class TextPickleType(TypeDecorator):

    impl = sqlalchemy.Text(SIZE)

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value.tolist())
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = np.array(json.loads(value))
        return value
