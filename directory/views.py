from django.shortcuts import render, redirect, get_object_or_404
from .forms import MemberProfileForm,NotionConfigForm,get_dynamic_profile_form
from .models import MemberProfile, NotionConfig,DynamicProfile,get_dynamic_model
from .notion import add_member_to_notion, delete_member_from_notion,update_member_in_notion,fetch_notion_schema, get_notion_client
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from notion_client import Client
import datetime


def home(request):
    return render(request, 'home.html')
    
def submit_profile(request):

    schema = fetch_notion_schema()
    DynamicProfileForm = get_dynamic_profile_form(schema)

    # Optional: Set default skills you want for the multi-select
    #skill_options = ["React", "JavaScript", "Python", "UI Design", "Figma"]

    if request.method == 'POST':
        form = DynamicProfileForm(request.POST)
        if form.is_valid():
            profile_data = {}
            for key, value in form.cleaned_data.items():
                if isinstance(value, (datetime.date, datetime.datetime)):
                    profile_data[key] = value.isoformat()  # "YYYY-MM-DD"
                elif schema[key] == "date" and not value:
                    # Auto-fill if date is required but not given
                    profile_data[key] = datetime.date.today().isoformat()
                else:
                    profile_data[key] = value
            profile = DynamicProfile.objects.create(data=profile_data)
            
            # Create page in Notion
            notion, db_id = get_notion_client()
            properties = {}

            for key, value in profile_data.items():
                type_ = schema[key]
                if type_ == "title":
                    properties[key] = {"title": [{"text": {"content": value}}]}
                elif type_ == "rich_text":
                    
                    properties[key] = {"rich_text": [{"text": {"content": value}}]}
                elif type_ == "multi_select":
                    if value:  # Only send if value is not empty
                        multi_values = [v.strip() for v in value.split(",") if v.strip()]
                        properties[key] = {
                        "multi_select": [{"name": v} for v in multi_values]
                        }
                elif type_ == "select":
                    if value:  # Only send if value is not empty
                        properties[key] = {"select": {"name": value}}
                elif type_ == "date":
                    properties[key] = {"date": {"start": str(value)}}
                elif type_ == "checkbox":
                    properties[key] = {"checkbox": bool(value)}
                elif type_ == "url":
                    if value:
                        properties[key] = {"url": value}
                elif type_ == "phone_number":
                    if value:
                        properties[key] = {"phone_number": value}
                elif type_ == "email":
                    if value:
                        properties[key] = {"email": value}
                else:
                    properties[key] = {"rich_text": [{"text": {"content": value}}]}

            notion_page = notion.pages.create(parent={"database_id": db_id}, properties=properties)
            profile.notion_page_id = notion_page["id"]
            profile.save()

            return redirect("directory")  # or success page
    else:
        form = DynamicProfileForm()

    return render(request, 'submit_profile.html', {'form': form})

    """ if request.method == 'POST':
        form = MemberProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            # 🔽 Add this part BELOW the initial save
            profile.submitted_at = timezone.now()
            notion_page_id = add_member_to_notion(profile)
            profile.notion_page_id = notion_page_id
            profile.save()
            print("✅ Saved to DB with Notion Page ID:", profile.notion_page_id)
            return redirect('directory')
    else:
        form = MemberProfileForm()
    return render(request, 'submit_profile.html', {'form': form}) """



def delete_profile(request, pk):
    DynamicProfile = get_dynamic_model()
    profile = get_object_or_404(DynamicProfile, pk=pk)

    # Archive the Notion page if it exists
    if profile.notion_page_id:
        try:
            delete_member_from_notion(profile.notion_page_id)
        except Exception as e:
            print("Failed to archive in Notion:", e)
    profile.delete()
    messages.success(request, "Profile deleted successfully!")
    return redirect('directory')

def delete_member_from_notion(page_id):
    notion, _ = get_notion_client()
    notion.pages.update(page_id=page_id, archived=True)


