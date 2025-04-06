from django.shortcuts import render, redirect, get_object_or_404
from .forms import MemberProfileForm,NotionConfigForm
from .models import MemberProfile, NotionConfig
from .notion import add_member_to_notion, delete_member_from_notion,update_member_in_notion
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from notion_client import Client


def home(request):
    return render(request, 'home.html')
    
def submit_profile(request):
    if request.method == 'POST':
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
    return render(request, 'submit_profile.html', {'form': form})

def delete_profile(request, pk):
    profile = get_object_or_404(MemberProfile, pk=pk)

    # Archive the Notion page if it exists
    if profile.notion_page_id:
        try:
            delete_member_from_notion(profile.notion_page_id)
        except Exception as e:
            print("Failed to archive in Notion:", e)
    profile.delete()
    return redirect('directory')

def delete_member_from_notion(page_id):
    notion, _ = get_notion_client()
    notion.pages.update(page_id=page_id, archived=True)


def edit_profile(request, id):
    member = get_object_or_404(MemberProfile, id=id)
    print("🔍 Original Notion Page ID (from DB):", member.notion_page_id)

    if request.method == 'POST':
        form = MemberProfileForm(request.POST, instance=member)
        if form.is_valid():
            updated_member = form.save(commit=False)

            # Just to be safe
            if not updated_member.notion_page_id:
                updated_member.notion_page_id = member.notion_page_id

            print("✅ Notion Page ID before save:", updated_member.notion_page_id)

            updated_member.submitted_at = timezone.now()
            updated_member.save()

            if updated_member.notion_page_id:
                print("🔄 Updating Notion page:", updated_member.notion_page_id)
                update_member_in_notion(updated_member)
            else:
                print("❌ No Notion Page ID found. Skipping update.")

            return redirect('directory')
    else:
        form = MemberProfileForm(instance=member)

    return render(request, 'edit_profile.html', {'form': form})

from django.db.models import Q

def member_directory(request):
    query = request.GET.get('q', '')
    availability = request.GET.get('availability', '')
    skill = request.GET.get('skill', '')

    members = MemberProfile.objects.all().order_by('-submitted_at')

    # Filter by name or bio if query exists
    if query:
        members = members.filter(
            Q(name__icontains=query) | Q(bio__icontains=query)
        )

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