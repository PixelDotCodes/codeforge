# CodeForge

> **A coding practice and contest tracker built to make progress measurable.**

CodeForge is a desktop application for tracking coding problems, revision, contests, goals, activity, and performance analytics in one place.

Instead of keeping coding progress scattered across different platforms and notes, CodeForge brings the important data together and turns it into useful insights.

---

## Features

### Problem Tracking

* Track solved coding problems
* Record difficulty and topic
* Maintain problem-solving history
* Track progress over time

### Revision

* Keep track of problems that need revision
* Organize revision based on previous activity
* Monitor revision progress

### Goals & Streaks

* Set coding goals
* Monitor progress toward goals
* Track coding activity and streaks

### Analytics

* Analyze problem-solving progress
* View topic and difficulty statistics
* Visualize activity and progress through charts

---

## Architecture

CodeForge follows a layered architecture to keep the user interface, application logic, and database operations separate.

The application is designed so that:

* **Frontend** handles user interaction.
* **Business Logic** determines what the application should do.
* **Repository / Data Access Layer** handles database operations.
* **PostgreSQL** stores the application data.

---

## Tech Stack

| Technology   | Purpose                 |
| ------------ | ----------------------- |
| Python       | Application development |
| Tkinter      | Desktop GUI             |
| PostgreSQL   | Database                |
| Matplotlib   | Data visualization      |
| Git & GitHub | Version control         |

---

## Project Structure

```text
codeforge/
│
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
│
├── database/
│
├── app/
│   ├── models/
│   ├── repositories/
│   ├── services/
│   ├── gui/
│   └── analytics/
│
└── tests/
```

> The project structure will evolve as development progresses.

---


## Getting Started

Clone the repository:

```bash
git clone https://github.com/PixelDotCodes/codeforge.git
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

The application is currently under development.

---

## Project Goal

CodeForge aims to provide a structured way to understand and improve coding practice by combining **problem tracking, revision, contest activity, goals, and analytics** into a single application.

---

## License

This project is licensed under the MIT License.
