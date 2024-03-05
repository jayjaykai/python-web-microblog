import datetime
import os
from flask import Flask, render_template, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGODB_URI")
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def create_app():
    app=Flask(__name__)
    app.db = client.microblog
    # entries=[]

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method=="POST":
            entry_content=request.form.get("content")
            formatted_date=datetime.datetime.today().strftime("%Y-%m-%d")
            # entries.append((entry_content, formatted_date))
            app.db.entries.insert_one({"content": entry_content, "date": formatted_date})

        entries_with_date=[
            (
                # entry[0],
                # entry[1],
                # datetime.datetime.strptime(entry[1], "%Y-%m-%d").strftime("%b %d")
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            # for entry in entries
            for entry in app.db.entries.find({})
        ]
        print(entries_with_date)
        return render_template("home.html", entries=entries_with_date)
    return app
# app.run()