# **Library Management System**

### A full-stack web application for managing a library's resources and operations efficiently.

---

## **Features**

### 1. **Authentication**
- **Admin Login**:
  - Admin credentials for managing library resources.
  - Accessible via the admin login page.
- **User Login**:
  - User credentials for browsing and interacting with the library.
  - Accessible via the user login page.

### 2. **Admin Dashboard**
- Access to the following functionalities:
  - **Reports**: Generate insights into library resources and activity.
  - **Transactions**: Manage book issues, returns, and fines.
  - **Maintenance**: Perform system housekeeping tasks.
  - **Books Management**: Add, update, or delete records.

### 3. **User Dashboard**
- Access to:
  - **Book Listings**: Browse available books.
  - **Transactions**: Request book issues, return books, and pay fines.
  - **Membership Status**: View current membership details.

### 4. **Transactions**
- **Book Issue**: Users request books, and admins approve or reject them.
- **Return Book**: Users return books, with overdue fines calculated.
- **Pay Fine**: Users can pay overdue fines.

### 5. **Reports**
- **Master Lists**:
  - Books
  - Memberships
- **Activity Reports**:
  - Active Issues
  - Overdue Returns

### 6. **Maintenance Module**
- **Housekeeping**:
  - Clean expired memberships.
  - Archive old transactions.
- **Membership Management**:
  - Add or update user memberships.
- **Books Management**:
  - Add or update book records.

---

## **Tech Stack**

### **Backend:**
- Python (Django Framework)
- Django REST Framework

### **Frontend:**
- HTML/CSS
- Bootstrap

### **Database:**
- SQLite

---

## **Installation**

### **Step 1: Clone the Repository**

git clone https://github.com/myselfharsh7/library-management-system.git
cd library-management-system

### ** Step 2: Set Up a Virtual Environment

python3 -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate  # Windows

### **Step 3: Install Dependencies

pip install -r requirements.txt

### **Step 4: Apply Migrations

python manage.py makemigrations
python manage.py migrate

### **Step 5: Create a Superuser

python manage.py createsuperuser

### **Step 6: Run the Server

python manage.py runserver

### **Usage
Admin Workflow

    Login: Use admin credentials.
    Dashboard:
        Manage books, users, transactions, and reports.
    Transactions:
        Approve/reject book issue requests.
        Mark book returns and calculate fines.

User Workflow

    Login: Use user credentials.
    Dashboard:
        Browse books.
        Request book issues.
        View transactions and pay fines.

### **Folder Structure

library-management-system/
├── core/
│   ├── migrations/
│   ├── templates/
│   │   ├── core/  (all html files)
│   ├── views.py
│   ├── models.py
│   ├── urls.py
├── library_management/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md

### **Contact
Name: Harsh Kumar Gupta
GitHub: myselfharsh7
Email: kumadii7@gmail.com
linkedin : https://www.linkedin.com/in/harsh-kumar-gupta-4a624318b/
