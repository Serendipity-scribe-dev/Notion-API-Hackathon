from notion_client import Client
from .models import NotionConfig
from collections import OrderedDict
#import os
from dotenv import load_dotenv
load_dotenv()

# notion = Client(auth=os.getenv("NOTION_API_KEY"))
# NOTION_DB_ID = os.getenv("NOTION_DB_ID")

def get_notion_client():
    config = NotionConfig.objects.first()
    if not config:
        raise Exception("❌ Notion configuration not found.")
    return Client(auth=config.api_key), config.database_id

def add_member_to_notion(profile):
        notion, NOTION_DB_ID = get_notion_client()
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
    try:
        notion, _ = get_notion_client()
    except Exception as e:
        print(f"❌ Failed to get Notion client: {e}")
        return

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
    from .notion import fetch_notion_schema
    try:
        notion, db_id = get_notion_client()
    except Exception as e:
        print("❌ Failed to get Notion client:", e)
        return

    if not profile.notion_page_id:
        print("❌ No Notion Page ID found. Skipping update.")
        return

    try:
        schema = fetch_notion_schema()
        properties = {}

        for field_name, field_type in schema.items():
            value = profile.data.get(field_name)

            if not value:
                continue

            if field_type == "title":
                properties[field_name] = {
                    "title": [{"text": {"content": value}}]
                }
            elif field_type == "rich_text":
                properties[field_name] = {
                    "rich_text": [{"text": {"content": value}}]
                }
            elif field_type == "select":
                properties[field_name] = {
                    "select": {"name": value}
                }
            elif field_type == "multi_select":
                properties[field_name] = {
                    "multi_select": [{"name": s.strip()} for s in value.split(",")]
                }
            elif field_type == "date":
                properties[field_name] = {
                    "date": {"start": value} if value else None
                }
            else:
                # fallback to rich_text
                properties[field_name] = {
                    "rich_text": [{"text": {"content": str(value)}}]
                }

        notion.pages.update(
            page_id=profile.notion_page_id,
            properties=properties
        )
        print(f"✅ Notion page {profile.notion_page_id} updated successfully.")
    except Exception as e:
        print(f"❌ Failed to update Notion page: {e}")

def fetch_notion_schema():
    notion, db_id = get_notion_client()
    response = notion.databases.retrieve(database_id=db_id)
    properties = response["properties"]
    schema = OrderedDict()

    # Separate out "Name" field
    name_field = None
    other_fields = []

    # Ensure "Name" comes first
    if "Name" in properties:
        schema["Name"] = properties["Name"]["type"]

    for name, prop in properties.items():
        if name != "Name":
            schema[name] = prop["type"]

    # for name, prop in properties.items():
    #     if name.lower() == "name":
    #         name_field = (name, prop["type"])
    #     else:
    #         # Some Notion SDKs do not expose created_time — so fallback if missing
    #         created = prop.get("created_time")
    #         other_fields.append((name, prop["type"], created))

    # Sort by created_time (fallback to alphabetically if not available)
    other_fields.sort(key=lambda x: x[2] if x[2] else x[0])

    # Build schema dict with "Name" first
    
    if name_field:
        schema[name_field[0]] = name_field[1]

    for name, field_type, _ in other_fields:
        schema[name] = field_type

    return schema