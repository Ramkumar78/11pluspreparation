from flask import Flask
from VocabQuest.backend.app import app

with app.app_context():
    commands = list(app.cli.list_commands(app.app_context()))
    print("Available commands:", commands)
    if "seed-db" in commands:
        print("FAIL: seed-db is present")
        exit(1)
    if "init-db" not in commands:
        print("FAIL: init-db is missing")
        exit(1)
    print("SUCCESS: seed-db is absent and init-db is present")
