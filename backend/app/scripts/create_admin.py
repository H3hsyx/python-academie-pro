from __future__ import annotations

import argparse

from sqlalchemy import select

from app.core.security import get_password_hash
from app.db.session import SessionLocal, init_db
from app.models import User


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", required=True)
    args = parser.parse_args()
    init_db()
    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.email == args.email))
        if user is None:
            user = User(username=args.username, email=args.email, password_hash=get_password_hash(args.password), role="admin")
            db.add(user)
        else:
            user.role = "admin"
            user.password_hash = get_password_hash(args.password)
        db.commit()
        print(f"Admin pret: {args.email}")


if __name__ == "__main__":
    main()
