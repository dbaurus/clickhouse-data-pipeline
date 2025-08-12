-- Создание базы данных на всех узлах кластера
CREATE DATABASE IF NOT EXISTS analytics ON CLUSTER '{cluster}';

--Создаём управляемую Airbyte базу
CREATE TABLE IF NOT EXISTS analytics.orders ON CLUSTER '{cluster}'
(
    `_airbyte_raw_id` String,                       -- UUID строки
    `_airbyte_extracted_at` DateTime64,             -- Время извлечения
    `_airbyte_meta` String,                         -- Мета-данные (JSON, опционально)
    `_airbyte_generation_id` UInt32                 -- ID "поколения" данных
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/analytics/orders', '{replica}')
ORDER BY _airbyte_extracted_at
PARTITION BY toYYYYMM(_airbyte_extracted_at)
SETTINGS index_granularity = 8192;
