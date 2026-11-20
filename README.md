# EcoTruck – Smart Waste Management System

A college-level full-stack web application built with Python Flask, SQLite, HTML, CSS and Jinja templates.

## Features
- Citizen, driver and administrator roles
- Registration and secure password hashing
- Citizen pickup requests with waste category, quantity, address and preferred date
- Admin assignment of drivers and trucks
- Driver pickup status updates
- Truck fleet management
- Complaint submission and resolution
- Recycling records generated when a pickup is marked Completed
- Admin reports and dashboard statistics
- Profile editing

## Requirements
- Windows 10/11
- Python 3.10 or newer
- Visual Studio Code

## Run in VS Code (Windows PowerShell)

1. Extract `EcoTruck.zip`.
2. Open VS Code.
3. Select **File → Open Folder** and choose the extracted `EcoTruck` folder.
4. Open **Terminal → New Terminal**.
5. Create a virtual environment:

   ```powershell
   py -m venv venv
   ```

6. Activate it:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run this once in the terminal:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\venv\Scripts\Activate.ps1
   ```

7. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

8. Start the application:

   ```powershell
   python app.py
   ```

9. Open this address in your browser:

   `http://127.0.0.1:5000`

## Demo logins

| Role | Email | Password |
|---|---|---|
| Administrator | admin@ecotruck.com | admin123 |
| Driver | driver@ecotruck.com | driver123 |

Citizens should create their own account using **Create account**.

## Suggested demonstration

1. Log in as a citizen and create a pickup request.
2. Log out and sign in as administrator.
3. Open Pickup requests and assign a driver and truck.
4. Log out and sign in as the demo driver.
5. Update the request to Picked Up and then Completed.
6. Sign back in as administrator and open Reports & analytics.
7. Demonstrate complaint submission as a citizen and resolution as admin.

## Database
The SQLite database `ecotruck.db` is automatically created in the project folder on first run. Tables include users, trucks, pickups, complaints and recycling.

To reset the demo data, stop the app, delete `ecotruck.db`, and run `python app.py` again. The database and sample admin/driver accounts will be recreated.

## Notes
- This is a local college demonstration application. It does not connect to a real GPS device, municipal system, SMS gateway or live map service.
- Route management is represented by pickup addresses and assignment workflow; live GPS tracking and automatic route optimisation are future enhancements.
- Change the Flask secret key and use production deployment settings before public deployment.
