# 🧠 NotionX — Smart Member Directory with Notion

Welcome to **NotionX**, a Django-based web app that allows users to submit and manage their professional profiles. Each profile is stored in a local database and also synced seamlessly to a **Notion database** using the official Notion API.

Built with ❤️ by Serendipity-Scribe for a hackathon challenge.

---

## 🚀 Features

- 🔗 Two-way sync: Data saved in both SQL and Notion.
- 📄 Submit profiles with bio, skills, availability, and links.
- 📝 Edit or delete profiles (reflects in Notion too).
- 🌙 Dark mode toggle with Bootstrap 5.
- 🧭 Responsive layout with clean navigation and footer.
- ☁️ Ready for deployment (Heroku/Vercel/Render compatible).
- 🔒 Secrets managed via `.env`.

---

## 🛠️ Tech Stack

- **Backend**: Django 5
- **Frontend**: Bootstrap 5, HTML, Django templates
- **Database**: SQLite (default), extendable to PostgreSQL
- **External API**: Notion API (v1)
- **Styling**: Bootstrap + custom CSS
- **Version Control**: Git & GitHub

---

## 🧪 Local Setup

```bash
# Clone the repo
git clone https://github.com/Serendipity-scribe-dev/Notion-API-Hackathon
cd Notion-API-Hackathon

# Create virtual environment
python -m venv env
source env/bin/activate  # or `env\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Add environment variables (see below)
cp .env.example .env

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

---

# 🔐 Environment Variables (.env)

Make sure to set the following in a .env file:

NOTION_API_KEY=your-secret-notion-api-key
NOTION_DB_ID=your-notion-database-id

---

# ⚙️ Automating the Notion Database

Can this app automatically create a Notion database with columns?

No, this app assumes the database already exists in your Notion workspace. You'll need to:

1.Manually create a Notion database.

2.Add these columns:

    Name (title)

    Bio (rich text)

    Skills (multi-select)

    Availability (select)

    Location (rich text or text)

    Links (text or rich text)

    Submitted At (date)

3.Copy the Database ID from the URL and paste it in your .env.

---

# 🤝 Contributing

PRs and issues are welcome! If you're using this for learning or want to adapt it, feel free to fork.

---

# 📜 License

This project is licensed under the MIT License.

---

# 💖 Made with Love

Made with 🖤 by Serendipity-Scribe

---

Let me know if you want a `.env.example` file too, or help pushing to GitHub!
