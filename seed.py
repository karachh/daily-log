import sqlite3
import random
from datetime import date, timedelta
from db import init_db

CAMINHO = "data_dev.db"
DIAS = 21

random.seed(42)
init_db(CAMINHO)

conexao = sqlite3.connect(CAMINHO)
cursor = conexao.cursor()

DATA_FINAL = date(2026, 7, 27)
registros = []

for i in range(DIAS):
    dia = DATA_FINAL - timedelta(days=i)
    fim_de_semana = dia.weekday() >= 5

    if fim_de_semana:
        tecnologia = round(random.uniform(0, 2), 1)
        teologia = round(random.uniform(0, 1.5), 1)
        academia = 0
    else:
        tecnologia = round(random.uniform(1, 4), 1)
        teologia = round(random.uniform(0, 1), 1)
        academia = random.choice([1, 1, 1, 0])

    leitura = random.choice([1, 0])
    registros.append((dia.isoformat(), tecnologia, teologia, academia, leitura))

cursor.execute("DELETE FROM entries")
cursor.executemany("""
    INSERT OR REPLACE INTO entries (data, horas_estudo_tecnologia, horas_estudo_teologia, foi_academia, leitura)
    VALUES (?, ?, ?, ?, ?)
""", registros)

conexao.commit()

cursor.execute("SELECT COUNT(*) FROM entries")
print(f"{cursor.fetchone()[0]} registros em {CAMINHO}")

conexao.close()