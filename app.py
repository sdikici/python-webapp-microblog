from flask import Flask, render_template, request, redirect, url_for
import os
import datetime
from pymongo import MongoClient, DESCENDING
from dotenv import load_dotenv
import pytz

load_dotenv()


def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.Microblog

    app.config['TIMEZONE'] = pytz.timezone('Europe/Berlin')

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            current_time = datetime.datetime.now(app.config['TIMEZONE'])

            formatted_date = current_time.strftime("%Y-%m-%d %H:%M:%S")
            app.db.entries.insert_one(
                {"content": entry_content, "date": formatted_date})
            return redirect(url_for('home'))

        entries = app.db.entries.find({}).sort("date", DESCENDING)

        entries_with_date = [(
            entry["content"],
            entry["date"],
            datetime.datetime.strptime(
                entry["date"], "%Y-%m-%d %H:%M:%S").strftime("%b %d")
        )
            for entry in entries
        ]
        return render_template("home.html", entries=entries_with_date)

    return app
