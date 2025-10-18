# IKSC CTF 🕵️‍♂️

A full-featured **Capture The Flag (CTF) platform** built with **Flask** and **SQLite**.  
Designed for learning web security, managing challenges, and tracking scores in a competitive CTF setup.

---

## Features 🚀

- **User Authentication:** Secure registration and login with hashed passwords.
- **Admin Dashboard:**  
  - View total challenges, users, and flags solved.  
  - Add/manage challenges easily.  
  - Track user scores and submissions.
- **Challenge Management:** Create, view, and solve challenges.  
- **Leaderboard:** Real-time leaderboard showing top users and solved counts.  
- **Responsive Design:** Works beautifully on mobile and desktop (Bootstrap + Chart.js).  
- **Secure:** Role-based access, hashed passwords, and flag verification.

---

## Screenshots 🖼️
 
<img width="1592" height="743" alt="image" src="https://github.com/user-attachments/assets/686438f5-45ba-4ae5-a2c4-449cf452fc32" />

---

## Installation & Setup 💻

1. **Clone the repository**
```bash
git clone https://github.com/your-username/IKSC-CTF.git
cd IKSC-CTF
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt
python app.py

