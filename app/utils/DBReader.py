import psycopg2


class DBReader:
    def lifeCheck(self):
        try:
            self.cursor.execute("Select 1;")
            return [True,"dbreader"]
        except(Exception) as e:
            return [e,"dbreader"]



    def __init__(self, userMS="postgres", hostDB="127.0.0.1", portDB=5432, passwdDB="", databDB="postgres"):
        self.host = hostDB
        self.port = portDB
        self.database = databDB
        self.user = userMS
        self.password = passwdDB

        # Establish the database connection
        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
        self.cursor = self.conn.cursor()

    def read_data(self, query, params=None):
        """
        Executes the given SQL query and returns the result, if applicable.

        :param query: The SQL query to execute.
        :param params: Optional query parameters.
        :return: List of tuples containing the query result (for SELECT), or None for other queries.
        """
        print(query,params)
        self.cursor.execute(query, params)

        # Проверяем, если запрос предполагает возврат данных
        if query.strip().lower().startswith("select"):
            return self.cursor.fetchall()
        else:
            # Если это не SELECT, делаем commit и возвращаем None
            self.conn.commit()
            return None

    def close(self):
        """Closes the cursor and the connection."""
        self.cursor.close()
        self.conn.close()
