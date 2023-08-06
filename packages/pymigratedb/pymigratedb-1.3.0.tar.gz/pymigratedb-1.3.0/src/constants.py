sqlite_protocol="sqlite:////"
pgsql_protocol="postgresql+psycopg2://"

sqlite = """
    CREATE TABLE IF NOT EXISTS migrations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        app TEXT NOT NULL,
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""

pgsql = """
    CREATE TABLE IF NOT EXISTS migrations (
        id serial NOT NULL,
        "name" varchar NOT NULL,
        app varchar NOT NULL,
        applied_at timestamptz(0) NOT NULL DEFAULT now(),
        CONSTRAINT migrations_pk PRIMARY KEY (id)
    );

    CREATE TABLE IF NOT EXISTS health (
        sync timestamptz NOT NULL,
        CONSTRAINT sync_pk PRIMARY KEY (sync)
    );
"""
