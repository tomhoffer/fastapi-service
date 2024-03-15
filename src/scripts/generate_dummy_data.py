import psycopg2.extras
import faker

"""
    Utility script that generates dummy data for the records table
"""

f = faker.Faker()
connection = psycopg2.connect(
    dbname="pm_assignment", user="PM_user", password="PM_password", host="localhost"
)
connection.set_session(autocommit=True)

with connection.cursor() as cursor:
    cursor.execute(
        """
                CREATE TABLE IF NOT EXISTS records  (
                    id SERIAL PRIMARY KEY,
                    email domain_email UNIQUE,
                    text VARCHAR(100)
                );"""
    )

    unique_emails = set([f.email() for _ in range(10**4)])

    records = [(el, f.sentence(nb_words=4)) for el in unique_emails]
    psycopg2.extras.execute_batch(
        cursor,
        "INSERT INTO records (email, text) VALUES (%s, %s)",
        records,
        page_size=10**3,
    )
    print(f"{len(unique_emails)} rows inserted.")
connection.close()
