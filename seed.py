#!/usr/bin/env python3

import csv
from config import app, db
from models import Episode, Guest, Appearance

def seed_database():
    # Clear existing data
    db.session.query(Appearance).delete()
    db.session.query(Guest).delete()
    db.session.query(Episode).delete()
    db.session.commit()

    # Create episodes
    episodes = [
        Episode(date="1/11/99", number=1),
        Episode(date="1/12/99", number=2),
        Episode(date="1/13/99", number=3),
    ]
    db.session.add_all(episodes)
    db.session.commit()

    # Create guests
    guests = [
        Guest(name="Michael J. Fox", occupation="actor"),
        Guest(name="Sandra Bernhard", occupation="Comedian"),
        Guest(name="Tracey Ullman", occupation="television actress"),
    ]
    db.session.add_all(guests)
    db.session.commit()

    # Create appearances
    appearances = [
        Appearance(rating=4, episode_id=1, guest_id=1),
        Appearance(rating=5, episode_id=2, guest_id=3),
        Appearance(rating=3, episode_id=3, guest_id=2),
    ]
    db.session.add_all(appearances)
    db.session.commit()

    print("Database seeded successfully!")

if __name__ == '__main__':
    with app.app_context():
        seed_database()