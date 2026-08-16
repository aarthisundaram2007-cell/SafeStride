import unittest

from migrate_sqlite_to_supabase import build_payload_for_remote_columns


class BuildPayloadForRemoteColumnsTest(unittest.TestCase):
    def test_excludes_missing_columns_from_payload(self):
        row = {
            "id": 1,
            "full_name": "Alice",
            "email": "alice@example.com",
            "password": "secret",
            "phone": "123",
            "address": "Main Street",
            "created_at": "2024-01-01",
        }

        payload = build_payload_for_remote_columns(
            row,
            available_columns={"id", "full_name", "email", "password", "phone", "created_at"},
        )

        self.assertEqual(
            payload,
            {
                "id": 1,
                "full_name": "Alice",
                "email": "alice@example.com",
                "password": "secret",
                "phone": "123",
                "created_at": "2024-01-01",
            },
        )


if __name__ == "__main__":
    unittest.main()
