from website import create_app

#This is where u should run the program

app = create_app()

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug=True)