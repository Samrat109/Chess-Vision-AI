# Contributing to ChessVision AI ♟️

Thank you for your interest in contributing to **ChessVision AI**!

We welcome contributions from developers, chess enthusiasts, testers, and open-source contributors who want to improve the platform.

Whether you are fixing a bug, improving the interface, adding a feature, or updating documentation, your contribution is appreciated.

---

## 📌 Table of Contents

- [About the Project](#about-the-project)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Branching Strategy](#branching-strategy)
- [Coding Guidelines](#coding-guidelines)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [Security Guidelines](#security-guidelines)
- [Code of Conduct](#code-of-conduct)

---

## ♟️ About the Project

ChessVision AI is an AI-powered chess analysis and game review platform built using Python, Django, Django REST Framework, and Stockfish.

The project aims to help players study chess positions, explore candidate moves, and review completed games.

### Main Technologies

- Python
- Django
- Django REST Framework
- Stockfish Chess Engine
- HTML, CSS, JavaScript
- SQLite
- Chrome Extension
- Progressive Web App (PWA)

---

## 🤝 How to Contribute

You can contribute in several ways:

- Report bugs and technical issues.
- Suggest new features and improvements.
- Improve the user interface and user experience.
- Optimize Python and Django code.
- Improve chess analysis functionality.
- Add or improve automated tests.
- Improve project documentation.
- Help with deployment and performance optimization.

---

## ⚙️ Development Setup

### 1. Fork the Repository

Fork the ChessVision AI repository to your GitHub account.

### 2. Clone Your Fork

```bash
git clone YOUR_FORK_REPOSITORY_URL
cd chessvision-ai
```

### 3. Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Install Stockfish

On Ubuntu:

```bash
sudo apt update
sudo apt install stockfish
```

### 6. Configure Environment Variables

Generate a Django secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Set the environment variables:

```bash
export DJANGO_SECRET_KEY='YOUR_SECRET_KEY'
export DJANGO_DEBUG=True
export DJANGO_ALLOWED_HOSTS='127.0.0.1,localhost'
```

Never commit secrets or credentials.

### 7. Run Database Migrations

```bash
python manage.py migrate
```

### 8. Start the Development Server

```bash
python manage.py runserver 8001
```

Open:

```text
http://127.0.0.1:8001/
```

---

## 🌿 Branching Strategy

Create a separate branch for every feature or bug fix.

Examples:

```bash
git checkout -b feature/improve-chess-analysis
```

```bash
git checkout -b fix/api-validation-error
```

```bash
git checkout -b docs/update-readme
```

Avoid making changes directly to the main branch.

---

## 💻 Coding Guidelines

Please follow these guidelines when contributing:

### Python and Django

- Follow PEP 8 Python coding conventions.
- Write readable and maintainable code.
- Use meaningful variable and function names.
- Keep Django views and business logic organized.
- Validate API input before processing.
- Handle exceptions appropriately.
- Avoid unnecessary changes to existing application logic.

### JavaScript

- Use clear and descriptive function names.
- Avoid unnecessary global variables.
- Handle API errors properly.
- Keep browser extension functionality separate from Django backend logic.

### General Guidelines

- Keep changes focused and small.
- Avoid adding unnecessary dependencies.
- Update documentation when functionality changes.
- Do not commit generated files, virtual environments, or sensitive information.

---

## 📝 Commit Message Guidelines

Use clear and descriptive commit messages.

Recommended format:

```text
type: short description
```

Examples:

```bash
git commit -m "feat: add chess position analysis"
```

```bash
git commit -m "fix: resolve invalid FEN validation"
```

```bash
git commit -m "docs: update installation instructions"
```

Suggested commit types:

| Type | Purpose |
|---|---|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation changes |
| refactor | Code restructuring |
| test | Adding or updating tests |
| perf | Performance improvements |
| chore | Maintenance tasks |

---

## 🔀 Pull Request Guidelines

Before submitting a pull request:

1. Make sure your changes work locally.
2. Run Django system checks.
3. Run relevant automated tests.
4. Update documentation if necessary.
5. Review your code for unnecessary changes.
6. Push your feature branch to your fork.

Run checks:

```bash
python manage.py check
```

Run tests:

```bash
python manage.py test
```

Push your branch:

```bash
git push origin feature/your-feature-name
```

Then:

1. Open the original GitHub repository.
2. Select **New Pull Request**.
3. Select your feature branch.
4. Explain what you changed and why.
5. Include screenshots when relevant.
6. Submit your pull request for review.

### Pull Request Description Template

Please include:

- What problem does this change solve?
- What changes were made?
- How was the change tested?
- Are there any breaking changes?
- Are screenshots or additional documentation available?

---

## 🐛 Reporting Bugs

If you discover a bug, open a GitHub Issue.

Include:

- A clear issue title.
- Steps to reproduce the problem.
- Expected behavior.
- Actual behavior.
- Error messages or screenshots.
- Operating system and Python version.
- Relevant Django logs, excluding secrets and personal information.

Please check existing issues before creating a duplicate.

---

## 💡 Suggesting Features

We welcome suggestions that improve ChessVision AI.

Some areas of interest include:

- Improved chess position evaluation.
- Better candidate move visualization.
- PGN import and game review.
- Opening and endgame analysis.
- Interactive chessboard improvements.
- Mobile-friendly interface.
- PWA improvements.
- Backend performance optimization.
- Better API documentation.

Before implementing a large feature, open an issue to discuss the proposed approach.

---

## 🔒 Security Guidelines

Security is important for ChessVision AI.

Please follow these rules:

- Never commit Django secret keys.
- Never upload passwords, API tokens, or private keys.
- Do not include `.env` files in commits.
- Validate user input.
- Avoid exposing sensitive server information.
- Report security vulnerabilities privately to the project maintainer rather than publishing exploit details.

---

## 📜 Code of Conduct

All contributors are expected to:

- Be respectful and professional.
- Welcome different experience levels and perspectives.
- Provide constructive feedback.
- Avoid harassment and discrimination.
- Focus discussions on improving the project.

We want ChessVision AI to be a welcoming environment for everyone.

---

## ⭐ Thank You!

Thank you for helping improve **ChessVision AI**.

Every contribution, whether a bug report, documentation update, feature suggestion, or code improvement, helps make the project better.

Happy Coding and Happy Chess! ♟️
