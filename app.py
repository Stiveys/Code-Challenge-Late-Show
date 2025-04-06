from flask import request, jsonify, make_response, redirect
from config import app, db
from models import Episode, Guest, Appearance

# Routes
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Welcome to the Late Show API",
        "available_endpoints": [
            "/episodes - Get all episodes",
            "/episodes/<id> - Get a specific episode",
            "/guests - Get all guests",
            "/appearances - Create a new appearance (POST)"
        ]
    })

@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([episode.to_dict() for episode in episodes])

@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    # Include appearances in the response
    episode_data = episode.to_dict()
    episode_data['appearances'] = [appearance.to_dict() for appearance in episode.appearances]
    return jsonify(episode_data)

@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([guest.to_dict() for guest in guests])

@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()

    # Check if required fields are present
    if not all(key in data for key in ['rating', 'episode_id', 'guest_id']):
        return jsonify({"errors": ["Missing required fields"]}), 400

    # Check if episode and guest exist
    episode = Episode.query.get(data['episode_id'])
    guest = Guest.query.get(data['guest_id'])

    if not episode or not guest:
        return jsonify({"errors": ["Episode or Guest not found"]}), 404

    try:
        # Create new appearance
        new_appearance = Appearance(
            rating=data['rating'],
            episode_id=data['episode_id'],
            guest_id=data['guest_id']
        )

        db.session.add(new_appearance)
        db.session.commit()

        return jsonify(new_appearance.to_dict())
    except ValueError as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["An error occurred while creating the appearance"]}), 500

if __name__ == '__main__':
    app.run(port=5555, debug=True)