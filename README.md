📖 StudyMate AI
StudyMate AI is a simple student study planner and performance management system built using Python, FastAPI, SQLAlchemy, SQLite, HTML, CSS, and JavaScript.

The application allows students to enter their study hours and marks. Based on the entered information, it provides a performance level, study suggestion, and study plan.

✨ Features
👨‍🎓 Add student details
📚 Store study hours
📝 Store student marks
🏆 Automatically calculate performance level
💡 Generate study suggestions
📖 Generate study plans
👀 View all students
✏️ Edit student information
🗑️ Delete student information
💾 Store student data in SQLite database
🌐 FastAPI backend with HTML/CSS/JavaScript frontend
🛠️ Technologies Used
Backend
Python
FastAPI
SQLAlchemy
Pydantic
Uvicorn
Frontend
HTML
CSS
JavaScript
Database
SQLite
📂 Project Structure
StudyMate-AI/
│
├── main.py
├── database.py
├── models.py
├── frontend.html
├── requirements.txt
├── README.md
└── .gitignore

Note: studymate.db will be created automatically when the application runs.

📊 Performance Levels
Mark	Level
90 - 100	Excellent
75 - 89	Very Good
50 - 74	Good
Below 50	Needs Improvement

📚 Study Suggestions
The application provides study suggestions based on the student's study hours.

5 or more hours → Keep up the good study routine!
3 to 4.9 hours → Try to increase your study hours.
Below 3 hours → You need to spend more time studying.
📖 Study Plans
The application generates a study plan based on the student's marks.

90 or above → Revise important topics and practice mock tests.
75 to 89 → Spend 1 hour on revision and 1 hour on weak topics.
50 to 74 → Study 2 hours daily and practice important questions.
Below 50 → Study 3 hours daily and focus more on weak subjects.
🚀 How to Run
1. Open the project folder
Open the StudyMate-AI project folder in VS Code.

2. Open Terminal
In VS Code, select:

Terminal → New Terminal

3. Install required packages
Run:

python -m pip install -r requirements.txt

4. Start the FastAPI server
Run:

python -m uvicorn main:app --reload

The backend will start at:

http://127.0.0.1:8000

5. Test the API
Open this URL in your browser:

http://127.0.0.1:8000

You should see:

StudyMate API is working!

6. Open API documentation
FastAPI provides automatic API documentation.

Open:

http://127.0.0.1:8000/docs

You can use the Swagger UI to test the API endpoints.

7. Open the frontend
Open frontend.html in your browser after starting the FastAPI server.

The frontend communicates with the FastAPI backend to add, view, edit, and delete students.

🔗 API Endpoints
Method	Endpoint	Description
GET	/	Check API status
POST	/student	Add a new student
GET	/students	Get all students
PUT	/student/{student_id}	Update a student
DELETE	/student/{student_id}	Delete a student

🗄️ Database
StudyMate AI uses SQLite as its database.

The database file is:

studymate.db

The database stores student information such as:

Student name
Study hours
Mark
Performance level
Study suggestion
🔮 Future Improvements
Possible future improvements include:

🤖 AI-powered personalized study recommendations
📅 Automatic daily and weekly study schedules
📈 Student performance charts
🔐 User login and authentication
📱 Mobile-friendly design
📊 Subject-wise marks tracking
⏰ Study reminders
📄 PDF report generation
☁️ Cloud database integration
🎯 Project Goal
The main goal of StudyMate AI is to help students understand their academic performance and improve their study habits.

This project also demonstrates how a frontend application can communicate with a FastAPI backend and store data using SQLAlchemy and SQLite.

👨‍💻 Author
Mahalakshmi

GitHub:

https://github.com/mahalakshmi-73

📄 License
This project is created for educational and learning purposes.