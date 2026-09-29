# CodeForge

> **A coding practice and revision tracker built to make progress measurable.**

CodeForge is a desktop application for tracking coding problems, revisions, activity, and performance analytics in one place.

It provides a simple way to record solved problems, review practice history, and visualize progress without relying on scattered notes or spreadsheets.

---

## Features

### Problem Tracking

* Add and manage coding problems
* Support for LeetCode and GeeksForGeeks
* Record question number, title, difficulty, and problem URL
* Search and filter problems by platform and difficulty

### Revision Tracking

* Log revisions for existing problems
* Record revision date and revision type
* View revision history
* Maintain a simple review workflow based on practice history

### Activity Tracking

* Automatically record problem practice activity
* Distinguish between new practice and revision activity
* Track activity over time
* View recent activity on the dashboard

### Dashboard

* Problem-solving statistics
* LeetCode-style activity heatmap
* Current practice streak
* Active-day count
* Suggested questions for review
* Top practiced problem

### Analytics

* Difficulty distribution
* Practice consistency
* Activity-based statistics
* Visual charts powered by Matplotlib

---

## Architecture

CodeForge follows a layered architecture:

```text
Tkinter UI
    ↓
Service / Business Logic
    ↓
Repository / Data Access Layer
    ↓
PostgreSQL
```

Each layer has a specific responsibility:

* **UI** handles user interaction and presentation.
* **Services** handle validation and business logic.
* **Repositories** handle PostgreSQL queries and data access.
* **PostgreSQL** stores persistent application data.

---

## Tech Stack

| Technology      | Purpose                 |
| --------------- | ----------------------- |
| Python          | Application development |
| Tkinter         | Desktop GUI             |
| PostgreSQL      | Database                |
| psycopg2-binary | PostgreSQL connectivity |
| Matplotlib      | Data visualization      |
| Git & GitHub    | Version control         |

---

## Project Structure

```text
codeforge/
├── database/
│   ├── __init__.py
│   ├── connection.py
│   └── schema.sql
├── repositories/
├── services/
├── ui/
│   └── views/
├── docs/
├── main.py
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/PixelDotCodes/codeforge.git
cd codeforge
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment on Windows

```powershell
.venv\Scripts\activate
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Configure PostgreSQL

Create a PostgreSQL database named `codeforge`.

Run:

```text
database/schema.sql
```

using pgAdmin Query Tool or `psql`.

CodeForge expects the following PostgreSQL connection settings:

```text
Host: localhost
Port: 5432
Database: codeforge
User: postgres
```

The database password is read from the `DB_PASSWORD` environment variable.

For the current PowerShell session:

```powershell
$env:DB_PASSWORD="your_password"
```

### 6. Run CodeForge

```powershell
python main.py
```

---

## Project Goal

CodeForge is designed to make coding practice more structured by combining problem tracking, revision history, activity tracking, and analytics into a single desktop application.

---

## License

This project is licensed under the MIT License.
