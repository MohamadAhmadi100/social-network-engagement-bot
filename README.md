# Social Network Engagement Bot

This project implements a social network engagement bot that monitors Instagram profiles, tracks follower counts, and sends milestone alerts via a Telegram bot.

## Features

- RESTful API built with FastAPI
- PostgreSQL database integration with SQLAlchemy
- Real Instagram Graph API call to fetch follower count
- Background task that monitors profiles and sends Telegram notifications when milestones are reached
- Basic authentication on API endpoints
- Bonus: Top follower insights for the last 24 hours
- Dockerized with Docker and Docker Compose
- Tests written with pytest

## Setup

1. Create a `.env` file (or use docker-compose environment variables) with:

```bash
DATABASE_URL=postgresql://user:password@db:5432/social_engagement
INSTAGRAM_ACCESS_TOKEN=INSTAGRAM_ACCESS_TOKEN
INSTAGRAM_USER_ID=INSTAGRAM_USER_ID
TELEGRAM_BOT_TOKEN=TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID=TELEGRAM_CHAT_ID
BASIC_AUTH_USERNAME=admin
BASIC_AUTH_PASSWORD=admin
MILESTONE_THRESHOLD=1000
```

2. Build and run using Docker Compose:

```bash
docker-compose up --build
```

3. The API will be available on http://localhost:8000

## Running Mock APIs

For testing without real API dependencies, you can run the following mocked services:
1.	Mock Instagram API

Run:
```bash
uvicorn app.mock.mock_instagram_api:app --host 0.0.0.0 --port 8001
```

2. Mock Telegram API

Run:
```bash
uvicorn app.mock.mock_telegram_api:app --host 0.0.0.0 --port 8002
```

This service simulates sending Telegram messages.

Make sure MOCK is set to True so that the application uses these mocked endpoints.

## Running Tests
```bash
pytest
```