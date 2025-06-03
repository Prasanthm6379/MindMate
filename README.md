# MindMate 🧠💙

A comprehensive full-stack digital companion application designed to support Alzheimer's patients and their caregivers in managing daily life, health monitoring, and emergency situations.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Frontend Components](#frontend-components)
- [API Endpoints](#api-endpoints)
- [Getting Started](#getting-started)
- [Authentication](#authentication)
- [Usage Examples](#usage-examples)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

MindMate is a specialized application that addresses the unique challenges faced by individuals with Alzheimer's disease and their caregivers. The platform provides tools for memory assistance, activity tracking, emergency alerts, medication reminders, and caregiver coordination.

### Key Problems Solved:
- **Memory Support**: Digital notes and reminders to help with daily tasks
- **Safety Monitoring**: Emergency alert system with caregiver notifications
- **Health Tracking**: Activity logging and medication reminders
- **Caregiver Coordination**: Multi-caregiver support with emergency contacts
- **Independence**: Helping patients maintain autonomy while staying safe

## 🏗 Architecture

MindMate is built as a modern full-stack application:

### Frontend (React.js)
- **Single Page Application (SPA)** with React 18+
- **Context API** for state management and authentication
- **Component-based architecture** for reusable UI elements
- **Responsive design** for mobile and desktop compatibility

### Backend (Flask API)
- **RESTful API** with Flask framework
- **JWT authentication** for secure user sessions
- **Database integration** with SQLAlchemy ORM
- **CORS enabled** for frontend-backend communication

## ✨ Features

### 👤 User Management
- **User Registration & Authentication**: Secure account creation and JWT-based login
- **Profile Management**: Update user information and account settings
- **Account Security**: Protected endpoints with bearer token authentication

### 📝 Memory Notes
- **Digital Memory Aid**: Create, edit, and organize personal notes and reminders
- **Multiple Note Types**: Support for text notes and other content types
- **Easy Retrieval**: Quick access to important information and memories
- **Personal Organization**: Title-based categorization for better organization

### 👥 Caregiver Network
- **Multiple Caregivers**: Add and manage multiple caregivers per patient
- **Emergency Contacts**: Designate primary emergency contacts
- **Relationship Tracking**: Record caregiver relationships (family, professional, etc.)
- **Contact Information**: Store phone numbers and email addresses for quick access

### 🚨 Emergency Alert System
- **Instant Alerts**: Send emergency notifications to designated caregivers
- **Location Tracking**: Include location information in emergency alerts
- **Alert Management**: Track alert status and resolution
- **Time Stamping**: Automatic logging of alert times for record-keeping

### 📊 Activity Logging
- **Daily Activity Tracking**: Log various types of activities (exercise, meals, medication, etc.)
- **Health Monitoring**: Track physical and mental activities
- **Progress Tracking**: Monitor activity patterns over time
- **Detailed Records**: Store activity details and timestamps

### ⏰ Smart Reminders
- **Medication Reminders**: Never miss important medications
- **Appointment Scheduling**: Healthcare and social appointment reminders
- **Recurring Reminders**: Weekly, daily, or custom repeat intervals
- **Categorized Reminders**: Health, personal, and social reminder types
- **Status Tracking**: Mark reminders as completed or pending

## 🎨 Frontend Components

### Core Components
- **📱 Dashboard**: Central hub displaying overview of all user activities and alerts
- **🔐 Login/Register**: User authentication and account creation interface
- **📝 MemoryNotes**: Create, edit, and manage digital memory aids
- **👥 Caregivers**: Manage caregiver network and emergency contacts
- **🚨 EmergencyAlerts**: View and manage emergency alert system
- **📊 Activities**: Log and track daily activities and health metrics
- **⏰ Reminders**: Set up and manage medication and appointment reminders
- **🧭 Navigation**: Intuitive navigation between different app sections

### Supporting Architecture
- **🔐 AuthContext**: Global authentication state management
- **🌐 API Service**: Centralized API communication layer
- **📱 Responsive Design**: Mobile-first, accessible user interface

## 🔌 API Endpoints

### Authentication
```
POST /user/login              # User authentication
```

### User Management
```
POST /user/                   # Create new user account
PUT /user/                    # Update user information
DELETE /user/{email}          # Delete user account
GET /user/{email}             # Get user by email
```

### Memory Notes
```
POST /user/memoryNote/{user_id}         # Create new memory note
PUT /user/memoryNote/{user_id}          # Update existing note
GET /user/memoryNote/{user_id}          # Get all notes for user
GET /user/memoryNote/{user_id}/{note_id} # Get specific note
DELETE /user/memoryNote/{user_id}/{note_id} # Delete note
```

### Caregiver Management
```
POST /user/caregiver                    # Add new caregiver
PUT /user/caregiver                     # Update caregiver information
GET /user/caregiver                     # Get all caregivers
GET /user/caregiver/{user_id}/{caregiver_id} # Get specific caregiver
DELETE /user/caregiver/{user_id}/{caregiver_id} # Remove caregiver
```

### Emergency Alerts
```
POST /user/emergencyalert               # Create emergency alert
PUT /user/emergencyalert                # Update alert status
GET /user/emergencyalert                # Get all alerts
GET /user/emergencyalert/{alert_id}     # Get specific alert
DELETE /user/emergencyalert             # Delete alert
```

### Activity Logging
```
POST /user/activitylog                  # Log new activity
PUT /user/activitylog                   # Update activity record
GET /user/activitylog                   # Get all activities
GET /user/activitylog/{activity_id}     # Get specific activity
DELETE /user/activitylog                # Delete activity record
```

### Reminders
```
POST /user/remainder                    # Create new reminder
PUT /user/remainder                     # Update reminder
GET /user/remainder/{user_id}           # Get all reminders for user
GET /user/remainder/{reminder_id}       # Get specific reminder
DELETE /user/remainder                  # Delete reminder
```

## 🚀 Getting Started

### Prerequisites
**Backend Requirements:**
- Python 3.8+
- Flask framework
- JWT authentication library
- Database system (SQLite/PostgreSQL/MySQL)

**Frontend Requirements:**
- Node.js 16+
- npm or yarn package manager
- Modern web browser

### Installation

#### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mindmate.git
   cd mindmate
   ```

2. **Set up backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize the database**
   ```bash
   python init_db.py
   ```

5. **Start the Flask API**
   ```bash
   python app.py
   ```
   API will be available at `http://localhost:5000`

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd Frontend/mind-mate
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Configure API endpoint**
   ```bash
   # Create .env file in frontend directory
   echo "REACT_APP_API_URL=http://localhost:5000" > .env
   ```

4. **Start the React application**
   ```bash
   npm start
   # or
   yarn start
   ```
   Frontend will be available at `http://localhost:3000`

### Quick Start
1. Start the backend server on port 5000
2. Start the frontend development server on port 3000
3. Navigate to `http://localhost:3000` in your browser
4. Create a new account or login with existing credentials

## 🔐 Authentication

MindMate uses JWT (JSON Web Token) based authentication. 

### Login Process:
1. **POST** to `/user/login` with email and password
2. Receive JWT token in response
3. Include token in Authorization header: `Bearer {your_token}`
4. Token expires after 12 hours (configurable)

### Example Login:
```bash
curl -X POST http://localhost:5000/user/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "your_password"}'
```

## 📖 Usage Examples

### Creating a Memory Note
```bash
curl -X POST http://localhost:5000/user/memoryNote/{user_id} \
  -H "Authorization: Bearer {your_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Doctor Appointment",
    "content": "Appointment with Dr. Smith on Friday at 2 PM",
    "note_type": "note"
  }'
```

### Adding a Caregiver
```bash
curl -X POST http://localhost:5000/user/caregiver \
  -H "Authorization: Bearer {your_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "user_id_here",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": 1234567890,
    "relationship": "Son",
    "emergency_contact": true
  }'
```

### Setting a Medication Reminder
```bash
curl -X POST http://localhost:5000/user/remainder \
  -H "Authorization: Bearer {your_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_id_here",
    "title": "Take Medication",
    "description": "Take morning pills with breakfast",
    "reminder_time": "2025-03-10T08:00:00",
    "repeat_interval": "daily",
    "reminder_type": "health"
  }'
```

## 🛠 Technology Stack

### Frontend
- **React.js 18+**: Modern JavaScript library for building user interfaces
- **React Context API**: State management for authentication and global state
- **CSS3**: Styling and responsive design
- **JavaScript ES6+**: Modern JavaScript features
- **Fetch API**: HTTP client for API communication

### Backend
- **Flask**: Lightweight Python web framework
- **Flask-JWT-Extended**: JWT token authentication
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Flask-CORS**: Cross-Origin Resource Sharing support
- **Python 3.8+**: Backend programming language

### Database
- **SQLite/PostgreSQL/MySQL**: Configurable database options

### Development Tools
- **Node.js & npm**: Frontend package management
- **Postman**: API testing and documentation
- **Git**: Version control

## 📁 Project Structure

```
MindMate/
├── Backend/                    # Flask API backend
│   ├── app.py                 # Main Flask application
│   ├── models/                # Database models
│   ├── routes/                # API route handlers
│   ├── config.py              # Configuration settings
│   └── requirements.txt       # Python dependencies
│
├── Frontend/mind-mate/        # React frontend
│   ├── public/                # Static assets
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── Dashboard.jsx      # Main dashboard
│   │   │   ├── Login.jsx          # Authentication
│   │   │   ├── Register.jsx       # User registration
│   │   │   ├── MemoryNotes.jsx    # Memory management
│   │   │   ├── Caregivers.jsx     # Caregiver management
│   │   │   ├── EmergencyAlerts.jsx # Emergency system
│   │   │   ├── Activities.jsx     # Activity tracking
│   │   │   ├── Reminders.jsx      # Reminder system
│   │   │   └── Navigation.jsx     # App navigation
│   │   ├── context/
│   │   │   └── AuthContext.jsx    # Authentication context
│   │   ├── services/
│   │   │   └── api.jsx            # API service layer
│   │   ├── App.jsx            # Main React component
│   │   └── index.js           # React entry point
│   ├── package.json           # Node.js dependencies
│   └── .env                   # Environment variables
│
├── README.md                  # Project documentation
└── .gitignore                # Git ignore file
```

## 🤝 Contributing

We welcome contributions to MindMate! Here's how you can help:

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Set up both frontend and backend development environments
4. Make your changes
5. Add tests for new functionality
6. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
7. Push to the branch (`git push origin feature/AmazingFeature`)
8. Open a Pull Request

### Contribution Guidelines
- **Frontend**: Follow React best practices and ESLint rules
- **Backend**: Follow PEP 8 style guidelines for Python code
- Add unit tests for new features
- Update documentation for API changes
- Ensure all tests pass before submitting PR
- Write clear, descriptive commit messages
- Test both frontend and backend integration

### Reporting Issues
- Use GitHub Issues to report bugs
- Include detailed reproduction steps
- Provide system information and error logs
- Use appropriate issue labels

---

**MindMate** - Empowering independence, ensuring safety, supporting families. 💙

*Made with ❤️ for the Alzheimer's community*