from src import app

def main():
    app.run(
        host=app.config["HOST"],
        port=app.config["PORT"],
        debug=app.config["DEBUG"],
    )

if __name__ == "__main__":
    main()
