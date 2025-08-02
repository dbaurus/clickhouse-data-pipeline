CREATE DATABASE IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.orders_local (
    id UInt32,
    user_id UInt32,
    product String,
    amount Decimal(10,2),
    created_at DateTime
) ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/orders', '{replica}')
ORDER BY (created_at, user_id);

CREATE TABLE IF NOT EXISTS analytics.orders_all AS analytics.orders_local
ENGINE = Distributed(clickhouse_cluster, default, orders_local, rand());
