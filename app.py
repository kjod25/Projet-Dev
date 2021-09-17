"""Application runner."""

print("For Cover : http://127.0.0.1:5000/Welcome/")

from sources import init_app


app = init_app()


if __name__ == "__main__":
    app.run(debug=True)