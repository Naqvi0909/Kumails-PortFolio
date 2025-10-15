# MedCore HMS

Hospital Management System built with Flask

## Description

MedCore HMS is a web-based Hospital Management System designed to streamline hospital operations and patient care management.

## Features

- RESTful API endpoints
- Health check monitoring
- Scalable architecture
- Production-ready with Gunicorn

## Installation

The project uses Python 3.11 and Flask. Dependencies are managed automatically in the Replit environment.

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server
python main.py
```

### Production Deployment

The application uses Gunicorn for production:

```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

## API Endpoints

- `GET /` - Welcome message and system status
- `GET /health` - Health check endpoint
- `GET /api/info` - Application information

## Project Structure

```
.
├── main.py           # Flask application entry point
├── requirements.txt  # Python dependencies
├── .gitignore       # Git ignore patterns
└── README.md        # Project documentation
```

## Environment Variables

- `PORT` - Server port (default: 5000)
- `REPLIT_DEPLOYMENT_ENV` - Deployment environment

## Technology Stack

- **Framework**: Flask 3.1.2
- **Server**: Gunicorn 23.0.0
- **Python**: 3.11

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
