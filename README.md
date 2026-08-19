# Google Calendar Salary Calculator

A full-stack web application that connects to Google Calendar, identifies teaching sessions, matches them with configurable hourly course rates, and automatically calculates total teaching hours and earnings for a selected date range.

The project was built to replace manual salary calculations from calendar events with a simple automated workflow.

---

## Preview

<img width="1156" height="546" alt="dashboard" src="https://github.com/user-attachments/assets/4c5337fa-6e2c-4442-8661-870a9faf8ef9" />

<img width="1160" height="887" alt="Result" src="https://github.com/user-attachments/assets/5c0d12e7-be47-4301-aa4d-e28061c3906d" />

<img width="1080" height="634" alt="-2147483648_-210019" src="https://github.com/user-attachments/assets/f08a5cf6-82f3-4d99-a34e-5150da3ce27b" />

<img width="1080" height="627" alt="-2147483648_-210023" src="https://github.com/user-attachments/assets/9b79a306-0602-42d1-8e87-0f1567ade5f8" />

---

## Features

- Google OAuth authentication with read-only Google Calendar access
- Fetches events from the user's primary Google Calendar
- Custom date-range selection
- Configurable course codes and hourly rates
- Persistent course-rate storage using SQLite
- Automatic matching of calendar event titles with course rates
- Automatic session-duration calculation
- Earnings calculation for every matched session
- **Held-only filtering based on Google Calendar event colors**
  - **Sage** events represent classes that were held and are included in the calculation
  - **Tomato** events represent cancelled classes and are excluded
  - **Default-color** events represent classes that have not yet taken place and are excluded
- Displays:
  - Total teaching hours
  - Total number of sessions
  - Total calculated salary
  - Individual session earnings
- Optional event-title filtering
- Add, update, and delete course rates
- Responsive React interface

---

## How It Works

1. The user defines course codes and their corresponding hourly rates.

2. The user connects their Google account using Google OAuth with read-only Calendar permission.

3. The frontend receives a temporary Google access token.

4. The user selects a start date, end date, and optionally filters calendar events by title.

5. The **Held only** option controls which calendar events are considered:
   - When enabled, only **Sage-colored events** are processed as completed teaching sessions.
   - **Tomato-colored events** are treated as cancelled classes and ignored.
   - **Default-color events** are treated as sessions that have not yet taken place and are also ignored.

6. The frontend sends the calculation request to the FastAPI backend.

7. The backend loads the configured course rates from SQLite.

8. The backend uses the Google access token to retrieve events from the Google Calendar API.

9. Eligible calendar events are matched against configured course names.

10. Earnings are calculated for every matched session:

   ```text
   Session Earnings = Session Duration × Hourly Rate
   ```
11. The backend returns the total hours, number of completed sessions, total salary, and individual session details.
    
---

## Architecture

```text
┌──────────────────────────────┐
│        React Frontend        │
│                              │
│  Google OAuth                │
│  Course Rate Management      │
│  Date / Title Filters        │
│  Results Dashboard           │
└──────────────┬───────────────┘
               │
               │ HTTP / JSON
               ▼
┌──────────────────────────────┐
│        FastAPI Backend       │
│                              │
│  /courses                    │
│  /sessions/calculate         │
│  Calendar Service            │
└─────────┬───────────┬────────┘
          │           │
          ▼           ▼
┌──────────────┐  ┌──────────────────┐
│    SQLite    │  │ Google Calendar  │
│  SQLAlchemy  │  │       API        │
└──────────────┘  └──────────────────┘
```

---

## Tech Stack

### Frontend

- React
- JavaScript
- Axios
- Google OAuth
- Lucide React
- CSS

### Backend

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- Pydantic

### External Services

- Google OAuth 2.0
- Google Calendar API

---

