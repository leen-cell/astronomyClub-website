# Astronomy Club Website 

A Flask-based web application to manage an astronomy club’s members, events, telescopes, research projects, resources and photos — backed by a MySQL database.

---

##  Features

- **Public Pages**  
  - Browse **members**, **events**, **telescopes**, **research projects**, **resources**, and **photo gallery**  
  - Responsive design with Lightbox, Owl Carousel, Slick Slider, and custom CSS  
- **Admin Panel**  
  - Secure login at `/admin-login`  
  - Dashboard overview of all entities  
  - Create / Read / Update / Delete members, events, resources, researches, photos  
- **RESTful APIs**  
  - JSON endpoints for inserting members, events, etc.  
  - Client-side AJAX calls (via `static/assets/js/custom.js`)  
- **MySQL Backend**  
  - Full schema and seed data in `database/database.sql`  
  - Tables: `members`, `theevents`, `telescopes`, `research`, `resources`, `photo`, `member2research`  

---

##  Technology Stack

- **Backend**: Python 3, Flask  
- **Database**: MySQL (via `mysql-connector-python`)  
- **Frontend**: HTML5, CSS3, JavaScript, jQuery, Lightbox, Owl Carousel, Slick Slider  
- **Templating**: Jinja2 (`templates/*.html`)  
- **Static Assets**: `static/assets/{css,js,images,fonts,pdfs}`  

---

##  Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/leen-cell/astronomyclub-website.git
cd astronomyclub-website

### 2. Set up Python environment
```bash
python3 -m venv venv
source venv/bin/activate        # On Linux/macOS
venv\Scripts\activate           # On Windows
pip install -r requirements.txt
```

> If `requirements.txt` doesn’t exist, you can install manually:
```bash
pip install flask mysql-connector-python
```

### 3. Set up MySQL database

1. Create a new MySQL database (e.g. `astroclub`).
2. Import the schema:
   ```bash
   mysql -u your_username -p astroclub < database/database.sql
   ```
3. Open `app.py` and edit the database configuration:
   ```python
   db_config = {
       'host': 'localhost',
       'user': 'your_username',
       'password': 'your_password',
       'database': 'astroclub'
   }
   ```

### 4. Run the app
```bash
flask run
```

Then visit: [http://localhost:5000](http://localhost:5000)

---

## 📁 Project Structure

```
astronomyclub-website/
├── app.py
├── database/
│   └── database.sql
├── static/
│   └── assets/
│       ├── css/
│       ├── js/
│       ├── images/
│       ├── fonts/
│       └── pdfs/
├── templates/
│   ├── index.html
│   ├── admin-login.html
│   ├── admin-dashboard.html
│   ├── members.html
│   └── ...
├── .gitignore
├── README.md
└── requirements.txt  ← optional
```

---

## Author

**Leen Alqazaqi**  
Computer Engineering  
Project for Astronomy Club 🌌
