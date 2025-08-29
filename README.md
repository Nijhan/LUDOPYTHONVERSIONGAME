


# LUDOPYTHONVERSIONGAME# 🎲 LUDO GAME (Console MVP)


**Date:** August 20, 2025
**Team:** Najma, Maina, Evalyne, Adrian, Everyone

A console-based **Ludo Game** written in Python with:

* 🎲 Dice rolls & token movement
* 🔄 Turn-based play for 2–4 players
* 🏆 Win detection logic
* 💾 Persistent player stats & saved games (PostgreSQL)
* ✅ Unit tests for core functionality

---

## 🚀 Features (MVP)

* [x] Dice Roll Logic (1–6 random)
* [x] Turn Management (player rotation + extra turn on 6)
* [x] Board Representation (linearized path for MVP)
* [x] Player Tokens (enter on 6, move stepwise, exact finish)
* [x] Winning Condition Detection
* [x] Player Registration & Stats
* [ ] Save/Load Ongoing Games (DB persistence – in progress)
* [ ] Advanced Movement (captures, safe squares – planned)

---

## 📂 Project Structure

```
LUDO GAME/
├── main.py                  # Game entrypoint (console loop)
├── game_logic.py            # Dice, movement, winning logic
├── database.py              # PostgreSQL integration
├── players.py               # Player registration & stats
├── utils/                   # Helpers
│   ├── dice_utils.py
│   └── movement_utils.py
├── tests/                   # Unit tests
│   ├── test_game_logic.py
│   └── test_database.py
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 🛠️ Setup

### 1) Requirements

* Python **3.10+**
* PostgreSQL **13+**
* Virtual environment recommended

### 2) Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3) Configure Database

Set a `DATABASE_URL` environment variable, or create a `.env` file:

```ini
DATABASE_URL=postgresql://user:password@localhost:5432/ludo_db
```

Initialize schema:

```bash
python -c "import database; database.Database().init_schema()"
```

### 4) Run the Game

```bash
python main.py
```

---

## 🎨 CLI Styling (Presentation-Ready)

For Project Week, the CLI is styled using [**rich**](https://rich.readthedocs.io/):

* Color-coded players (`Red`, `Blue`, `Green`, `Yellow`)
* Token states shown in **tables**
* Decorative **banners** and **status messages**
* Optional interactive menus (via `inquirer`)

---

## ✅ Running Tests

We use `pytest`:

```bash
pytest -q
```

Database tests are skipped automatically if `DATABASE_URL` is not set.

---

## 👥 Team & Branch Mapping

* **LB-9 🎲 Game Logic (Najma):** `game_logic.py`, `utils/`
* **LB-10 🧠 Database (Maina):** `database.py`
* **LB-11 🎯 Player Management (Evalyne):** `players.py`
* **LB-12 🧪 Testing (Adrian):** `tests/`
* **LB-13 🔀 Integration (Everyone):** `main.py`
* **LB-14 🎮 Winning Logic (Najma):** `game_logic.py`

---

## 🏁 MVP Goal

* Playable **console-based Ludo game**
* 2–4 players
* Save/load functionality with PostgreSQL
* Fully tested and interactive

---

## 🔮 Future Enhancements

* Capture & safe-square rules
* Graphical TUI with `rich` grids
* GitHub Actions for CI/CD
* Online multiplayer (stretch goal)
