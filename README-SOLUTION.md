# Late Show API

This is a Flask API for tracking late show episodes, guests, and their appearances. The API allows you to view episodes and guests, as well as create new appearances with ratings.

## Setup Instructions

1. Clone the repository
2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Initialize the database:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```
5. Seed the database with sample data:
   ```
   python seed.py
   ```
6. Run the application:
   ```
   python app.py
   ```
   The server will start on http://127.0.0.1:5555/

## API Endpoints

### GET /
Returns a welcome message and list of available endpoints.

**Response Example:**
```json
{
  "message": "Welcome to the Late Show API",
  "available_endpoints": [
    "/episodes - Get all episodes",
    "/episodes/<id> - Get a specific episode",
    "/guests - Get all guests",
    "/appearances - Create a new appearance (POST)"
  ]
}
```

### GET /episodes
Returns a list of all episodes.

**Response Example:**
```json
[
  {
    "id": 1,
    "date": "1/11/99",
    "number": 1
  },
  {
    "id": 2,
    "date": "1/12/99",
    "number": 2
  }
]
```

### GET /episodes/:id
Returns a specific episode by ID, including all appearances.

**Response Example (Success - 200 OK):**
```json
{
  "id": 1,
  "date": "1/11/99",
  "number": 1,
  "appearances": [
    {
      "id": 1,
      "rating": 4,
      "episode_id": 1,
      "guest_id": 1,
      "guest": {
        "id": 1,
        "name": "Michael J. Fox",
        "occupation": "actor"
      }
    }
  ]
}
```

**Response Example (Not Found - 404):**
```json
{
  "error": "Episode not found"
}
```

### GET /guests
Returns a list of all guests.

**Response Example:**
```json
[
  {
    "id": 1,
    "name": "Michael J. Fox",
    "occupation": "actor"
  },
  {
    "id": 2,
    "name": "Sandra Bernhard",
    "occupation": "Comedian"
  }
]
```

### POST /appearances
Creates a new appearance with a rating for a specific episode and guest.

**Request Body:**
```json
{
  "rating": 5,  // Must be between 1 and 5
  "episode_id": 1,
  "guest_id": 2
}
```

**Response Example (Success - 200 OK):**
```json
{
  "id": 3,
  "rating": 5,
  "guest_id": 2,
  "episode_id": 1,
  "episode": {
    "date": "1/11/99",
    "id": 1,
    "number": 1
  },
  "guest": {
    "id": 2,
    "name": "Sandra Bernhard",
    "occupation": "Comedian"
  }
}
```

**Response Example (Validation Error - 400):**
```json
{
  "errors": ["Rating must be between 1 and 5"]
}
```

**Response Example (Not Found - 404):**
```json
{
  "errors": ["Episode or Guest not found"]
}
```

## Models

### Episode
Represents a late show episode with a date and number.

**Attributes:**
- `id`: Integer, primary key
- `date`: String, the date of the episode
- `number`: Integer, the episode number

### Guest
Represents a guest with a name and occupation.

**Attributes:**
- `id`: Integer, primary key
- `name`: String, the guest's name
- `occupation`: String, the guest's occupation

### Appearance
Represents a guest's appearance on an episode with a rating.

**Attributes:**
- `id`: Integer, primary key
- `rating`: Integer, must be between 1 and 5 (inclusive)
- `episode_id`: Integer, foreign key to Episode
- `guest_id`: Integer, foreign key to Guest

**Validations:**
- Rating must be between 1 and 5 (inclusive)

## Relationships

- An Episode has many Guests through Appearances
- A Guest has many Episodes through Appearances
- An Appearance belongs to both an Episode and a Guest
- Cascade delete is configured for Appearances when an Episode or Guest is deleted
