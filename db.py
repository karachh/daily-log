import sqlite3

def init_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            horas_estudo_tecnologia REAL,
            horas_estudo_teologia REAL,
            foi_academia INTEGER,
            leitura INTEGER
        )
    """)
    
    conn.commit()
    conn.close()
    print("Banco de dados criado com sucesso.")

if __name__ == "__main__":
    init_db()