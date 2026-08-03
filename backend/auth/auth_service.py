import bcrypt
from backend.database import Database


class AuthService:

    def __init__(self):

        self.db = Database()

    def register(self, username, password):

        hashed = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        )

        try:

            self.db.cursor.execute(

                "INSERT INTO users(username,password) VALUES(?,?)",

                (
                    username,
                    hashed.decode()
                )

            )

            self.db.connection.commit()

            return True

        except:

            return False

    def login(self, username, password):

        self.db.cursor.execute(

            "SELECT password FROM users WHERE username=?",

            (username,)

        )

        user = self.db.cursor.fetchone()

        if user is None:

            return False

        return bcrypt.checkpw(

            password.encode(),

            user[0].encode()

        )