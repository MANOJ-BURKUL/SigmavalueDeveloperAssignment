Real Estate Analysis Chatbot

A full-stack project built using React (frontend) and Django REST Framework (backend).
The chatbot takes user queries like:

“Analyze Wakad”

“Compare Aundh and Ambegaon Budruk demand trends”

“Show price growth for Akurdi over the last 3 years”

…and returns:

 A natural-language summary
 A price/demand trend chart
 A filtered data table
 Locality detection & comparison
 Optional OpenAI-powered analysis

 project Structure
SigmavalueDeveloperAssignment/
│
├── backend/        # Django REST API
│   ├── backend/    # Django project folder
│   ├── api/        # Core API logic
│   ├── venv/       # Virtual environment (ignored)
│   └── manage.py
│
└── frontend/       # React application
    ├── src/
    ├── public/
    └── package.json

 Backend (Django) Setup
1 Navigate to backend folder
cd backend

2️ Activate virtual environment

Windows PowerShell:

.\venv\Scripts\activate


Git Bash / VSCode Terminal:

source venv/Scripts/activate

3️ Install dependencies
pip install -r requirements.txt

4️ Apply migrations
python manage.py migrate

5️ Start backend server
python manage.py runserver 8000


Backend will run at:

 http://127.0.0.1:8000/

API Root: http://127.0.0.1:8000/api/

 API Endpoints
Method	Endpoint	Description
GET	/api/health/	Returns API status
GET	/api/localities/	Returns all localities from Excel
POST	/api/analyze/	Returns summary, chart data, table data
 Sample POST (Thunder Client / Postman)

POST → http://127.0.0.1:8000/api/analyze/
Body → JSON:

{
  "query": "Analyze Wakad"
}

 Frontend (React) Setup
1️ Navigate to frontend folder
cd frontend

2️ Install dependencies
npm install

3️ Create .env file
REACT_APP_API_URL=http://127.0.0.1:8000/api

4️ Start frontend
npm start


Frontend runs at:

 http://localhost:3000

 Optional: Enable OpenAI Summaries

Add an environment variable in backend:

Windows PowerShell:

setx OPENAI_API_KEY "your_key_here"


Git Bash:

export OPENAI_API_KEY="your_key_here"


Backend now uses real LLM summaries.

 Features
 Locality extraction from free-text query
 Price trend chart
 Demand trend chart
 Summary using rules or OpenAI
 Multi-locality comparison
 Filtered table export
 Excel dataset parsing
 CORS enabled for frontend communication
 Deployment (Optional)
 Backend

Render.com

Railway.app

EC2 / VPS

Frontend

Vercel

Netlify

GitHub Pages

 How to Push to GitHub

From project root:

git add .
git commit -m "Initial commit - Real Estate Chatbot"
git push -u origin main

 Required Submission

 GitHub Repo
 Optional Live Demo
 1–2 Minute Demo Video showing:

Query input

Summary display

Chart rendering

Table filtering
