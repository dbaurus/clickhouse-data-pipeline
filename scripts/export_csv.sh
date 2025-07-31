#!/bin/bash
clickhouse-client --query="SELECT * FROM analytics.orders_all WHERE toDate(created_at) = today()" \
                  --format=CSVWithNames > /minio/backups/orders_$(date +%F).csv
