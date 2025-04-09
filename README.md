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

title: 🚀 NotionX Setup Guide
description: Build dynamic profile submission/editing synced with your Notion database.
steps:

- step: 🔐 Set up Environment Variables
  details: |
  Create a `.env` file in your root directory and add:

  ```env
  NOTION_API_KEY=your-secret-notion-api-key
  NOTION_DB_ID=your-notion-database-id
  ```

- step: 🏗️ Create a Notion Database (Once Only)
  details: |

  1. Open Notion and create a new **Table database**.
  2. Click `Share` → `Connections` → Add the integration you created at [Notion Integrations](https://www.notion.so/my-integrations).
  3. Copy the **Database ID** from the URL (after notion.so till the ?)
  4. Paste it into your `.env` as `NOTION_DB_ID`.

- step: 🧠 How Automation Works
  details: |
  ✅ Once you've connected your Notion DB and Integration:

  - As soon as you start **adding new columns** in your Notion database (e.g., `Email`, `Portfolio`, `Phone Number`), they will **automatically appear** in your form.
  - The field types (like `title`, `text`, `multi_select`, `select`, `checkbox`, `email`, etc.) are **auto-detected** and rendered dynamically in the form.
  - Any `select` or `multi_select` options defined in Notion are turned into proper dropdowns / checkbox lists for input.
  - The app is smart enough to:
    - 📝 Submit data to Notion
    - ✏️ Edit data (also synced back to Notion)
    - 🗑️ Delete entries (archives them in Notion)

  No need to hardcode form fields ever again.

- step: 🔁 Supported Notion Column Types
  list:

  - title
  - rich_text
  - multi_select
  - select
  - checkbox
  - phone_number
  - email
  - url
  - date

- step: 📦 Run the App
  details: |
  ```
  python manage.py runserver
  ```

---

### 📺 Demo

[![Watch the video](https://cdn.loom.com/sessions/thumbnails/632471c078dc47e7acd41f063dc0c12c-dd7f367267937079-full-play.gif)](https://www.loom.com/share/632471c078dc47e7acd41f063dc0c12c)

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
