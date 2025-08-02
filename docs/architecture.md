# Архитектура системы

## Серверы
- **srv-ch-01, srv-ch-02**: ClickHouse кластер с ClickHouse Keeper
- **srv-db-01**: PostgreSQL + Kafka (KRaft)
- **srv-ab-01**: Airbyte (синхронизация данных)
- **srv-mon-01**: Grafana + MinIO (визуализация и хранение)

## Потоки данных
1. Данные генерируются в PostgreSQL и Kafka
2. Airbyte забирает данные и загружает в ClickHouse
3. ClickHouse хранит и обрабатывает
4. Grafana визуализирует
5. Данные выгружаются в CSV и сохраняются

## Демонстрация
- Airbyte: http://srv-ab-01:8000
- Grafana: http://srv-mon-01:3000
- MinIO: http://srv-mon-01:9000
