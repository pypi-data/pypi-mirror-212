import os
import unittest
import src.migrate as migrate

class Test(unittest.TestCase):
    def setUp(self):
        with open('test.db', 'w') as file:
            file.close()
        self.db = f"{os.getcwd()}/test.db"

    def test_migrate_test1_init(self):
        with self.assertRaises(SystemExit):
            migrate.Migrate("execute", self.db, driver='sqlite')

    def test_migrate_test2_create(self):
        migrate.Migrate("create", self.db, driver='sqlite', migration_name="test")

    def test_migrate_test3_migrate(self):
        with open('migrations/001_migrate.sql', 'w') as file:
            file.write("""
                CREATE TABLE test (
                    id INTEGER PRIMARY KEY
                )
            """)

        migrate.Migrate("execute", self.db, driver='sqlite')
