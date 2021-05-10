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

## Funcionamento

O bot funciona com um simples 

`python bot.py`

A rotina que faz a contagem de dias dos objetos é executada uma vez ao dia usando-se

`python count_day.py`
