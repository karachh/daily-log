import sqlite3
import pandas as pd

CAMINHO = "data_dev.db"

conexao = sqlite3.connect(CAMINHO)

df = pd.read_sql_query("""
    SELECT
        data,
        horas_estudo_tecnologia,
        horas_estudo_teologia,
        foi_academia,
        leitura
    FROM entries
    ORDER BY data
""", conexao, parse_dates=["data"])

conexao.close()

dias_esperados = (df["data"].max() - df["data"].min()).days + 1
dias_registrados = len(df)
buracos = dias_esperados - dias_registrados

if buracos > 0:
    print(f"Atenção: {buracos} dia(s) sem registro no período.")
else:
    print("Período completo, sem buracos.")
print()

print(f"Linhas: {len(df)}  |  Periodo: {df['data'].min().date()} a {df['data'].max().date()}")
print()

df["horas_total"] = df["horas_estudo_tecnologia"] + df["horas_estudo_teologia"]

print("--- 5 primeiras linhas ---")
print(df.head())
print()

print("--- Resumo geral ---")
print(f"Horas de tecnologia:  {df['horas_estudo_tecnologia'].sum():.1f}")
print(f"Horas de teologia:    {df['horas_estudo_teologia'].sum():.1f}")
print(f"Media diaria total:   {df['horas_total'].mean():.2f}")
print(f"Dias de academia:     {int(df['foi_academia'].sum())} de {len(df)}")
print(f"Dias com leitura:     {int(df['leitura'].sum())} de {len(df)}")
print()

df["semana"] = df["data"].dt.to_period("W").apply(lambda p: p.start_time.date())

resumo_semanal = df.groupby("semana").agg(
    dias=("data", "count"),
    tecnologia=("horas_estudo_tecnologia", "sum"),
    media_tecnologia=("horas_estudo_tecnologia", "mean"),
    teologia=("horas_estudo_teologia", "sum"),
    media_teologia=("horas_estudo_teologia", "mean"),
    taxa_academia=("foi_academia", "mean"),
).round(2)

print("--- Por semana ---")
print(resumo_semanal)