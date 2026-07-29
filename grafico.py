import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

CAMINHO = "data_dev.db"

conexao = sqlite3.connect(CAMINHO)
df = pd.read_sql_query("""
    SELECT data, horas_estudo_tecnologia, horas_estudo_teologia
    FROM entries
    ORDER BY data
""", conexao, parse_dates=["data"])
conexao.close()

fig, ax = plt.subplots(figsize=(12, 5))

ax.bar(df["data"], df["horas_estudo_tecnologia"],
       label="Tecnologia", color="#2b6cb0")

ax.bar(df["data"], df["horas_estudo_teologia"],
       bottom=df["horas_estudo_tecnologia"],
       label="Teologia", color="#dd6b20")

ax.set_title("Horas de estudo por dia")
ax.set_ylabel("Horas")
ax.legend()

fig.autofmt_xdate()
fig.tight_layout()
fig.savefig("estudo_diario.png", dpi=120)

print("Grafico salvo em estudo_diario.png")