# InkLaunch - Self-Publishing Platform

A modern self-publishing platform built with **Python** and **MongoDB** that empowers authors to showcase their books, exchange peer reviews, and compete for monthly recognition with AI-powered book analysis.

## 🚀 Features

- **User Authentication**: Secure registration and login with role-based access (user/admin)
- **Book Management**: Upload and manage books with rich metadata
- **Peer Review System**: Exchange constructive feedback with fellow authors
- **AI Book Reviews**: GPT-4 powered multi-dimensional book analysis for competitions
- **Monthly Competition**: "Author of the Month" recognition program
- **Author Tools**: Metadata checker, ISBN validator
- **Resources**: Educational articles and publishing guides

## 🛠 Technology Stack

- **Backend**: Python 3.9+ with Flask
- **Database**: MongoDB (NoSQL)
- **AI**: OpenAI GPT-4 Turbo
- **Frontend**: HTML5, Bootstrap 5, JavaScript
- **Authentication**: JWT + Flask sessions

## Quick Start

\`\`\`bash
# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your MongoDB URI and API keys

# Run the application
python app.py
\`\`\`

Visit http://localhost:5000

## Testing

\`\`\`bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/
\`\`\`
