"""
Boiler plate taken from open source github.
"""

# sqlite db communication
import sqlite3

# Very basic SQLite wrapper
#
# Creates table from schema
# Provides small set of utility functions to query the database
#
#


class db_table:
    # SQLite database filename
    DB_NAME = "restaurant-menu-comparision.db"

    def __init__(self, name, schema):
        # error handling
        if not name:
            raise RuntimeError("invalid table name")
        if not schema:
            raise RuntimeError("invalid database schema")

        # init fields and initiate database connection
        self.name = name
        self.schema = schema
        self.db_conn = sqlite3.connect(self.DB_NAME)

        # ensure the table is created
        self.create_table()

    def create_table(self):
        columns_query_string = ', '.join(
            ["%s %s" % (k, v) for k, v in self.schema.items()])

        # CREATE TABLE IF NOT EXISTS users (id integer PRIMARY KEY, name text)
        self.db_conn.execute("CREATE TABLE IF NOT EXISTS %s (%s)" %
                             (self.name, columns_query_string))
        self.db_conn.commit()

    def select(self, columns=[], where={}, like={}):
        # by default, query all columns
        if not columns:
            columns = [k for k in self.schema]

        # build query string
        columns_query_string = ", ".join(columns)
        query = "SELECT %s FROM %s" % (columns_query_string, self.name)

        # build where query string
        if where:
            where_query_string = ["%s = '%s'" %
                                  (k, v) for k, v in where.items()]
            query += " WHERE " + ' AND '.join(where_query_string)

        # build like query string, make substring search with irrespective of case
        if like:
            like_query_string = ["%s LIKE '%%%s%%'" %
                                 (k, v) for k, v in like.items()]
            if where:
                query += " AND " + ' AND '.join(like_query_string)
            else:
                query += " WHERE " + ' AND '.join(like_query_string)

        result = []
        # SELECT id, name FROM users [ WHERE id=42 AND name=John ]
        for row in self.db_conn.execute(query):
            result_row = {}
            # convert from (val1, val2, val3) to { col1: val1, col2: val2, col3: val3 }
            for i in range(0, len(columns)):
                result_row[columns[i]] = row[i]
            result.append(result_row)

        return result

    def insert(self, item):
        # build columns & values queries
        columns_query = ", ".join(item.keys())
        values_query = ", ".join(["'%s'" % v for v in item.values()])

        # INSERT INTO users(id, name) values (42, John)
        cursor = self.db_conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO %s(%s) values (%s)" %
                       (self.name, columns_query, values_query))
        cursor.close()
        self.db_conn.commit()
        return cursor.lastrowid

    def update(self, values, where):
        # build set & where queries
        set_query = ", ".join(["%s = '%s'" % (k, v)
                              for k, v in values.items()])
        where_query = " AND ".join(["%s = '%s'" % (k, v)
                                   for k, v in where.items()])

        # UPDATE users SET name = Simon WHERE id = 42
        cursor = self.db_conn.cursor()
        cursor.execute("UPDATE %s SET %s WHERE %s" %
                       (self.name, set_query, where_query))
        cursor.close()
        self.db_conn.commit()
        return cursor.rowcount

    # Close the database connection
    #

    def close(self):
        self.db_conn.close()