def update_member_in_notion(profile, schema):
    notion, db_id = get_notion_client()
    properties = {}

    for key, value in profile.data.items():
        field_type = schema.get(key)

        if field_type == "title":
            properties[key] = {"title": [{"text": {"content": value}}]}

        elif field_type == "rich_text":
            properties[key] = {"rich_text": [{"text": {"content": value}}]}

        elif field_type == "multi_select":
            if value:
                properties[key] = {
                    "multi_select": [{"name": item.strip()} for item in value.split(",") if item.strip()]
                }

        elif field_type == "select":
            if value:
                properties[key] = {"select": {"name": value}}

        elif field_type == "checkbox":
            properties[key] = {"checkbox": bool(value)}

        elif field_type == "phone_number":
            properties[key] = {"phone_number": value}

        elif field_type == "url":
            properties[key] = {"url": value}

        elif field_type == "email":
            properties[key] = {"email": value}

        elif field_type == "date":
            if value:
                properties[key] = {"date": {"start": str(value)}}

        else:
            properties[key] = {"rich_text": [{"text": {"content": str(value)}}]}

    notion.pages.update(page_id=profile.notion_page_id, properties=properties)


def edit_profile(request, id):
    DynamicProfile = get_dynamic_model()
    profile = get_object_or_404(DynamicProfile, id=id)

    schema = fetch_notion_schema()
    DynamicForm = get_dynamic_profile_form(schema)

    if request.method == 'POST':
        form = DynamicForm(request.POST)
        if form.is_valid():
            updated_data = form.cleaned_data

            # Save updated data to model
            for field, value in updated_data.items():
                if isinstance(value, (datetime.date, datetime.datetime)):
                    profile.data[field] = value.isoformat()
                else:
                    profile.data[field] = value
            profile.save()

            # Update in Notion
            try:
                update_member_in_notion(profile, schema)
                messages.success(request, "Profile updated successfully!")
            except Exception as e:
                messages.error(request, f"❌ Failed to update Notion page: {str(e)}")

            return redirect('directory')
    else:
        form = DynamicForm(initial=profile.data)

    return render(request, 'edit_profile.html', {'form': form})



from django.db.models import Q

def member_directory(request):
    query = request.GET.get('q', '')
    availability = request.GET.get('availability', '')
    skill = request.GET.get('skill', '')
    profiles = DynamicProfile.objects.all().order_by('-submitted_at')

    members = MemberProfile.objects.all().order_by('-submitted_at')

    # Filter by name or bio if query exists
    if query:
        members = members.filter(Q(name__icontains=query) | Q(bio__icontains=query))
        print("Filtered members count:", members.count())  # See if this logs anything

    # Filter by availability
    if availability:
        members = members.filter(availability__iexact=availability)

    # Filter by skill (checking if skill is a substring in the comma-separated skills field)
    if skill:
        members = members.filter(skills__icontains=skill)

    context = {
        'members': members,
        'search_query': query,
        'selected_availability': availability,
        'selected_skill': skill,
        'profiles': profiles,
    }
    return render(request, 'member_directory.html', context)

def setup_notion_config(request):
    notion_name = None
    success = False

    try:
        config = NotionConfig.objects.first()
    except NotionConfig.DoesNotExist:
        config = None

    if request.method == 'POST':
        form = NotionConfigForm(request.POST, instance=config)
        if form.is_valid():
            config = form.save()

            try:
                # Use the Notion API to fetch the database info
                notion = Client(auth=config.api_key)
                db_info = notion.databases.retrieve(config.database_id)
                notion_name = db_info.get("title", [{}])[0].get("text", {}).get("content", "Untitled Database")
                success = True
            except Exception as e:
                print("❌ Failed to fetch Notion DB name:", e)
    else:
        form = NotionConfigForm(instance=config)

    return render(request, 'setup_notion.html', {
        'form': form,
        'success': success,
        'notion_name': notion_name
    })


def get_notion_client():
    config = NotionConfig.objects.first()
    if not config:
        raise Exception("❌ Notion configuration not found.")
    return Client(auth=config.api_key), config.database_id