# Annotation Daily HQ

A beautiful, local-only web application for daily work logging and team performance tracking for data annotation teams.

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)

## Features

### Annotator Portal (`/log`)
- Quick and easy daily work logging
- Track images annotated, hours spent, task types
- Report challenges and suggestions
- Clean, minimal form design

### Team Lead Dashboard (`/dashboard`)
- Real-time KPI metrics (total images, hours, active annotators)
- Interactive charts (images per annotator, per project)
- Summary tables with filtering
- Dedicated challenges & suggestions view
- Export to CSV or Excel

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this project**

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

5. **Open your browser**
   - Annotator Portal: http://localhost:8000/log
   - Team Dashboard: http://localhost:8000/dashboard

## Project Structure

```
workreport/
├── app/
│   ├── main.py              # FastAPI application entry
│   ├── config.py            # Configuration settings
│   ├── database.py          # SQLAlchemy setup
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic validation schemas
│   ├── routes/              # HTTP route handlers
│   ├── services/            # Business logic
│   └── templates/           # Jinja2 HTML templates
├── static/
│   ├── css/output.css       # Compiled TailwindCSS
│   └── js/chart.min.js      # Chart.js library
├── data/
│   └── workreport.db        # SQLite database (auto-created)
├── requirements.txt         # Python dependencies
├── run.py                   # Launcher script
└── README.md
```

## Usage

### For Annotators

1. Navigate to http://localhost:8000/log
2. Fill in your daily work details:
   - Date (defaults to today)
   - Your name
   - Project name
   - Task type (Bounding Boxes, Segmentation, Classification, QA/Review, Other)
   - Images completed
   - Hours spent
   - Status
   - (Optional) Challenges, suggestions, notes
3. Click "Submit Work Log"
4. Use "Log Another Entry" for multiple projects

### For Team Leads

1. Navigate to http://localhost:8000/dashboard
2. Use filters to select:
   - Date
   - Specific projects
   - Specific annotators
3. Review:
   - KPI summary cards
   - Charts showing distribution
   - Detailed entry tables
   - Challenges & suggestions
4. Export reports using CSV or Excel buttons

## Configuration

### Database Location
By default, the SQLite database is stored in `data/workreport.db`. To change this, edit `app/config.py`:

```python
DATABASE_URL = f"sqlite:///{DATA_DIR / 'workreport.db'}"
```

### Task Types
Modify available task types in `app/config.py`:

```python
TASK_TYPES = [
    "Bounding Boxes",
    "Segmentation",
    "Classification",
    "QA / Review",
    "Other"
]
```

### Status Options
Modify status options in `app/config.py`:

```python
STATUS_OPTIONS = [
    "Completed",
    "Partially completed",
    "Blocked"
]
```

## Development

### Running with auto-reload
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Rebuilding TailwindCSS (if modifying styles)
```bash
npm install
npm run build:css
```

Or for development with watch mode:
```bash
npm run watch:css
```

## Network Access

To allow other computers on your local network to access the app:

1. Find your computer's local IP address
2. Run the app (it binds to `0.0.0.0` by default)
3. Other users can access via `http://YOUR_IP:8000/log`

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Jinja2 templates, TailwindCSS
- **Charts**: Chart.js
- **Server**: Uvicorn

## License

MIT License - Feel free to use and modify for your team's needs.

---

**Annotation Daily HQ** — Simple. Beautiful. Local.

