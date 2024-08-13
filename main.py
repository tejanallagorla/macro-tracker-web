from website import create_app

# initialize Flask app
app = create_app()

# run app on local server
if __name__ == '__main__':
    app.run()
