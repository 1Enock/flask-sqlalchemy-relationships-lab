from server.app import app
from server.models import Event, Session, Speaker, Bio, db

with app.app_context():
    try:
        events = Event.query.all()
    except Exception:
        events = []

__all__ = ["app", "Event", "Session", "Speaker", "Bio", "db", "events"]
