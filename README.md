# 📝 Flask ToDo API

A simple, production-ready RESTful ToDo API built with:

- 🔥 Flask & Flask-RESTX
- 🔐 JWT-based Authentication
- 🐘 PostgreSQL
- 🐳 Docker & Docker Compose
- 🧪 Swagger UI Documentation

---

## 🚀 Features

- User registration and login
- JWT token generation & protected routes
- CRUD operations for ToDos
- Swagger UI at `/docs` with JWT authorization
- Dockerized deployment
- PostgreSQL database
- `.env` config for secrets

---

## 📁 Project Structure

todo-app/
│
├── app/
│   ├── __init__.py        # App factory, API setup, DB config
│   ├── auth.py            # Signup/login routes
│   ├── models.py          # User & ToDo models
│   ├── routes.py          # ToDo CRUD endpoints
│   ├── protected.py       # Example protected route
│   ├── database.py        # db instance
│   ├── jwt.py             # JWTManager initialization
│
├── run.py                # Entry point
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── Dockerfile            # Web service Dockerfile
├── docker-compose.yml    # Compose file with PostgreSQL
└── README.md             # You're here!

---

## ⚙️ .env Configuration

Create a `.env` file in the root:

```
DATABASE_URL=postgresql://postgres:postgres@postgres_db:5432/tododb
JWT_SECRET_KEY=your-secret-key
```

---

## 🐳 Running the App (Docker)

```bash
# Build and start containers
sudo docker compose up --build
```

App will be available at:
- http://localhost:5000

Swagger UI:
- http://localhost:5000/docs

---

## 🧪 API Documentation (via Swagger UI)
Visit http://localhost:5000/docs

Use the Authorize button and paste:
```
Bearer <your-jwt-token>
```

---

## 📦 API Endpoints Summary

| Method | Endpoint              | Description                | Auth |
|--------|-----------------------|----------------------------|------|
| POST   | /auth/signup          | Register a new user        | ❌   |
| POST   | /auth/login           | Login and get JWT          | ❌   |
| GET    | /todos/               | List all ToDos             | ✅   |
| POST   | /todos/               | Create a new ToDo          | ✅   |
| PUT    | /todos/<id>           | Update a ToDo by ID        | ✅   |
| DELETE | /todos/<id>           | Delete a ToDo by ID        | ✅   |
| GET    | /protected/secret     | Sample protected route      | ✅   |

---

## 🐘 PostgreSQL Access

Docker DB container:
- Host: postgres_db
- Port: 5432
- User: postgres
- Password: postgres
- DB: tododb

---

## 📦 Python Dependencies

```
Flask==2.3.3
Flask-RESTX==1.3.0
Flask-SQLAlchemy==3.1.1
flask-jwt-extended==4.6.0
python-dotenv==1.0.1
psycopg2-binary==2.9.9
```

---

## 🧹 Reset Containers

```bash
# Stop and remove all containers
docker compose down

# Rebuild everything fresh
docker compose up --build
```

---

## 👨‍💻 Author
Muhammad Yasin  
