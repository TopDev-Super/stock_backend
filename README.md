# Stock AI Analysis System

An AI-powered stock market data analysis system that allows users to query stock data using natural language. Built with FastAPI (backend) and React (frontend).

## 🏗️ Project Structure

```
stock_AI/
├── backend/                 # Python FastAPI Backend
│   ├── api/                # FastAPI application
│   ├── ai/                 # AI/LLM services
│   ├── database/           # Database connection
│   ├── models/             # Pydantic schemas
│   ├── services/           # Business logic
│   ├── config.py           # Configuration
│   ├── requirements.txt    # Python dependencies
│   └── run.py             # Backend entry point
├── frontend/               # React Frontend
│   ├── public/            # Static files
│   ├── src/               # React components
│   ├── package.json       # Node.js dependencies
│   └── README.md          # Frontend documentation
├── docs/                   # Documentation
├── scripts/                # Setup and utility scripts
└── README.md              # This file
```

## 🚀 Quick Start

### Option 1: Run Complete System Setup
```bash
python scripts/setup_complete_system.py
```

### Option 2: Manual Setup

#### Backend Setup
```bash
# Navigate to backend
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Configure environment
cp env_template.txt .env
# Edit .env with your database and OpenAI credentials

# Test backend
python test_system.py

# Start backend server
python run.py
```

#### Frontend Setup
```bash
# Navigate to frontend
cd frontend

# Install Node.js dependencies
npm install

# Start frontend development server
npm start
```

## 📋 Prerequisites

### Backend Requirements
- Python 3.8+
- MySQL Server
- OpenAI API Key

### Frontend Requirements
- Node.js 16+
- npm or yarn

## 🔧 Backend (Python/FastAPI)

### Features
- **Natural Language Querying**: Convert questions to SQL
- **AI-Powered SQL Generation**: OpenAI GPT-4 integration
- **Database Schema Awareness**: Automatic table discovery
- **Intelligent Results Explanation**: AI explains query results
- **RESTful API**: Complete API with Swagger documentation
- **Real-time Database Connection**: Direct MySQL integration

### API Endpoints
- `GET /health` - System health check
- `GET /database/status` - Database connection status
- `POST /query` - Process natural language questions
- `GET /suggestions` - Get AI-generated question suggestions
- `GET /examples` - Get example questions

### Backend Architecture
```
backend/
├── api/main.py              # FastAPI application
├── ai/llm_service.py        # OpenAI/LangChain integration
├── database/connection.py   # MySQL connection management
├── services/stock_ai_service.py # Main business logic
├── models/schemas.py        # Pydantic models
├── config.py               # Configuration management
├── requirements.txt         # Python dependencies
└── run.py                  # Backend entry point
```

### Backend Setup Instructions
1. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp env_template.txt .env
   # Edit .env with your credentials
   ```

3. **Test System**
   ```bash
   python test_system.py
   ```

4. **Start Server**
   ```bash
   python run.py
   ```

5. **Access API Documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 🎨 Frontend (React)

### Features
- **Modern UI/UX**: Clean, professional interface
- **Responsive Design**: Works on all devices
- **Real-time Updates**: Live system monitoring
- **Interactive Components**: Rich query interface
- **Data Visualization**: Analytics dashboard
- **Toast Notifications**: User-friendly feedback

### Frontend Architecture
```
frontend/
├── public/
│   └── index.html          # Main HTML file
├── src/
│   ├── components/         # React components
│   │   ├── Layout.js      # Main layout with navigation
│   │   ├── Dashboard.js   # Dashboard overview
│   │   ├── QueryInterface.js # AI query interface
│   │   ├── DatabaseStatus.js # Database monitoring
│   │   ├── Suggestions.js # AI suggestions
│   │   └── Analytics.js   # Analytics dashboard
│   ├── services/
│   │   └── api.js         # API service layer
│   ├── App.js             # Main app component
│   ├── index.js           # React entry point
│   └── index.css          # Global styles
├── package.json           # Dependencies and scripts
├── tailwind.config.js    # Tailwind configuration
└── postcss.config.js     # PostCSS configuration
```

### Frontend Setup Instructions
1. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start Development Server**
   ```bash
   npm start
   ```

3. **Access Application**
   - Frontend: http://localhost:3000

## 🔗 API Integration

The frontend communicates with the backend via REST API:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | System health check |
| `/database/status` | GET | Database connection status |
| `/query` | POST | Process natural language query |
| `/suggestions` | GET | Get AI-generated suggestions |
| `/examples` | GET | Get example questions |

### Example API Usage
```bash
# Health check
curl http://localhost:8000/health

# Process query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Which stocks have a price above 100?"}'

# Get suggestions
curl http://localhost:8000/suggestions
```

## 🛠️ Development

### Backend Development
- **Adding New Endpoints**: Modify `backend/api/main.py`
- **Database Operations**: Extend `backend/database/connection.py`
- **AI Logic**: Modify `backend/ai/llm_service.py`
- **Business Logic**: Update `backend/services/stock_ai_service.py`

### Frontend Development
- **Adding New Components**: Create in `frontend/src/components/`
- **API Integration**: Use `frontend/src/services/api.js`
- **Styling**: Use Tailwind CSS classes
- **Routing**: Add routes in `frontend/src/App.js`

## 📚 Documentation

- **Backend Documentation**: See `backend/README.md`
- **Frontend Documentation**: See `frontend/README.md`
- **API Documentation**: http://localhost:8000/docs (when backend is running)

## 🚀 Deployment

### Backend Deployment
```bash
cd backend
pip install -r requirements.txt
python run.py
```

### Frontend Deployment
```bash
cd frontend
npm install
npm run build
# Serve the build/ directory
```

## 🔧 Troubleshooting

### Common Backend Issues
1. **Database Connection Failed**
   - Verify MySQL server is running
   - Check database credentials in `.env`
   - Ensure database and tables exist

2. **OpenAI API Errors**
   - Verify API key is correct
   - Check API key has sufficient credits
   - Ensure internet connection

### Common Frontend Issues
1. **API Connection Failed**
   - Ensure backend is running on localhost:8000
   - Check CORS configuration
   - Verify API endpoints

2. **Build Errors**
   - Clear node_modules and reinstall
   - Check Node.js version (16+ required)
   - Verify all dependencies are installed

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation at `/docs`
3. Check application logs for detailed error messages
4. Verify database and OpenAI configurations 