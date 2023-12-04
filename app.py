from website import create_app
#imports the whole website folder, and the create_app() from __init__.py
app = create_app()
if __name__ == "__main__":
    # the returned object from create_app() with all the config in
    app.run(debug=True)