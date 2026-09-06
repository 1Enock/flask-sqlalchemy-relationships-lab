#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/events')
def get_events():
    events = Event.query.all()
    return jsonify([
        {"id": event.id, "name": event.name, "location": event.location}
        for event in events
    ])


@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    event = db.session.get(Event, id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    sessions = [{
        "id": session.id,
        "title": session.title,
        "start_time": session.start_time.isoformat() if session.start_time else None,
        "event_id": session.event_id,
    } for session in event.sessions]
    return jsonify(sessions)


@app.route('/speakers')
def get_speakers():
    speakers = Speaker.query.all()
    return jsonify([
        {"id": speaker.id, "name": speaker.name}
        for speaker in speakers
    ])


@app.route('/speakers/<int:id>')
def get_speaker(id):
    speaker = db.session.get(Speaker, id)
    if not speaker:
        return jsonify({"error": "Speaker not found"}), 404

    bio_text = speaker.bio.bio_text if speaker.bio else "No bio available"
    return jsonify({
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": bio_text,
    })


@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    session = db.session.get(Session, id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    speakers = [{
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": speaker.bio.bio_text if speaker.bio else None,
    } for speaker in session.speakers]
    return jsonify(speakers)


if __name__ == '__main__':
    app.run(port=5555, debug=True)