#  Comparative Transcription Service

This FastAPI-based microservice compares **diarized transcriptions** with categorized real-estate keywords and returns structured, speaker-specific matches. It supports keyword management via API and integrates **PostgreSQL** for keyword storage.

---

##  Features

-  Compare diarized text (speaker-wise) with categorized keywords
-  Organize matches by category and speaker (Agent/Customer)
-  Keywords are fetched dynamically from PostgreSQL (`keywords` table)
-  REST APIs to Add / Delete keywords by category
-  Logs activity and handles exceptions gracefully

---

##  Tech Stack

- **Python 3.10+**
- **FastAPI** – Web framework for APIs
- **PostgreSQL** – Primary database
- **SQLAlchemy** – ORM for DB access
- **Uvicorn** – ASGI server for FastAPI

---

##  Database Schema

### `keywords` Table

| Column   | Type   | Description                             |
|----------|--------|-----------------------------------------|
| id       | SERIAL | Primary Key                             |
| category | TEXT   | Category name (e.g. Financial Details)  |
| keyword  | TEXT   | The keyword itself (e.g. SBI)           |

```sql
CREATE TABLE keywords (
    id SERIAL PRIMARY KEY,
    category TEXT NOT NULL,
    keyword TEXT NOT NULL
);
 Setup Instructions
Clone the Repository

bash

git clone https://github.com/your-org/comparative-transcription.git
Create a virtual environment & install dependencies

bash

1. python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
Configure Environment Variables
Create a .env file based on .env.example with your DB credentials.

Run the FastAPI App
bash

uvicorn main:app --reload

View API Docs
Open your browser and go to:
http://localhost:8000/docs

Project Structure

app/
├── main.py               # FastAPI routes and logic
├── models.py             # SQLAlchemy ORM models
├── database.py           # DB session and engine setup
├── requirements.txt      # Project dependencies
├── .env.example          # Sample env file
└── README.md             # Documentation (this file)

 API Endpoint Documentation
 GET /Match_keywords/{conversation_id}
Purpose:
Analyze diarized conversation by conversation_id and return matched keywords organized by category and speaker.
Workflow:

Fetches diarized segments from the Transcription table
Loads keywords from the keywords table in DB
Compares each keyword against speaker text
Tracks match count and spoken text
Returns structured output

Sample Response:
{
  "agent_id": "agent_123",
  "conversation_id": "conv_001",
  "project_id": "proj_456",
  "builder_name": "ABC Builders",
  "matched_Keywords": [
    {
      "category": "Property Types",
      "keywords": [
        {
          "keyword": "villa",
          "countBySpeaker": {
            "Agent": { "count": 1, "text": ["This is a villa."] },
            "Customer": { "count": 0, "text": [] }
          }
        }
      ]
    }
  ],
  "diarized_text": [...]
}

## GET /Show_keywords
Purpose:
List all keywords in the database grouped by category.
Workflow:

Fetches all rows from the keywords table
Groups keywords by category
Returns them as structured JSON
Sample Response:

{
  "keywords": {
    "Property Types": ["villa", "plots"],
    "Communication & Tools": ["whatsapp", "browser"]
  }
}

#POST/Add_keywords
Purpose:
Add a new keyword to a specific category.
Sample Request Body:

{
  "category": "Location & Accessibility",
  "keyword": "siruseri"
}
Behavior:

Checks if the keyword already exists (case-insensitive)
If not found, inserts into the keywords table
Returns a success message
Sample Response:
{
  "message": "Keyword added successfully."
}

## DELETE /Delete_keywords
Purpose:
Delete a keyword from a specific category.
Sample Request Body:

{
  "category": "Communication & Tools",
  "keyword": "whatsapp"
}
Behavior:
Locates the keyword (case-insensitive) in the category
Deletes the row if it exists
Returns a success message

Sample Response:

{
  "message": "Keyword deleted successfully."
}

Notes
All keyword management endpoints (POST, DELETE, GET) work directly with the PostgreSQL keywords table.
Error handling is in place for missing data and invalid inputs.
