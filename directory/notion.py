from notion_client import Client
import os
from dotenv import load_dotenv
load_dotenv()

notion = Client(auth=os.getenv("NOTION_API_KEY"))
NOTION_DB_ID = os.getenv("NOTION_DB_ID")

def add_member_to_notion(profile):
        page = notion.pages.create(
            parent={"database_id": NOTION_DB_ID},
            properties={
                "Name": {"title": [{"text": {"content": profile.name}}]},
                "Bio": {"rich_text": [{"text": {"content": profile.bio}}]},
                "Skills": {
                    "multi_select": [{"name": skill.strip()} for skill in profile.skills.split(",")]
                },
                "Availability": {"select": {"name": profile.availability}},
                "Location": {"rich_text": [{"text": {"content": profile.location or ""}}]},
                "Links": {"rich_text": [{"text": {"content": profile.links or "N/A"}}]},
                "Submitted At":{"date" : { "start": profile.submitted_at.isoformat()}}
            },
        )
        print("✅ Notion Page Created. ID:", page.get("id"))
        return page["id"]

def delete_member_from_notion(page_id):
    print(f"Archiving page in Notion: {page_id}")
    try:
        if page_id:
            notion.pages.update(
                page_id=page_id,
                archived=True  # This marks the page as deleted in Notion
            )
        print(f"✅ Page {page_id} archived successfully.")
    except Exception as e:
        print(f"❌ Failed to archive page {page_id}: {e}")


def update_member_in_notion(profile):
    if not profile.notion_page_id:
        print("❌ No Notion Page ID found. Skipping update.")
        return

    try:
        notion.pages.update(
            page_id=profile.notion_page_id,
            properties={
                "Name": {"title": [{"text": {"content": profile.name}}]},
                "Bio": {"rich_text": [{"text": {"content": profile.bio}}]},
                "Skills": {
                    "multi_select": [{"name": skill.strip()} for skill in profile.skills.split(",")]
                },
                "Availability": {"select": {"name": profile.availability}},
                "Location": {"rich_text": [{"text": {"content": profile.location or ""}}]},
                "Links": {"rich_text": [{"text": {"content": profile.links or ""}}]},
                "Submitted At": {"date": {"start": profile.submitted_at.isoformat()}}
            }
        )
        print(f"✅ Notion page {profile.notion_page_id} updated successfully.")
    except Exception as e:
        print(f"❌ Failed to update Notion page: {e}")


        