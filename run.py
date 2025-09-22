from ecocycle_app import app, initialize_database

if __name__ == '__main__':
    # Ensure database is initialized
    initialize_database()
    app.run(debug=True, host='0.0.0.0', port=5000)