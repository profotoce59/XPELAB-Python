"""Creates the `movies` table.

The equivalent of `cargo run --bin init_db`.
Run: python -m src.examples.init_db
"""

from dotenv import load_dotenv

from src.datasource import postgres_datasource
from src.errors import XpelabError


def main() -> None:
    load_dotenv()
    print("Environment variables loaded")

    try:
        postgres_datasource.initialize_db()
    except XpelabError as error:
        print(f"Failed to initialize database: {error}")
    else:
        print("Database initialized successfully")


if __name__ == "__main__":
    main()