## Project Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── db/
│   │   │   └── database.py
│   │   │
│   │   ├── models/
│   │   │   └── models.py
│   │   │
│   │   ├── routers/
│   │   │   ├── courses.py
│   │   │   └── sessions.py
│   │   │
│   │   ├── schemas/
│   │   │   └── schemas.py
│   │   │
│   │   ├── services/
│   │   │   └── calendar_service.py
│   │   │
│   │   └── main.py
│   │
│   ├── .env.example
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.css
│   │   ├── App.js
│   │   ├── index.css
│   │   └── index.js
│   │
│   ├── .env.example
│   ├── package.json
│   └── package-lock.json
│
├── .gitignore
└── README.md
```

---

## API Endpoints

### Course Rates

#### Get all course rates

```http
GET /courses/
```

Returns all configured course rates.

---

#### Create or update a course rate

```http
POST /courses/
```

Example request:

```json
{
  "course_name": "PY5",
  "hourly_rate": 200
}
```

If the course already exists, its hourly rate is updated.

---

#### Delete a course rate

```http
DELETE /courses/{course_id}
```

Deletes the course rate associated with the provided ID.

---

### Salary Calculation

```http
POST /sessions/calculate
```

Example request:

```json
{
  "google_token": "GOOGLE_ACCESS_TOKEN",
  "start_date": "2026-07-01",
  "end_date": "2026-07-31",
  "title_filter": null,
  "only_sage": true
}
```

Example response:

```json
{
  "summary": {
    "total_hours": 41,
    "total_salary": 7920,
    "total_sessions": 41
  },
  "sessions": [
    {
      "event_title": "PY5 - Example Session",
      "event_date": "2026-07-01T10:00:00Z",
      "duration_hours": 1,
      "hourly_rate": 200,
      "total_earnings": 200
    }
  ]
}
```

---

## Getting Started

### Prerequisites

Make sure the following are installed:

- Git
- Python
- Node.js
- npm

You will also need:

- A Google Cloud project
- Google Calendar API enabled
- A Google OAuth 2.0 Web Application Client ID

---

## 1. Clone the Repository

```bash
git clone https://github.com/shokufa/gcal-salary-calculator.git
cd gcal-salary-calculator
```

---

## 2. Backend Setup

Move into the backend directory:

```bash
cd backend
```

Create a virtual environment.

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the backend dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The backend will run at:

```text
http://localhost:8000
```

FastAPI's interactive API documentation is available at:

```text
http://localhost:8000/docs
```

---

## 3. Frontend Setup

Open another terminal and move into the frontend directory:

```bash
cd frontend
```

Install the frontend dependencies:

```bash
npm install
```

Create a `.env` file inside the `frontend` directory.

You can copy the provided `.env.example`.

### Windows

```bash
copy .env.example .env
```

### macOS / Linux

```bash
cp .env.example .env
```

Configure the environment variables:

```env
REACT_APP_GOOGLE_CLIENT_ID=your_google_oauth_client_id
REACT_APP_API_BASE_URL=http://localhost:8000
```

Start the React development server:

```bash
npm start
```

The frontend will run at:

```text
http://localhost:3000
```

---

## Google OAuth Configuration

Create an OAuth 2.0 Client ID from your Google Cloud project.

Use:

```text
Application type: Web application
```

For local development, add the following Authorized JavaScript Origin:

```text
http://localhost:3000
```

Make sure the **Google Calendar API** is enabled for the same Google Cloud project.

The application requests read-only Calendar access:

```text
https://www.googleapis.com/auth/calendar.readonly
```

This allows the application to retrieve calendar events without modifying or deleting them.

---

## Environment Variables

Real `.env` files should never be committed to Git.

The repository includes `.env.example` files to show the required environment variable names without exposing real configuration values.

Example frontend configuration:

```env
REACT_APP_GOOGLE_CLIENT_ID=your_google_oauth_client_id
REACT_APP_API_BASE_URL=http://localhost:8000
```

Make sure your real `.env` files are excluded through `.gitignore`.

---

## Salary Calculation Logic

Course rates are configured using course names or course codes.

For example:

```text
PY5 → $200/hour
AP3 → $160/hour
PY3 → $250/hour
```

When a Google Calendar event contains one of these course codes in its title, the application matches the event to the corresponding hourly rate.

For example:

```text
Event: PY5 - Example Student

Duration: 1 hour
Hourly Rate: $200

Earnings = 1 × $200
Earnings = $200
```

All matching sessions are processed and summed to generate the final salary calculation.

---

## Security & Privacy

- Authentication is handled through Google OAuth.
- The application requests read-only access to Google Calendar.
- Calendar access tokens are used to retrieve events during salary calculation.
- Real `.env` files are excluded from version control.
- Sensitive credentials should never be committed to GitHub.
- `.env.example` files contain placeholders only.

---

## Motivation

This project was created to automate a repetitive real-world task: manually reviewing teaching sessions in Google Calendar and calculating monthly earnings based on different hourly rates.

Instead of manually counting sessions and calculating each payment, the application retrieves the relevant calendar events and performs the calculations automatically.

It also served as a practical full-stack development project involving frontend/backend communication, authentication, databases, REST APIs, and integration with an external API.

---

## What I Learned

While building this project, I gained practical experience with:

- Building a full-stack application
- React state management
- Frontend and backend communication
- REST API design
- FastAPI routing
- SQLAlchemy ORM
- SQLite databases
- Google OAuth 2.0
- Google Calendar API integration
- Working with access tokens
- Environment variables
- CORS configuration
- Third-party API integration
- Error handling
- Separating application logic into routers, services, models, schemas, and database layers

---

## Future Improvements

Possible future improvements include:

- Production deployment
- User accounts and authentication
- PostgreSQL support for production
- Docker support
- Automated frontend and backend testing
- Exporting calculated salary reports
- CSV/PDF report generation
- Improved mobile responsiveness
- More advanced event filtering
- Configurable Google Calendar color mappings
- Historical salary reports
- Improved error handling and logging

---

## License

This project was created primarily as a portfolio and learning project.
