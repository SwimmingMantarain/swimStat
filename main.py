from website import create_app

# Create Flask application instance
app = create_app()


# If this script is run directly (as opposed to being imported),
# start the Flask development server
if __name__ == "__main__":
    """
    Start the Flask development server.

    This function is called when the script is run directly.
    It starts the Flask development server with the app instance.
    The `debug` parameter is set to `True` to enable debugging mode.
    The `use_reloader` parameter is set to `False` to disable the automatic reloader.
    """

    app.run(debug=True, use_reloader=False)

