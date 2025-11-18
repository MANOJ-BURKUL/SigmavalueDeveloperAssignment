# Real Estate Analysis Chatbot

## Project Overview
A full-stack web application that provides AI-powered real estate market analysis for Pune localities. Built with React frontend and Django backend, featuring interactive charts, data tables, and natural language query processing.

## Recent Changes (November 18, 2025)

### Initial Implementation
- Created Django REST API backend with Excel data processing
- Implemented React frontend with Bootstrap chat interface
- Added Chart.js visualizations for price and demand trends
- Configured workflows for backend (port 8000) and frontend (port 5000)
- Integrated OpenAI API support with intelligent fallback to mock summaries

### Bug Fixes and Improvements
- Fixed locality detection to handle multi-word names with punctuation
- Added environment variable support for backend URL configuration
- Improved comparison summaries to show stats for all localities
- Created comprehensive README documentation

## Project Architecture

### Backend (`/backend`)
- **Django 5.2.8** with REST Framework
- **Data Processing**: pandas & openpyxl for Excel parsing
- **API Endpoints**:
  - `/api/health/` - Health check
  - `/api/localities/` - List available localities
  - `/api/analyze/` - Process queries and return analysis

### Frontend (`/frontend`)
- **React 19.2.0** with functional components and hooks
- **UI Framework**: Bootstrap 5 for responsive design
- **Charts**: Chart.js for interactive visualizations
- **Components**:
  - `ChatInterface.js` - Main chat UI with query handling
  - `ChartComponent.js` - Dynamic chart rendering

### Data (`/backend/data`)
- Excel file with real estate data (2020-2024)
- Localities: Akurdi, Ambegaon Budruk, Aundh, Wakad
- Metrics: Price trends, demand, sales volume, carpet area

## User Preferences
- None specified yet

## Features

### Core Functionality
1. **Natural Language Queries**: Ask about real estate trends in plain English
2. **Single Locality Analysis**: Get detailed price and demand trends for one area
3. **Comparison Analysis**: Compare multiple localities side-by-side
4. **Interactive Charts**: Visualize trends with line and bar charts
5. **Data Tables**: View detailed year-by-year statistics
6. **AI Summaries**: OpenAI-powered insights (optional, with fallback)

### Sample Queries
- "Give me analysis of Wakad"
- "Compare Ambegaon Budruk and Aundh demand trends"
- "Show price growth for Akurdi over the last 3 years"

## Environment Configuration

### Backend Environment Variables
- Standard Django settings (SECRET_KEY, DEBUG, etc.)
- `OPENAI_API_KEY` (optional) - For AI-powered summaries

### Frontend Environment Variables (`.env` file)
- `PORT=5000` - Frontend server port
- `DANGEROUSLY_DISABLE_HOST_CHECK=true` - Allow Replit proxy
- `WDS_SOCKET_PORT=0` - WebSocket configuration
- `REACT_APP_BACKEND_URL=http://127.0.0.1:8000` - Backend API URL

## Running the Application

Both workflows are configured and start automatically:
- **Backend**: Django server on port 8000
- **Frontend**: React dev server on port 5000 (webview)

Manual commands:
```bash
# Backend
cd backend && python manage.py runserver 0.0.0.0:8000

# Frontend  
cd frontend && PORT=5000 DANGEROUSLY_DISABLE_HOST_CHECK=true npm start
```

## Testing

### API Testing
```bash
# Health check
curl http://127.0.0.1:8000/api/health/

# List localities
curl http://127.0.0.1:8000/api/localities/

# Analyze query
curl -X POST http://127.0.0.1:8000/api/analyze/ \
  -H "Content-Type: application/json" \
  -d '{"query": "Analyze Wakad"}'
```

### Verified Functionality
✅ Single locality queries work correctly  
✅ Multi-locality comparison queries detect all localities  
✅ Charts render with correct data for all localities  
✅ Data tables display comprehensive information  
✅ Mock summaries provide meaningful insights  
✅ Frontend-backend integration works seamlessly  
✅ Responsive UI with Bootstrap styling

## Known Limitations
- LSP type-checking warnings in pandas code (cosmetic, not functional errors)
- OpenAI integration requires API key (falls back to mock summaries)
- Data limited to 4 Pune localities (2020-2024)

## Deployment Notes
- Frontend can be deployed to Vercel/Netlify
- Backend can be deployed to Render/Heroku/Railway
- Set `REACT_APP_BACKEND_URL` to production backend URL
- Ensure Django ALLOWED_HOSTS includes production domain
- Run `python manage.py migrate` on first deployment

## Future Enhancements
- Add data export functionality (CSV/Excel download)
- Implement user authentication and query history
- Add more chart types (pie charts, heatmaps)
- Expand to more localities and years
- Add mobile app version
- Implement caching for faster responses
