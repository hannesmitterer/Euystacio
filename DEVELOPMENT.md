# Euystacio Development Setup

This document explains how to run the Euystacio project locally after the recent restructuring.

## Overview

The repository now supports both Flask and FastAPI backends:
- **Flask app** (`app.py`): Main emotional rhythm interface with pulses, reflections, and tutor nomination
- **FastAPI app** (`main.py`): Lightweight API bridge with manifesto and chat endpoints

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Running Locally

#### Option 1: Flask App Only
```bash
python app.py
```
The Flask app will be available at `http://localhost:5000`

#### Option 2: FastAPI App Only
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
The FastAPI app will be available at `http://localhost:8000`

#### Option 3: Both Apps with Docker Compose
```bash
docker-compose up
```
This will start:
- Flask app on port 5000
- FastAPI app on port 8000
- Nginx reverse proxy on port 8080

## Project Structure

```
.
├── app.py                      # Flask application
├── main.py                     # FastAPI application
├── red_code.py                 # RED_CODE state management (top-level)
├── reflector.py                # Reflection logic (top-level)
├── tutor_nomination.py         # Tutor nomination system (top-level)
├── sentimento_pulse_interface.py  # Pulse interface
├── red_code.json               # Current RED_CODE state
├── red_code.example.json       # Example RED_CODE structure
├── requirements.txt            # Python dependencies
├── docker-compose.yml          # Docker Compose configuration
├── nginx.conf                  # Nginx reverse proxy config
└── templates/                  # Flask templates
    └── index.html
```

## API Endpoints

### Flask App (`app.py`)
- `GET /` - Serve main interface
- `GET /api/red_code` - Get RED_CODE state
- `GET /api/pulses` - Get all pulses
- `GET /api/reflect` - Run reflection
- `GET /api/reflections` - Get all reflections
- `GET /api/tutors` - Get tutor list
- `POST /api/pulse` - Submit a pulse

### FastAPI App (`main.py`)
- `GET /` - API info
- `GET /ping` - Health check
- `GET /manifesto` - Get manifesto
- `POST /chat/send` - Send chat message
- `GET /chat/log` - Get chat history

## Development Notes

### Module Changes
The imports have been restructured to use top-level modules:
- `from red_code import RED_CODE, ensure_red_code`
- `from reflector import reflect_and_suggest`
- `from tutor_nomination import TutorNomination`

### Auto-initialization
The Flask app now automatically:
- Creates `red_code.json` if missing (via `ensure_red_code()`)
- Creates `logs/` directory
- Creates `tutors.json` with default tutors

## Production Deployment

For production, consider:
1. **Choose one backend** or use both behind a reverse proxy
2. **Use gunicorn for Flask**: `gunicorn app:app -b 0.0.0.0:5000`
3. **Use uvicorn for FastAPI**: `uvicorn main:app --host 0.0.0.0 --port 8000`
4. **Configure nginx** to route requests appropriately (see `nginx.conf`)

## License

See `SACRED_COMMONS_LICENSE.md` for licensing information.
