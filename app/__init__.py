from flask import Flask

app = Flask(__name__)

from app import views # located at the end to avoid a circular import