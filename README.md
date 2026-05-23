# 📋 Smart Task Management System

**Sankar Group — Python Development Internship Assignment**

**Candidate:** Goudampally Sai Snehitha  
**Domain:** Python Developer Intern  
**College:** Anurag University, Hyderabad  

---

## 🚀 Features

- ✅ User Registration & Login with password hashing
- ✅ REST APIs — Add, Update, Delete, Get All Tasks
- ✅ SQLite Database (PostgreSQL compatible structure)
- ✅ Analytics using Pandas & NumPy
- ✅ Real-time updates using WebSockets
- ✅ Clean responsive frontend with HTML & CSS
- ✅ Task filtering by status and priority

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.x | Core language |
| Flask | Web framework |
| SQLite | Database |
| Pandas & NumPy | Analytics module |
| Flask-SocketIO | WebSocket support |
| HTML & CSS | Frontend |

---

## 📁 Project Structure

```
smart-task-manager/
├── app.py              # Main Flask application
├── database.py         # Database initialization
├── analytics.py        # Pandas & NumPy analytics
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── templates/
│   ├── index.html      # Main dashboard
│   ├── login.html      # Login page
│   └── register.html   # Register page
└── static/
    └── style.css       # Stylesheet
```

---

## ⚙️ Setup Instructions

### Step 1 — Clone the repository
```bash
git clone https://github.com/saisnehitha28/smart-task-manager.git
cd smart-task-manager
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Run the application
```bash
python app.py
```

### Step 4 — Open in browser
```
http://127.0.0.1:5000
```

---

## 🔌 REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/tasks | Get all tasks |
| POST | /api/tasks | Add new task |
| PUT | /api/tasks/:id | Update task |
| DELETE | /api/tasks/:id | Delete task |
| GET | /api/analytics | Get analytics data |

---

## 📊 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    username   TEXT NOT NULL,
    email      TEXT UNIQUE NOT NULL,
    password   TEXT NOT NULL,
    created_at TEXT NOT NULL
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    title       TEXT NOT NULL,
    description TEXT,
    priority    TEXT DEFAULT 'Medium',
    status      TEXT DEFAULT 'Pending',
    created_at  TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 📸 Screenshots

*[Add screenshots here after running the project]*

---

## 🎯 Evaluation Coverage

| Criteria | Implementation |
|---|---|
| Flask & REST APIs | ✅ Full CRUD REST API |
| Database Integration | ✅ SQLite with proper schema |
| Code Quality | ✅ Clean, commented code |
| Pandas & NumPy | ✅ Analytics module |
| WebSocket Feature | ✅ Real-time task notifications |
| Frontend UI | ✅ Responsive HTML/CSS |

---

*Developed by Goudampally Sai Snehitha — Sankar Group Internship Assignment 2026*
## 👩‍💻 About Me

I am Goudampally Sai Snehitha, a B.Tech CSE student
at Anurag University, Hyderabad (CGPA: 8.3). I built
this Smart Task Management System as part of my Python
Developer internship assignment at Sankar Group.

This project helped me practically learn:
- Flask web framework and REST API development
- Database design and SQLite integration
- Pandas and NumPy for data analytics
- WebSockets for real-time communication
- Responsive frontend with HTML and CSS

I am passionate about Python development and eager
to build real-world applications!

**Connect with me:**
- LinkedIn: linkedin.com/in/saisnehitha-goudampally
- GitHub: github.com/saisnehitha28
- Email: saisnehitha701@gmail.com
