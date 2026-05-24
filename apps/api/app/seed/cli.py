import sys

from app.seed.runtime import init_database, reset_and_reseed, seed_database


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "init"

    if command == "init":
        from app.core.database import db_session

        with db_session() as db:
            init_database()
            seed_database(db, force=False)
    elif command in {"reseed", "reset"}:
        reset_and_reseed()
    elif command == "path":
        from app.core.database import database_path

        print(database_path())
    else:
        raise SystemExit(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
