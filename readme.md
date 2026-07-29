# Daily Log

Registro diário de hábitos de estudo, treino e leitura. Um script coleta os dados
via terminal, um banco SQLite guarda o histórico, e a análise agrega em resumo
semanal com pandas — mais um gráfico de barras empilhadas.

## Arquitetura

```
terminal (input)  →  log_entry.py  →  SQLite       →  analyze.py   →  console
                     coleta +          entries         agrega +
                     converte tipos                    valida         grafico.py
                                                                      → PNG

seed.py  →  data_dev.db   (dados sintéticos para desenvolvimento)
```

Dois bancos separados: `data.db` guarda os registros reais e `data_dev.db` guarda
21 dias sintéticos. A análise é desenvolvida contra o banco de desenvolvimento,
onde existe volume suficiente para os agrupamentos semanais fazerem sentido, e
depois apontada para o banco real. Os dados reais nunca são tocados por script
de teste.

## Stack

- Python 3 (`pandas`, `matplotlib`)
- SQLite (biblioteca padrão `sqlite3`)
- Git para versionamento

## Como rodar

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

python db.py          # cria o banco e a tabela
python log_entry.py   # registra o dia de hoje
python seed.py        # popula data_dev.db com 21 dias sintéticos
python analyze.py     # valida e agrega
python grafico.py     # gera estudo_diario.png
```

## Modelo de dados

**`entries`** — um registro por dia

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | INTEGER (PK) | Identificador autoincremental |
| `data` | TEXT (UNIQUE) | Data em formato ISO (`AAAA-MM-DD`) |
| `horas_estudo_tecnologia` | REAL | Horas de estudo em tecnologia |
| `horas_estudo_teologia` | REAL | Horas de estudo em teologia |
| `foi_academia` | INTEGER | 0 ou 1 |
| `leitura` | INTEGER | 0 ou 1 |

## Decisões técnicas

**Idempotência.** A coluna `data` tem restrição `UNIQUE` e a carga usa
`INSERT OR REPLACE`. Rodar `log_entry.py` duas vezes no mesmo dia sobrescreve o
registro em vez de duplicar — sem isso, um duplo registro inflaria a média de
horas em silêncio, sem erro nenhum. O `seed.py` usa a mesma garantia por outro
caminho: `DELETE` + `INSERT` (*full refresh*), que reconstrói a tabela inteira a
cada execução.

**Datas em ISO.** Guardadas como `AAAA-MM-DD`, formato em que ordenação
alfabética coincide com ordem cronológica. É também o único formato que o
`strftime` do SQLite reconhece como data — com `DD/MM/AAAA`, extrair dia da
semana devolveria vazio.

**Booleano como 0/1, não como texto.** Guardar `1` em vez de `"s"` permite que
`sum()` conte os dias positivos e `mean()` devolva a proporção diretamente. Com
texto, cada pergunta exigiria filtrar antes de contar.

**Seed determinístico.** `random.seed(42)` fixa a sequência de sorteios, e a
janela é ancorada em `date(2026, 7, 27)` em vez de `date.today()`. Sem a âncora,
o dado de desenvolvimento mudava a cada virada de meia-noite — e comparar duas
execuções não dizia se a diferença veio do código ou do calendário.

**Validação de completude contra referência externa.** A verificação compara os
dias registrados com uma sequência gerada por `pd.date_range()` a partir de
constantes declaradas, não a partir do `min()` e `max()` do próprio banco.
A versão anterior era auto-referencial: apagar o último dia apenas encolhia o
período, e a conta continuava fechando. Detectar dado faltante exige uma fonte de
verdade independente do dado sendo validado.

**Agregação normalizada.** O resumo semanal mostra média diária além da soma.
Somas de semanas com 6, 7 e 1 dia não são comparáveis — a semana corrente
parecia um colapso quando era apenas incompleta. A coluna `dias` permanece na
tabela como métrica de qualidade: ela é a ressalva impressa ao lado do número.

**Agregação em pandas, coleta em SQL.** A query traz as linhas cruas e o
agrupamento acontece no DataFrame. A escala do projeto (dezenas de linhas)
justifica isso; em volume maior, o `GROUP BY` deveria rodar dentro do banco.

## Limitações conhecidas

- **Duplicação de configuração.** `DATA_FINAL` está escrita em `seed.py` e
  `analyze.py`, e o caminho do banco em três arquivos. Mudar em um e esquecer o
  outro quebra em silêncio. A correção seria centralizar num `config.py`.
- **Troca de banco é manual.** Alternar entre `data.db` e `data_dev.db` exige
  editar a constante `CAMINHO` — e, junto com ela, a âncora de data, já que o
  banco real acompanha o calendário e o de desenvolvimento não.
- **Semana sem registro desaparece do relatório.** `groupby` só cria grupo para
  o que existe no dado; uma semana inteira sem registro não vira linha com zero,
  ela some da tabela. Abandonar a coleta deixa o relatório mais limpo, não mais
  alarmante.
- **Médias dividem pelos dias registrados, não pelos dias do calendário.** Um dia
  esquecido move a média sem que nada tenha mudado na rotina — e como o dia
  esquecido tende a ser o dia bagunçado, o viés é para cima.
- **Amostras pequenas não são sinalizadas.** `taxa_academia = 1.00` sobre um
  único dia aparece igual a `1.00` sobre sete. A normalização resolveu a escala,
  não a confiança.
- **Migração de schema é destrutiva.** Alterar a estrutura da tabela exige apagar
  o banco e recriar, perdendo o histórico. Aceitável neste volume; em produção,
  o caminho seria `ALTER TABLE` ou uma ferramenta de *migrations*.
- **Dado sintético não tem a distribuição do dado real.** O seed sorteia leitura
  em 50/50 e produziu 81% na amostra. Ele serve para testar se o código funciona,
  não para concluir nada.
- **Sem agendamento.** A execução é manual, e não existe lembrete — a coleta
  depende inteiramente de disciplina.

## Contexto

Projeto construído como estudo prático de engenharia de dados: um fluxo completo
de coleta, armazenamento, transformação e visualização, em escala reduzida e sem
infraestrutura pesada. A escolha do SQLite e a ausência de orquestrador são
deliberadas — o objetivo é dominar os conceitos de idempotência, qualidade de
dados e modelagem antes de introduzir ferramentas que apenas coordenam scripts
que já funcionam.

## Próximos passos

- Centralizar constantes em `config.py`
- Reindexar o resumo semanal para que semanas vazias apareçam como zero
- Agendar a execução (Agendador de Tarefas do Windows)
- Migrar de SQLite para PostgreSQL