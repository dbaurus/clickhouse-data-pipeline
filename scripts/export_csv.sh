#!/bin/bash
# Выгрузка последних заказов в CSV

clickhouse-client --host srv-ch-01 --port 8123 \
  --query="SELECT * FROM analytics.orders_all LIMIT 100" \
  --format CSVWithNames > /tmp/orders_$(date +%F).csv

echo "CSV сохранён: /tmp/orders_$(date +%F).csv"
