#!/usr/bin/env python3
"""
Скрипт для генерации синтетических данных:
- Вставка заказов в PostgreSQL
- Отправка событий пользователей в Kafka
"""

import random
import time
import psycopg2
from datetime import datetime, timedelta
from kafka import KafkaProducer
import json
import logging
import sys

# ================================
# Настройки логирования
# ================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ================================
# 🔧 Конфигурация подключения
# ================================

# PostgreSQL
PG_CONFIG = {
    'host': 'srv-db-01',        # или 'localhost', если запускается на том же сервере
    'port': 5432,
    'dbname': 'retail',
    'user': 'user',
    'password': 'pass'
}

# Kafka
KAFKA_BROKER = 'srv-db-01:9092'  # Kafka брокер
KAFKA_TOPIC = 'user_actions'

# Генератор данных
USER_COUNT = 100
PRODUCTS = [
    "Laptop", "Smartphone", "Tablet", "Headphones", "Mouse",
    "Keyboard", "Monitor", "Webcam", "Router", "Smartwatch"
]
ACTIONS = ["view", "add_to_cart", "purchase", "login", "logout", "search"]

# Количество записей для генерации (0 = бесконечно)
MAX_ORDERS = 1000
MAX_EVENTS = 5000


# ================================
# 🛠️ Вспомогательные функции
# ================================

def create_tables_if_not_exists():
    """Создаёт таблицы в PostgreSQL, если их нет"""
    try:
        conn = psycopg2.connect(**PG_CONFIG)
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                product VARCHAR(100) NOT NULL,
                amount NUMERIC(10, 2) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
        ''')

        conn.commit()
        cur.close()
        conn.close()
        logger.info("✅ Таблицы в PostgreSQL проверены/созданы")
    except Exception as e:
        logger.error(f"❌ Ошибка при создании таблиц: {e}")
        sys.exit(1)


def insert_order(user_id, product, amount):
    """Вставляет заказ в PostgreSQL"""
    try:
        conn = psycopg2.connect(**PG_CONFIG)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO orders (user_id, product, amount, created_at) VALUES (%s, %s, %s, NOW())",
            (user_id, product, amount)
        )
        conn.commit()
        cur.close()
        conn.close()
        logger.debug(f"📦 Вставлен заказ: user_id={user_id}, product={product}, amount={amount:.2f}")
    except Exception as e:
        logger.error(f"❌ Ошибка вставки в PostgreSQL: {e}")


def send_kafka_event(producer, user_id, action, page=None):
    """Отправляет событие в Kafka"""
    event = {
        "user_id": user_id,
        "action": action,
        "timestamp": int(time.time()),
        "page": page or f"/product/{random.randint(1, 20)}",
        "client_ip": f"192.168.1.{random.randint(1, 254)}"
    }
    try:
        producer.send(KAFKA_TOPIC, value=event)
        logger.debug(f"📤 Отправлено в Kafka: {event}")
    except Exception as e:
        logger.error(f"❌ Ошибка отправки в Kafka: {e}")


# ================================
# 🚀 Основная функция
# ================================

def main():
    logger.info("🚀 Запуск генератора синтетических данных...")

    # Создание таблиц
    create_tables_if_not_exists()

    # Подключение к Kafka
    try:
        producer = KafkaProducer(
            bootstrap_servers=[KAFKA_BROKER],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='1',
            retries=3
        )
        logger.info(f"✅ Подключено к Kafka: {KAFKA_BROKER}")
    except Exception as e:
        logger.error(f"❌ Не удалось подключиться к Kafka: {e}")
        sys.exit(1)

    # Счётчики
    order_count = 0
    event_count = 0

    # Бесконечный цикл генерации
    try:
        while True:
            # === Генерация заказа (реже) ===
            if MAX_ORDERS == 0 or order_count < MAX_ORDERS:
                if random.random() < 0.3:  # 30% шанс заказа
                    user_id = random.randint(1, USER_COUNT)
                    product = random.choice(PRODUCTS)
                    amount = round(random.uniform(50, 2000), 2)
                    insert_order(user_id, product, amount)
                    order_count += 1

            # === Генерация события Kafka (чаще) ===
            if MAX_EVENTS == 0 or event_count < MAX_EVENTS:
                user_id = random.randint(1, USER_COUNT)
                action = random.choice(ACTIONS)
                send_kafka_event(producer, user_id, action)
                event_count += 1

            # === Ограничение частоты ===
            time.sleep(0.5)  # ~2 события в секунду

            # === Ограничение по количеству ===
            if MAX_ORDERS > 0 and order_count >= MAX_ORDERS and \
               MAX_EVENTS > 0 and event_count >= MAX_EVENTS:
                logger.info("✅ Все данные сгенерированы. Завершение.")
                break

    except KeyboardInterrupt:
        logger.info("🛑 Генерация остановлена пользователем.")
    except Exception as e:
        logger.error(f"🛑 Критическая ошибка: {e}")
    finally:
        producer.close(timeout=5)
        logger.info("👋 Генератор завершил работу.")


# ================================
# Запуск
# ================================

if __name__ == "__main__":
    main()
