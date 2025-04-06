from django.shortcuts import render, redirect, get_object_or_404
from .forms import MemberProfileForm
from .models import MemberProfile
from .notion import add_member_to_notion, delete_member_from_notion,update_member_in_notion
from django.utils import timezone

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
            return redirect('directory')
    else:
        form = MemberProfileForm()
    return render(request, 'submit_profile.html', {'form': form})

def delete_profile(request, pk):
    profile = get_object_or_404(MemberProfile, pk=pk)

    # Archive the Notion page if it exists
    if profile.notion_page_id:
        try:
            add_member_to_notion.pages.update(page_id=profile.notion_page_id, archived=True)
        except Exception as e:
            print("Failed to archive in Notion:", e)
    profile.delete()
    return redirect('directory')

def member_directory(request):
    members = MemberProfile.objects.all().order_by('-submitted_at')
    return render(request, 'member_directory.html', {'members': members})

def delete_profile(request, pk):
    profile = get_object_or_404(MemberProfile, id=pk)
    print("Notion Page ID:", profile.notion_page_id)  # Add this line

    # Call Notion API to archive the page
    delete_member_from_notion(profile.notion_page_id)

    # Then delete from your local DB
    profile.delete()
    return redirect('directory')

def edit_profile(request, id):
    member = get_object_or_404(MemberProfile, id=id)

    if request.method == 'POST':
        form = MemberProfileForm(request.POST, instance=member)
        if form.is_valid():
            updated_member = form.save(commit=False)
            updated_member.submitted_at = timezone.now()
            updated_member.save()
            update_member_in_notion(updated_member)  # update in Notion
            return redirect('directory')  # redirect to wherever you list profiles
    else:
        form = MemberProfileForm(instance=member)

    return render(request, 'edit_profile.html', {'form': form})