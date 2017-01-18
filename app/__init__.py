from flask import Flask

app = Flask(__name__)
app.secret_key = "superdupersecretkey"

from app import views # located at the end to avoid a circular import