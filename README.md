# MindMate 🧠💙

A comprehensive digital companion application designed to support Alzheimer's patients and their caregivers in managing daily life, health monitoring, and emergency situations.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Getting Started](#getting-started)
- [Authentication](#authentication)
- [Usage Examples](#usage-examples)
- [Technology Stack](#technology-stack)
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
- Python 3.8+
- Flask framework
- JWT authentication library
- Database system (SQLite/PostgreSQL/MySQL)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mindmate.git
   cd mindmate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize the database**
   ```bash
   python init_db.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

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

- **Backend Framework**: Flask (Python)
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: SQLite/PostgreSQL/MySQL (configurable)
- **API Architecture**: RESTful API
- **Security**: Bearer token authentication
- **Data Format**: JSON

## 🤝 Contributing

We welcome contributions to MindMate! Here's how you can help:

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Add tests for new functionality
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Contribution Guidelines
- Follow PEP 8 style guidelines for Python code
- Add unit tests for new features
- Update documentation for API changes
- Ensure all tests pass before submitting PR
- Write clear, descriptive commit messages

### Reporting Issues
- Use GitHub Issues to report bugs
- Include detailed reproduction steps
- Provide system information and error logs
- Use appropriate issue labels

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- 📧 Email: support@mindmate.app
- 💬 GitHub Issues: [Create an issue](https://github.com/yourusername/mindmate/issues)
- 📚 Documentation: [Wiki](https://github.com/yourusername/mindmate/wiki)

## 🙏 Acknowledgments

- Healthcare professionals who provided insights into Alzheimer's care
- Caregivers and families who shared their experiences
- Open source community for the tools and libraries used

---

**MindMate** - Empowering independence, ensuring safety, supporting families. 💙

*Made with ❤️ for the Alzheimer's community*