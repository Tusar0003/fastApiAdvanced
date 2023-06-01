from fastapi import Depends
from ..database.sql_helper import SqlHelper
from ..database.database import get_cursor, get_connection


class AuthService(object):

    def __init__(self, connection=Depends(get_connection)):
        self.connection = connection
        self.sql_helper = SqlHelper(connection)

    def get_users(self):
        query = 'SELECT * FROM public.users;'
        result = self.sql_helper.select(query=query)

        return result
