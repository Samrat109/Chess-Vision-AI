# ♟️ ChessVision AI

**AI-Powered Chess Analysis and Game Review Platform**

ChessVision AI is a chess analysis platform designed to help players understand chess positions, explore candidate moves, and review saved games using the Stockfish chess engine.

The project combines a Django backend, Python-based chess analysis, and a Chrome browser extension to provide an interactive chess analysis experience.

---

## 🚀 Features

- **Chess Position Analysis:** Analyze chess positions using the Stockfish engine.
- **Candidate Moves:** Explore suggested moves and their evaluations.
- **Position Evaluation:** View centipawn scores and mate-in-N evaluations when available.
- **Principal Variation:** Explore possible continuation lines.
- **Saved Game Review:** Retrieve and review previously saved chess games.
- **Django Dashboard:** Access chess analysis through a web interface.
- **Chrome Extension:** Access analysis features through a browser popup.
- **Progressive Web App (PWA):** Includes a web app manifest, application icons, and service worker setup.
- **REST API:** Communicate with the Django backend through API endpoints.

> ChessVision AI is intended for completed-game analysis, study positions, and permitted training activities.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Backend | Python, Django |
| API | Django REST Framework |
| Chess Engine | Stockfish |
| Frontend | HTML, CSS, JavaScript |
| Browser Extension | Chrome Extension Manifest V3 |
| Database | SQLite |
| Version Control | Git, GitHub |
| Deployment Target | AWS EC2, Ubuntu, Nginx, Gunicorn |
| Web App | Progressive Web App (PWA) |

---

## 📁 Project Structure

```text
chessvision-ai/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── games/
│   ├── migrations/
│   ├── templates/
│   │   └── games/
│   │       └── dashboard.html
│   ├── static/
│   │   └── games/
│   │       ├── icons/
│   │       ├── manifest.webmanifest
│   │       └── service-worker.js
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── predictions/
│
├── players/
│
├── chessvision-extension/
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.js
│   ├── content.js
│   └── icons/
│
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
└── db.sqlite3
```

*The structure above describes the intended project layout. Some files may differ depending on your current implementation.*

---

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd chessvision-ai
```

### 2. Create a Python virtual environment

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If Stockfish is not installed:

```bash
sudo apt update
sudo apt install stockfish
```

Verify:

```bash
stockfish
```

Type `quit` to exit.

### 4. Configure environment variables

Generate a Django secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Set your local environment variables:

```bash
export DJANGO_SECRET_KEY='YOUR_GENERATED_SECRET_KEY'
export DJANGO_DEBUG=True
export DJANGO_ALLOWED_HOSTS='127.0.0.1,localhost'
```

Never commit your secret key to GitHub.

### 5. Run database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Check the Django application

```bash
python manage.py check
```

### 7. Start the development server

```bash
python manage.py runserver 8001
```

Open your browser:

```text
http://127.0.0.1:8001/
```

---

## 🔌 API Endpoints

The Django backend exposes REST API endpoints for chess analysis and saved-game retrieval.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/positions/predict/` | Analyze a chess position |
| GET | `/api/positions/games/<game_id>/` | Retrieve saved game details |
| GET | `/api/positions/games/<game_id>/position/<ply>/` | Retrieve analysis for a game position |

### Example: Analyze a Chess Position

**Request:**

```http
POST /api/positions/predict/
Content-Type: application/json
```

**Example request body:**

```json
{
    "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
}
```

The API analyzes the submitted position and returns candidate moves and evaluation information according to the backend response format.

---

## 🌐 Chrome Extension Setup

ChessVision AI includes a Chrome extension for accessing analysis features through a browser popup.

### Installation

1. Open Google Chrome.
2. Navigate to:

```text
chrome://extensions/
```

3. Enable **Developer mode**.
4. Click **Load unpacked**.
5. Select the `chessvision-extension` directory.
6. Open the ChessVision AI extension.

### Backend Connection

For local development, the extension connects to:

```javascript
const BASE_URL = "http://127.0.0.1:8001";
```

For production, update this to your deployed HTTPS domain.

---

## 📱 Progressive Web App (PWA)

ChessVision AI includes PWA components to support an installable web experience.

Current PWA components:

Web app manifest.

Application icons (192×192 and 512×512).

Service worker.

Standalone display configuration.

For installation on supported devices, deploy the application over HTTPS.

☁️ Deployment

The planned production architecture uses:

                 Users
                   |
                   v
              HTTPS / DNS
                   |
                   v
                AWS EC2
                   |
                   v
                 Nginx
                   |
                   v
                Gunicorn
                   |
                   v
              Django Backend
                   |
             +-----+-----+
             |           |
             v           v
          Stockfish    Database

Planned deployment technologies:

AWS EC2

Ubuntu Server

Nginx

Gunicorn

Stockfish

HTTPS / SSL

PostgreSQL for future database scaling

🔒 Security

Keep Django's production secret key outside the source code.

Set DEBUG=False in production.

Configure ALLOWED_HOSTS correctly.

Use HTTPS for production.

Never commit .env, private keys, or credentials.

Restrict SSH access to trusted IP addresses.

Do not expose the Django development server publicly.

🧪 Testing

Run Django system checks:

python manage.py check

Run automated tests:

python manage.py test

🗺️ Future Improvements

Interactive chessboard with move navigation.

Complete PGN import and game review.

Improved chess position visualization.

Opening and endgame analysis.

User authentication and game history.

Analysis reports and downloadable PGN files.

Responsive mobile-first dashboard.

Cloud deployment and production monitoring.

PostgreSQL database integration.

Improved PWA offline experience.

🎯 Project Goal

The goal of ChessVision AI is to build an accessible chess analysis platform that helps players study positions, review completed games, and improve their understanding of chess through engine-powered analysis.

👨‍💻 Author

Samrat Gaikwad

GitHub: Samrat109