from flask import Blueprint, render_template
from models import Jobs

main = Blueprint("main", __name__)

@main.route("/")
def home():
    jobs = Jobs.query.all()
    return render_template("index.html", jobs=jobs)
