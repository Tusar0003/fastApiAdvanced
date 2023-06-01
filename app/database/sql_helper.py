from psycopg2.extras import execute_values
from psycopg2.extensions import cursor as main_cursor
from sqlalchemy.pool.base import _ConnectionFairy
from contextlib import closing
from ..utils.responses import Responses
from ..utils.strings import Strings
from ..utils.decorators import method_handler
from fastapi import Depends
from ..database.database import get_cursor, get_connection, get_engine


class SqlHelper(object):

    def __init__(self, connection):
        # self.cursor = cursor
        self.connection = connection

    # def __del__(self):
    #     cursor.close()

    @method_handler
    def execute(self, query, values=None):
        with closing(self.connection.cursor()) as cursor:
            if values is None:
                cursor.execute(query, )
            else:
                cursor.execute(query, values)

            self.connection.commit()
            return Responses.success_response()

    @method_handler
    def insert(self, query, values=None):
        with closing(self.connection.cursor()) as cursor:
            if values is None:
                cursor.execute(query, )
            else:
                cursor.execute(query, values)
            self.connection.commit()

            if cursor.rowcount == 1:
                return Responses.success_response()
            else:
                return Responses.error_response(
                    message=Strings.INSERTION_FAILED
                )

    @method_handler
    def bulk_insert(self, query, values):
        with closing(self.connection.cursor()) as cursor:
            execute_values(cursor, query, values)
            self.connection.commit()

            if cursor.rowcount > 0:
                return Responses.success_response()
            else:
                return Responses.error_response(
                    message=Strings.INSERTION_FAILED
                )

    @method_handler
    def insert_with_id(self, query, values=None):
        with closing(self.connection.cursor()) as cursor:
            if values is None:
                cursor.execute(query, )
            else:
                cursor.execute(query, values)
            return_id = cursor.fetchone()

            if cursor.rowcount == 1:
                return Responses.success_response(data=return_id)
            else:
                return Responses.error_response(
                    message=Strings.INSERTION_FAILED
                )

    @method_handler
    def update(self, query, values):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query, values)
            self.connection.commit()

            if cursor.rowcount > 0:
                cursor.close()
                return Responses.success_response()
            else:
                cursor.close()
                return Responses.error_response(
                    message=Strings.UPDATE_FAILED
                )

    @method_handler
    def select(self, query, values=None):
        with closing(self.connection.cursor()) as cursor:
            if values is None:
                cursor.execute(query,)
            else:
                cursor.execute(query, values)
            result = cursor.fetchall()

            row_headers = [col[0] for col in cursor.description]
            data = [dict(zip(row_headers, row)) for row in result]

            if len(data) > 0:
                return Responses.success_response(
                    data=data
                )
            else:
                return Responses.error_response(
                    message=Strings.NO_DATA_FOUND
                )

    @method_handler
    def delete(self, query, values):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query, values)
            self.connection.commit()

            if cursor.rowcount > 0:
                return Responses.success_response(message='Deleted successfully.')
            else:
                return Responses.error_response(
                    message=Strings.DELETE_FAILED
                )

    @method_handler
    def delete_all(self, query):
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(query, )
            self.connection.commit()
            return Responses.success_response()
