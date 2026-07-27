import sqlite3

def init_db(caminho="data.db"):
    conn = sqlite3.connect(caminho)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL UNIQUE,
            horas_estudo_tecnologia REAL,
            horas_estudo_teologia REAL,
            foi_academia INTEGER,
            leitura INTEGER
        )
    """)

    conn.commit()
    conn.close()
    print(f"Banco pronto em {caminho}")

if __name__ == "__main__":
    init_db()