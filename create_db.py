from sqlalchemy import text
from main import db, app

with app.app_context():
    db.create_all()
    with db.engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """))
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT,
            years_employed INTEGER
        )
        """))
        conn.execute(text("INSERT INTO users (username, password) VALUES ('admin', 'test1234');"))
        conn.execute(text("""
            INSERT INTO employees (name, age, email, years_employed) VALUES 
            ("Alice Johnson", 30, "alice.johnson@example.com", 5),
            ("Bob Smith", 28, "bob.smith@example.com", 3),
            ("Charlie Brown", 35, "charlie.brown@example.com", 8),
            ("Diana Prince", 32, "diana.prince@example.com", 4),
            ("Ethan Hunt", 40, "ethan.hunt@example.com", 10),
            ("Fiona Gallagher", 29, "fiona.gallagher@example.com", 2),
            ("George Lucas", 50, "george.lucas@example.com", 15),
            ("Hannah Montana", 27, "hannah.montana@example.com", 1);
        """))
        conn.commit()
