# Future Factory

A marketing and lead-generation website built for a digital agency — designed to showcase services and turn visitors into qualified leads.

## Features

- **Home, Services, About, Contact, and Leadership pages**
- **Lead capture form** for prospective clients
- **Admin dashboard notifications** — push notifications alert the admin whenever a new lead comes in, so nothing gets missed

## Tech Stack

- **Backend:** Django, Python
- **Frontend:** HTML, CSS, JavaScript

## Getting Started

### Prerequisites
- Python 3.11+
- pip

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/ali-sher-makki/futurefactory.git
   cd futurefactory
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations and run the development server:
   ```
   python manage.py migrate
   python manage.py runserver
   ```

5. Visit `http://127.0.0.1:8000/` in your browser.

> **Note:** if the project uses a `.env` file for settings like `SECRET_KEY` or email credentials, create one in the project root before running migrations — check `settings.py` for the exact variable names it expects.

## Author

**Ali Sher Makki**
- GitHub: [github.com/ali-sher-makki](https://github.com/ali-sher-makki)
- LinkedIn: [linkedin.com/in/ali-sher-0a2a78266](https://www.linkedin.com/in/ali-sher-0a2a78266)
- Upwork: [upwork.com/freelancers/~017c5d404ff0c6ab67](https://www.upwork.com/freelancers/~017c5d404ff0c6ab67)

This project is shared for portfolio and demonstration purposes.
