from main import app, socketio,db

db.create_all()
if __name__ == '__main__':
    socketio.run(app, debug=True, host="", port=5000)

