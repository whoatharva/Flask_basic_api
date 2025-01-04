# Flask Basic API

A simple RESTful API using Flask, Flask-RESTful, and Flask-SQLAlchemy for user management with SQLite.

## Setup

1. **Clone the Repo**  
   ```bash
   git clone https://github.com/whoatharva/Flask_basic_api.git
   cd Flask_basic_api
   ```

2. **Install Dependencies**  
   ```bash
   pip install -r requirement.txt
   ```

3. **Initialize Database**  
   ```bash
   python create_db.py
   ```

4. **Run the Server**  
   ```bash
   python api.py
   ```

Access the API at `http://127.0.0.1:5000/`.

## Endpoints

- **`/api/users/`**
  - `GET`: List all users.
  - `POST`: Add a new user (`name`, `email`).

- **`/api/users/<id>`**
  - `GET`: Get user by ID.
  - `PATCH`: Update user (`name`, `email`).
  - `DELETE`: Delete user by ID.

## Example

Create a user:
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"name": "John", "email": "john@example.com"}' \
http://127.0.0.1:5000/api/users/
```

---

Happy Coding! 🚀
