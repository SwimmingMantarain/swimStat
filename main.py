from website import create_app

# Create Flask application instance
app = create_app()

# start the Flask development server
if __name__ == "__main__":

    app.run(debug=True, use_reloader=False)

