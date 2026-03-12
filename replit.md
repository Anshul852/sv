# ScholarMind — Privacy-First AI Academic Scheduler

## Overview

Full-stack academic scheduling app with a SvelteKit frontend and Python FastAPI backend.
Source code ported from [github.com/Anshul852/sv](https://github.com/Anshul852/sv).

## Architecture

```
artifacts/scholarmind/     # SvelteKit frontend (port 22748, served at /)
artifacts/api-server/      # Express proxy → Python FastAPI backend (port 8080, served at /api)
backend/                   # Python FastAPI backend (port 8000, internal)
```

## Stack

- **Frontend**: SvelteKit 2, Svelte 4, Tailwind CSS 4, TypeScript
- **Backend**: Python FastAPI, Uvicorn, Pydantic, Passlib (JWT auth)
- **Database**: Supabase (PostgreSQL) — requires SUPABASE_URL / SUPABASE_KEY env vars
- **AI Agents**: Q-Learning (browser), Multi-Armed Bandit
- **Security**: AES-256 client-side encryption, JWT tokens, IndexedDB offline-first

## Routes (Frontend)

- `/` — Landing page
- `/dashboard` — Dashboard with widgets (cognitive load, study plan, schedule)
- `/study` — Study sessions
- `/sessions` — Session history
- `/deep-work` — Deep work session tracker
- `/schedule` — Academic schedule + calendar sync
- `/profile` — Student profile
- `/chat` — AI chatbot
- `/ai` — AI features
- `/rooms` — Silent study rooms
- `/vault` / `/privacy-vault` — Encrypted data vault
- `/settings` — Settings (connectors, theme)
- `/import` — Import syllabus
- `/login` / `/register` — Auth pages

## API Endpoints (Backend FastAPI)

- `POST /api/auth/*` — Authentication (login, register, device pairing)
- `GET/PUT /api/students/*` — Student profile & dashboard
- `GET/POST /api/study/*` — Study sessions, deep work
- `GET/POST /api/university/*` — LMS connections
- `GET /api/admin/*` — Admin panel (protected by ADMIN_TOKEN)
- `POST /api/sync/*` — Encrypted data sync
- `POST /api/chat/*` — AI chatbot

## Workflows

- `artifacts/scholarmind: web` — SvelteKit dev server
- `artifacts/api-server: API Server` — Express proxy to FastAPI
- `Python FastAPI Backend` — Python FastAPI at port 8000

## Environment Variables Needed

- `SUPABASE_URL` — Supabase project URL
- `SUPABASE_KEY` — Supabase anon key
- `SUPABASE_SERVICE_KEY` — Supabase service role key
- `SECRET_KEY` — JWT secret key
- `ADMIN_TOKEN` — Admin panel access token
