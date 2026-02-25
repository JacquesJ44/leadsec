#!/usr/bin/env python3
"""Create an initial admin user for the application.

Usage:
  source venv/bin/activate
  python create_admin.py

The script will prompt for username, email and password.
"""
import getpass
import sys
from app import create_app
from app.models import db, User


def prompt(prompt_text, default=None):
    if default:
        return input(f"{prompt_text} [{default}]: ") or default
    return input(f"{prompt_text}: ")


def main():
    app = create_app()
    with app.app_context():
        username = prompt('Username', 'admin')
        email = prompt('Email', '')

        # Read password twice
        while True:
            password = getpass.getpass('Password: ')
            if not password:
                print('Password cannot be empty')
                continue
            password2 = getpass.getpass('Confirm Password: ')
            if password != password2:
                print('Passwords do not match, try again')
                continue
            break

        existing = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing:
            print('A user with that username or email already exists:')
            print(f'  id={existing.id} username={existing.username} email={existing.email}')
            confirm = input('Do you want to overwrite/update the password for this user? (y/N): ').lower()
            if confirm != 'y':
                print('Aborting.')
                sys.exit(1)
            user = existing
        else:
            user = User(username=username, email=email)

        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        print(f'User created/updated: id={user.id} username={user.username} email={user.email}')


if __name__ == '__main__':
    main()
