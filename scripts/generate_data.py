import psycopg2
from kafka import KafkaProducer
import json, random, time

# Генерация в PostgreSQL
conn = psycopg2.connect(host="srv-db-01", user="postgres", password="postgres", database="postgres")
cur = conn.cursor()

for _ in range(10):
    cur.execute("INSERT INTO orders (user_id, product, amount) VALUES (%s, %s, %s)",
                (random.randint(1, 100), random.choice(['Laptop', 'Phone', 'Tablet']), round(random.uniform(100, 2000), 2)))
conn.commit()
conn.close()

# Генерация в Kafka
producer = KafkaProducer(bootstrap_servers='srv-db-01:9092')

for _ in range(10):
    event = {
        "user_id": random.randint(1, 100),
        "action": random.choice(["view", "cart", "purchase"]),
        "timestamp": time.time()
    }
    producer.send("user_actions", json.dumps(event).encode('utf-8'))

producer.close()
print("Данные сгенерированы")
