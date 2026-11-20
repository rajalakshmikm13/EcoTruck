# ♻️ EcoTruck – Smart Waste Management System

A college-level full-stack web application built with Python Flask, SQLite, HTML, CSS and Jinja templates.

EcoTruck is designed to simplify waste collection and recycling management by connecting citizens, waste collection drivers and administrators through a single web application.

---

## 1. Problem Statement

Traditional waste management systems often involve manual collection requests, inefficient communication and difficulties in monitoring waste collection activities.

Citizens may experience delayed pickups, while administrators may find it difficult to manage collection vehicles, drivers and recycling records.

EcoTruck aims to provide a centralised digital solution to improve waste collection management, simplify pickup scheduling and maintain recycling records.

## 2. Objectives

- Develop a user-friendly smart waste management application.
- Allow citizens to request waste collection online.
- Organise waste into different categories.
- Manage collection trucks and drivers.
- Assign drivers and trucks to pickup requests.
- Track waste collection status.
- Provide complaint management facilities.
- Maintain recycling records.
- Generate collection reports and statistics.

## 3. Features and Modules

### 3.1 User Authentication
- Citizen, driver and administrator roles.
- User registration and login.
- Secure password hashing.
- Role-based access control.

### 3.2 Citizen Dashboard
- View pickup statistics.
- Submit waste pickup requests.
- View pickup history and status.
- Submit complaints.
- Update profile information.

### 3.3 Waste Pickup Management
- Create waste collection requests.
- Select waste categories.
- Enter waste quantity.
- Provide collection address.
- Select preferred collection date.
- Monitor pickup status.

### 3.4 Waste Categorisation

The application supports:
- Organic waste
- Plastic waste
- Paper waste
- Metal waste
- E-waste
- Mixed waste

### 3.5 Truck Management
- Register collection trucks.
- Maintain truck registration numbers.
- Store truck models and capacities.
- View truck availability and maintenance status.

### 3.6 Driver Management
- View registered drivers.
- Monitor assigned collection jobs.
- Assign drivers to pickup requests.

### 3.7 Pickup Tracking

The application supports the following pickup statuses:

1. Requested
2. Assigned
3. Picked Up
4. Completed
5. Cancelled

### 3.8 Complaint Management
- Citizens can submit complaints.
- Administrators can view complaints.
- Administrators can resolve complaints.

### 3.9 Recycling Management
- Record completed waste collections.
- Categorise recycled waste.
- Maintain recycling quantities.

### 3.10 Reports and Analytics
- View total pickup requests.
- Monitor completed and pending pickups.
- View recycling quantities by category.
- Monitor registered citizen accounts.

---

## 4. Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML5, CSS3 |
| Backend | Python |
| Web Framework | Flask |
| Database | SQLite |
| Template Engine | Jinja2 |
| Password Security | Werkzeug |
| Code Editor | Visual Studio Code |
| Version Control | Git |
| Repository Hosting | GitHub |

---

## 5. Project Folder Structure

```text
EcoTruck/
│
├── app.py
├── requirements.txt
├── README.md
├── ecotruck.db
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── new_pickup.html
│   ├── pickups.html
│   ├── trucks.html
│   ├── drivers.html
│   ├── complaints.html
│   ├── reports.html
│   └── profile.html
│
└── static/
    └── style.css
```

Note: The SQLite database is created automatically when the application starts.

---

## 6. Requirements

- Windows 10/11
- Python 3.10 or newer
- Visual Studio Code
- Git
- Web browser

---

## 7. Run in VS Code (Windows PowerShell)

### Step 1: Extract the Project

Extract `EcoTruck.zip` into your computer.

### Step 2: Open VS Code

1. Open Visual Studio Code.
2. Select **File → Open Folder**.
3. Choose the extracted `EcoTruck` folder.

### Step 3: Open Terminal

Select **Terminal → New Terminal**.

### Step 4: Create a Virtual Environment

```powershell
py -m venv venv
```

