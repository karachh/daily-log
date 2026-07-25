import sqlite3
from datetime import date

def add_entry():
    horas_estudo_tecnologia = float(input("Quantas horas você estudou de tecnologia hoje? "))
    horas_estudo_teologia = float(input("Quantas horas você estudou de teologia hoje? "))
    foi_academia = input("Foi na academia hoje? (s/n) ").strip().lower()
    leitura = input("Realizou uma leitura hoje? (s/n)? ").strip().lower()

    foi_academia_int = 1 if foi_academia == "s" else 0
    leitura_int = 1 if leitura == "s" else 0
    hoje = str(date.today())

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO entries (data, horas_estudo_tecnologia, horas_estudo_teologia, foi_academia, leitura)
        VALUES (?, ?, ?, ?, ?)
    """, (hoje, horas_estudo_tecnologia, horas_estudo_teologia, foi_academia_int, leitura_int))

    conn.commit()
    conn.close()
    print(f"Registro de {hoje} salvo com sucesso.")

if __name__ == "__main__":
    add_entry()