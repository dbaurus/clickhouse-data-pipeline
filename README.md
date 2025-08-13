# ClickHouse Data Pipeline
Cистема управления потоками данных с ClickHouse.

## 🖥️ Серверы
- ClickHouse: srv-ch-01, srv-ch-02
- DB: srv-db-01 (PostgreSQL)
- Airbyte: srv-ab-01
- Monitoring: srv-mon-01 (Superset)

## 🚀 Запуск
```bash
ansible-playbook -i ansible/inventory.ini ansible/site.yml --ask-become-pass