### Step 5: Activate the Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### Step 6: Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

### Step 7: Start the Application

```powershell
python app.py
```

### Step 8: Open the Application

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

## 8. Demo Login Credentials

| Role | Email | Password |
|---|---|---|
| Administrator | admin@ecotruck.com | admin123 |
| Driver | driver@ecotruck.com | driver123 |

Citizens should create their own account using the **Create account** page.

Note: These are demonstration credentials. They should be changed before public deployment.

---

## 9. Sample Inputs and Outputs

### Sample Input – Waste Pickup Request

| Field | Sample Value |
|---|---|
| Waste Category | Plastic |
| Quantity | 5 kg |
| Address | Madurai |
| Preferred Date | Selected date |
| Additional Notes | Near main entrance |

### Expected Output

The application creates a pickup request with a unique request ID and displays its initial status as `Requested`.

### Pickup Status Workflow

```text
Citizen submits pickup request
             |
             v
          Requested
             |
             v
Admin assigns driver and truck
             |
             v
          Assigned
             |
             v
Driver collects the waste
             |
             v
          Picked Up
             |
             v
          Completed
             |
             v
Recycling record generated
```

---

## 10. Suggested Demonstration

1. Log in as a citizen and create a pickup request.
2. Log out and sign in as administrator.
3. Open Pickup Requests and assign a driver and truck.
4. Log out and sign in as the demo driver.
5. Update the request to Picked Up and then Completed.
6. Sign back in as administrator and open Reports & Analytics.
7. Demonstrate complaint submission as a citizen and resolution as administrator.

---

## 11. Testing Performed

The following test cases are to be used to verify the application.

| Test Case | Expected Result |
|---|---|
| Citizen registration | Account created |
| Valid login | Dashboard displayed |
| Invalid login | Error message displayed |
| Pickup request | Request saved |
| Truck registration | Truck added |
| Driver assignment | Driver and truck assigned |
| Pickup status update | Status updated |
| Complaint submission | Complaint saved |
| Complaint resolution | Complaint marked Resolved |
| Reports | Collection statistics displayed |

**Testing results:** Update the actual test results after executing the application and verifying each feature.

---

## 12. Database

The SQLite database `ecotruck.db` is automatically created in the project folder on the first run.

The database contains the following tables:

| Table | Purpose |
|---|---|
| users | Stores citizen, driver and administrator details |
| trucks | Stores collection truck information |
| pickups | Stores waste pickup requests |
| complaints | Stores submitted complaints |
| recycling | Stores recycling records |

To reset the demonstration data:

1. Stop the application.
2. Delete `ecotruck.db`.
3. Run `python app.py` again.

The database and sample administrator and driver accounts will be recreated.

---

## 13. Known Limitations

- Live GPS tracking is not implemented.
- Automatic route optimisation is not implemented.
- Real-time vehicle location is not available.
- SMS and email notifications are not integrated.
- The application currently uses a local SQLite database.

Route management is represented through pickup addresses and driver/truck assignment.

---

## 14. Future Enhancements

- GPS-based live truck tracking.
- Automatic waste collection route optimisation.
- AI-based waste classification.
- Smart waste-bin monitoring using IoT sensors.
- Email and SMS notifications.
- Mobile application integration.
- Cloud database integration.
- Advanced recycling analytics.

---

## 15. Conclusion

EcoTruck provides a centralised platform for managing waste collection activities through a web-based application.

It connects citizens, drivers and administrators through different modules for pickup requests, truck management, driver assignment, complaints and recycling reports.

The project demonstrates how Python, Flask, SQLite and web technologies can be used to develop a practical Smart Waste Management System.

---

## 16. References

- Python Documentation: https://docs.python.org/3/
- Flask Documentation: https://flask.palletsprojects.com/
- SQLite Documentation: https://www.sqlite.org/docs.html
- Git Documentation: https://git-scm.com/doc
- GitHub Documentation: https://docs.github.com/
