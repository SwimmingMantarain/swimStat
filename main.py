import sys
from website import create_app
app = create_app()

if "--ignore-errors" in sys.argv:
    sys.argv.remove("--ignore-errors")

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)