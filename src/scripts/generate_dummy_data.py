import asyncio
import psycopg
import faker

"""
    Utility script that generates dummy data for the records table using psycopg3 (async), batching inserts and handling unique constraint violations. Retries until the desired number of unique records is inserted. Uses executemany for batch inserts.
"""

BATCH_SIZE = 100_000
TOTAL_RECORDS = 10_000_000

async def main():
    f = faker.Faker()
    async with await psycopg.AsyncConnection.connect(
        dbname="dummy_db", user="User", password="Password", host="localhost"
    ) as connection:
        await connection.set_autocommit(True)
        async with connection.cursor() as cursor:
            await cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS records  (
                        id SERIAL PRIMARY KEY,
                        email domain_email UNIQUE,
                        text VARCHAR(100)
                    );"""
            )

            # Get current count of records
            await cursor.execute("SELECT COUNT(*) FROM records")
            inserted = (await cursor.fetchone())[0]
            while inserted < TOTAL_RECORDS:
                batch = []
                while len(batch) < BATCH_SIZE:
                    email = f.email()
                    text = f.sentence(nb_words=4)
                    batch.append((email, text))
                await cursor.executemany(
                    "INSERT INTO records (email, text) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING",
                    batch,
                )
                await cursor.execute("SELECT COUNT(*) FROM records")
                inserted = (await cursor.fetchone())[0]
                print(f"Inserted {inserted} records...")
            print(f"Done. Inserted {inserted} unique records.")

if __name__ == "__main__":
    asyncio.run(main())
