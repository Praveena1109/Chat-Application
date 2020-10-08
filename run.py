from main import app, socketio, db
import os

db.create_all()
if __name__ == '__main__':
    socketio.run(app, debug=True, host=os.environ.get('HOST'), port=5000)

