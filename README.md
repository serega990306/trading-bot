# trading-bot

```shell
cd trading-bot
docker compose logs -f notifications
docker compose up -d --build
docker compose exec notifications /bin/bash
/bin/ls
/bin/sqlite3 TradingBot.sqlite 'select * from operations;'

id|currency|operation|buy|initial_sell|sell|amount
df38d2a3-4d79-4a6d-a93b-0bf6d0ee0b15|BTCUSDT|LTP3|0.005|0.001|0.002|0.004
```

Setup Docker mirrors:
```shell
vi /etc/docker/daemon.json
{ "registry-mirrors" : [ "https:\/\/huecker.io", "https:\/\/mirror.gcr.io" ] }
systemctl restart docker
docker pull mirror.gcr.io/library/python:3.11

/bin/vim services/positions.txt
```