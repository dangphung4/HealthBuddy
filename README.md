# HealthBuddy

Hey there! Welcome to HealthBuddy, your personal health assistant. It's like having a doctor in your pocket, ready to chat with you anytime, in several languages. We're using some pretty neat AI to make sure your buddy can chat back with audio and even sync its lips to the conversation.

## Features

- **Multilingual Support**: Your HealthBuddy speaks multiple languages.
- **Realistic Interactions**: Not only does it talk back, but it also moves its lips to make the chat feel more real.
- **Voice-Powered**: Just talk to it, and it'll respond right back to you.

## Tech Stack

- **Frontend**: Built with React and powered by Vite for speedy interactions.
- **Backend**: Runs on FastAPI, which keeps things running smoothly.
- **AI Tools**: Uses Synthesia AI for lip-sync animations and Google Cloud Text-to-Speech for clear and natural voice responses.

## Project Layout

Here’s how we’ve organized the project:

```
/healthbuddy
|-- /frontend          # React stuff happens here
|-- /backend           # FastAPI handles the backend
|-- /docs              # Documentation
|-- README.md
```

## Setup Guide

### Prerequisites

- Node.js
- Python 3.8+
- Git

### Installation

#### Clone the Repository

```bash
git clone https://github.com/yourusername/healthbuddy.git
cd healthbuddy
```

#### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

#### Backend Setup

```bash
cd ../backend
pip install -r requirements.txt
uvicorn main:app --reload
OR
fastapi dev main.py
OR
fastapi run
```

## Configuration

Make sure to configure the necessary API keys:

- `SYNTHESIA_API_KEY`: Your API key for Synthesia AI
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your Google Cloud service account key

## Usage

Start the frontend and backend as described above, and head over to `http://localhost:3000` to chat with your HealthBuddy.

## Contribute

Interested in making HealthBuddy better? We love your input! We want to make contributing to this project as easy and transparent as possible.

## License

HealthBuddy is open source software licensed as MIT. The license is available in the [LICENSE.md](LICENSE.md) file in our repo.

## Thanks

- Cheers to Synthesia AI and Google Cloud Text-to-Speech for the tech that makes HealthBuddy come alive.

---
