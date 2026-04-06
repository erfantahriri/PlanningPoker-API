# PlanningPoker API

Django + Django Channels back-end for the PlanningPoker application — real-time planning sessions for scrum/agile teams.

## Features

- Room management: create, join, and update rooms with optional password protection
- Participant roles: **Dev**, **Designer**, **PM**, **EM** (plus legacy Voter/Spectator) with per-role voting permissions
- Card sets: Standard, Fibonacci, T-Shirt Sizes
- Real-time updates over WebSocket (Django Channels + Redis)
- Issue management: create, rename, delete, set current issue
- Voting: submit votes, flip cards, reset board
- Session summary: public endpoint with full issue/vote history
- Voting timer and emoji reactions over WebSocket

## Quick Start (Docker)

The easiest way to run everything together is with Docker Compose from the repo root:

```sh
docker compose up --build
```

This starts PostgreSQL, Redis, the API (on port 8000), and the front-end (on port 3000).

## Manual Setup

### Requirements

- Python 3.9+
- PostgreSQL
- Redis

### Environment variables

```sh
export PLANNING_POKER_DB_NAME='planningpoker'
export PLANNING_POKER_DB_USER='postgres'
export PLANNING_POKER_DB_PASSWORD='postgres'
export PLANNING_POKER_DB_HOST='127.0.0.1'
export PLANNING_POKER_DJANGO_SECRET_KEY='your-secret-key'
export PLANNING_POKER_JWT_SECRET_KEY='your-jwt-secret'
export PLANNING_POKER_SUID_ALPHABET='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
export REDIS_HOST='localhost'
export DJANGO_SETTINGS_MODULE='planningpoker.settings'
```

### Run

```sh
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
daphne -b 0.0.0.0 -p 8000 planningpoker.routing:application
```

API is available at `http://localhost:8000`. Docs at `http://localhost:8000/swagger/` (Swagger UI) or `http://localhost:8000/redoc/` (ReDoc).

## API Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/v1/rooms/` | List / create rooms |
| POST | `/v1/rooms/:uid/join` | Join a room |
| GET | `/v1/rooms/:uid/info` | Public room info |
| GET | `/v1/rooms/:uid/summary` | Public session summary |
| PATCH | `/v1/rooms/:uid` | Update room title / card set |
| GET | `/v1/rooms/:uid/participants` | List participants |
| PATCH | `/v1/rooms/:uid/participants/:uid` | Update own name or any participant's role |
| GET/POST | `/v1/rooms/:uid/issues` | List / create issues |
| GET/PATCH/DELETE | `/v1/rooms/:uid/issues/:uid` | Get / update / delete issue |
| GET/POST | `/v1/rooms/:uid/current_issue` | Get / set current issue |
| GET/POST/DELETE | `/v1/rooms/:uid/issues/:uid/votes` | Get / submit / reset votes |
| POST | `/v1/rooms/:uid/issues/:uid/votes/flip` | Flip vote cards |

## Related

- [PlanningPoker-Front](https://github.com/erfantahriri/PlanningPoker-Front)

## License

GPL-3.0
