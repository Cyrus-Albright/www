from app import create_app

app = create_app("default")

if __name__ == "__main__":
    app.debug = app.config.get("DEBUG")
    app.run(host="0.0.0.0", port="8000")
