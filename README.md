# [Calango HC](https://calango.club)

Bot do balde de sete dias.

## Configuração

Edite o `balde.conf_sample` e renomeie para `balde.conf`

```
TOKEN = Token do bot do Telegram.
CHANNELID = Id do canal do Telegram para onde irão os posts.
GROUPID = Id do grupo em que o bot fará a verificação se a pessoa faz parte antes de fazer a postagem.
```

É necessário ter a lib instalada para que tudo funcione

`pip install pytelegrambotapi`

Por fim, é necessário um banco de dados e uma tabela para que tudo funcione.

```
import sqlite3

db = 'CalangoHC'
table = 'Balde'
conn = sqlite3.connect(db)
cursor = conn.cursor()
aux = ('''CREATE TABLE {} (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    post TEXT,
    photo TEXT,
    desc TEXT,
    days INT,
    newp TEXT,
    name TEXT);
''').format(table)
cursor.execute(aux)
```

## Funcionamento

O bot funciona com um simples 

`python bot.py`

A rotina que faz a contagem de dias dos objetos é executada uma vez ao dia usando-se

`python count_day.py`
