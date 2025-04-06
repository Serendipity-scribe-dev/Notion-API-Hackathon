from notion_client import Client

# Get credentials from user input
api_key = input("🔑 Enter your Notion API Key: ").strip()
db_id = input("🗂️  Enter your Notion Database ID: ").strip()

notion = Client(auth=api_key)

try:
    response = notion.databases.retrieve(database_id=db_id)
    print("✅ Successfully connected to Notion Database!")
    print("📄 Database Title:", response['title'][0]['text']['content'])
except Exception as e:
    print("❌ Failed to connect to Notion:")
    print(e)
