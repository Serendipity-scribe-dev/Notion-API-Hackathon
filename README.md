# 🧠 NotionX — Smart Member Directory with Notion

Welcome to **NotionX**, a Django-based web app that allows users to effortlessly **submit, edit, and manage professional profiles**, all while syncing them in real-time to a Notion database using the official Notion API.

Built with ❤️ by Serendipity-Scribe for a hackathon challenge.

---

## 🚀 Features

- 🔗 Two-way sync: Data saved in both SQL and Notion.
- 📄 Profile submission made simple: Users can add their name, bio, skills, availability, location, and links.
- 🔍 Smart Member Directory: Display profiles as stylish cards, complete with filtering and tag support via Notion's multi-select fields.
- 📝 Edit or delete profiles (reflects in Notion too).
- 🌙 Dark mode toggle with Bootstrap 5.
- 🧭 Responsive layout with clean navigation and footer.
- 🔄 Streamlined onboarding: The app serves as an automated form for new members to onboard themselves — no manual entry needed!
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
git clone https://github.com/Serendipity-scribe-dev/Notion-API-Hackathon.git
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

# 💡 What Problem Does It Solve?

**Manual onboarding is outdated.**
NotionX automates the process of gathering new member details and organizing them beautifully inside Notion.

It eliminates:

- Back-and-forth DMs or emails

- Copy-pasting profiles into Notion

- Losing track of who's available and what they do

And enables:

- A real-time directory with filters and tags

- Easy updates (just edit your info on the site!)

- A single source of truth for your team or community

Whether you're building a team, organizing a talent pool, or managing contributors — **NotionX scales your onboarding and directory workflow**.

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

2.Add these columns (Field , Type):

- Name (title)

- Bio (text)

- Skills (multi-select)

- Availability (select)

- Location (text)

- Links (text)

- Submitted At (date)

  3.Go to https://www.notion.so/my-integrations, create a new interation, copy the **Internal Integration Secret** & paste in .env as NOTION_API_KEY.

  4.Come to your Notion Database, go to options and select connections. Add your integration as Connections.

  5.Copy the Database ID from the URL (💡The part right after notion.so/ and before the ? is the Database ID) and paste it in your .env as NOTION_DB_ID.

---

# 🤝 Contributing

PRs and issues are welcome! If you're using this for learning or want to adapt it, feel free to fork.

---

# 📜 License

This project is licensed under the MIT License.

---

# 💖 Made with Love

Made with ❤️ by Serendipity-Scribe

---

Let me know if you want a `.env.example` file too, or help pushing to GitHub!
