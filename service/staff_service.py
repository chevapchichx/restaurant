from sqlalchemy import create_engine, text
import bcrypt


engine = create_engine('mysql+mysqlconnector://root:root@localhost:8889/restaurant')

def get_auth_waiter(login, password):
    with engine.connect() as conn:
        query = text("SELECT login, password, post, first_name, last_name FROM staff WHERE login = :login")
        result = conn.execute(query, {"login": login})
        auth_info = result.fetchone()
        
        if auth_info is None:
            return None
        
        hashed_password = auth_info[1]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return auth_info
        else:
            return None
