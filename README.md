# Real Estate Analysis Chatbot

A full-stack web application built with React and Django that provides real estate market analysis for localities in Pune, India. The chatbot processes Excel data and provides insights, charts, and detailed tables based on user queries.

## Features

- **Natural Language Queries**: Ask questions about real estate trends in plain English
- **AI-Powered Summaries**: Optional OpenAI integration for intelligent market analysis
- **Interactive Charts**: Visualize price trends and demand patterns with Chart.js
- **Detailed Data Tables**: View comprehensive real estate data filtered by locality
- **Comparison Analysis**: Compare multiple localities side-by-side
- **Responsive UI**: Modern Bootstrap-based chat interface

## Tech Stack

### Backend (Django)
- Django 5.2.8
- Django REST Framework
- pandas & openpyxl for Excel processing
- django-cors-headers for CORS support
- OpenAI API (optional) for enhanced summaries

### Frontend (React)
- React 19.2.0
- Bootstrap 5 for styling
- Chart.js & react-chartjs-2 for data visualization
- Axios for API communication

## Project Structure

```
.
├── backend/
│   ├── api/
│   │   ├── data_processor.py    # Excel data processing logic
│   │   ├── views.py              # API endpoints
│   │   └── urls.py               # URL routing
│   ├── backend/
│   │   ├── settings.py           # Django configuration
│   │   └── urls.py               # Main URL configuration
│   ├── data/
│   │   └── real_estate_data.xlsx # Real estate dataset
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatInterface.js  # Main chat UI component
│   │   │   └── ChartComponent.js # Chart rendering component
│   │   ├── App.js                # Root component
│   │   └── index.js
│   ├── package.json
│   └── .env                      # Environment variables
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 20+
- npm

### Backend Setup

1. Install Python dependencies:
```bash
pip install django djangorestframework django-cors-headers pandas openpyxl
```

2. Run migrations:
```bash
cd backend
python manage.py migrate
```

3. Start the Django server:
```bash
python manage.py runserver 0.0.0.0:8000
```

The backend API will be available at `http://127.0.0.1:8000/api/`

### Frontend Setup

1. Install Node dependencies:
```bash
cd frontend
npm install
```

2. Configure the backend URL (optional):
Create a `.env` file in the `frontend` directory:
```env
PORT=5000
DANGEROUSLY_DISABLE_HOST_CHECK=true
WDS_SOCKET_PORT=0
REACT_APP_BACKEND_URL=http://127.0.0.1:8000
```

3. Start the React development server:
```bash
PORT=5000 DANGEROUSLY_DISABLE_HOST_CHECK=true npm start
```

The frontend will be available at `http://localhost:5000`

**Note:** The `REACT_APP_BACKEND_URL` environment variable allows you to configure the backend API URL for different environments (development, staging, production). If not set, it defaults to `http://127.0.0.1:8000`.

## API Endpoints

### GET `/api/health/`
Health check endpoint to verify API is running.

**Response:**
```json
{
  "status": "ok",
  "message": "Real Estate Analysis API is running"
}
```

### GET `/api/localities/`
Get list of all available localities in the dataset.

**Response:**
```json
{
  "localities": ["Akurdi", "Ambegaon Budruk", "Aundh", "Wakad"]
}
```

### POST `/api/analyze/`
Analyze real estate data based on user query.

**Request:**
```json
{
  "query": "Analyze Wakad"
}
```

**Response:**
```json
{
  "summary": "Real estate analysis for Wakad (2020-2024): The average flat rate is currently ₹10,278 per sqft. Price growth over the period is 12.7%. Total units sold: 24,071. Strong appreciation observed...",
  "chart_data": {
    "type": "price_trend",
    "data": [
      {
        "year": 2020,
        "avg_flat_rate": 9116.95,
        "avg_office_rate": 11083.54,
        "avg_shop_rate": 13904.59
      },
      ...
    ]
  },
  "table_data": [
    {
      "year": 2020,
      "total_sales": "₹20,983,019,240",
      "total_sold": 3521,
      "flat_avg_rate": "₹9,117",
      ...
    },
    ...
  ],
  "localities": ["Wakad"]
}
```

## Sample Queries

Try asking the chatbot:

- **Single Locality Analysis**
  - "Give me analysis of Wakad"
  - "Show price growth for Akurdi over the last 3 years"
  - "What's the demand trend in Aundh?"

- **Comparison Queries**
  - "Compare Ambegaon Budruk and Aundh demand trends"
  - "Compare Wakad and Akurdi price growth"

## OpenAI Integration (Optional)

To enable AI-powered summaries, set the `OPENAI_API_KEY` environment variable:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Without the API key, the application will use intelligent mock summaries based on data analysis.

## Data

The application uses real estate data for Pune localities including:
- Year-wise price trends (2020-2024)
- Sales volumes and transaction data
- Property type breakdowns (flats, offices, shops)
- Average rates per square foot
- Total units and carpet area supplied

## Development

### Running Both Servers Simultaneously

**Terminal 1 (Backend):**
```bash
cd backend && python manage.py runserver 0.0.0.0:8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend && PORT=5000 DANGEROUSLY_DISABLE_HOST_CHECK=true npm start
```

### Testing the API

Test health endpoint:
```bash
curl http://127.0.0.1:8000/api/health/
```

Test analysis endpoint:
```bash
curl -X POST http://127.0.0.1:8000/api/analyze/ \
  -H "Content-Type: application/json" \
  -d '{"query": "Analyze Wakad"}'
```

## Deployment

The application can be deployed to platforms like:
- **Frontend**: Vercel, Netlify
- **Backend**: Render, Heroku, Railway
- **Full-stack**: Replit, DigitalOcean App Platform

## License

MIT License

## Assignment Details

This project was created as part of the Sigmavalue Full Stack Developer Assignment. It demonstrates:
- Clean code structure and readability
- Seamless UI/UX and backend integration
- Accurate Excel data processing
- Clear and informative chart visualizations
- LLM integration for intelligent summaries
