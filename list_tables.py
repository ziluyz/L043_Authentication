from app import db, app
from sqlalchemy import inspect

def list_tables():
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print("Tables in the database:")
        for table in tables:
            print(table)

if __name__ == "__main__":
    list_tables()