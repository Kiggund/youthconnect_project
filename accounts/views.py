from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.contrib import messages
from accounts.forms import UserEditForm, ProfileEditForm
import os
import traceback

@login_required
def edit_account(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            try:
                user_form.save()

                profile = profile_form.save(commit=False)
                new_image = request.FILES.get('profile_pic')
                old_image = request.user.profile.profile_pic

                # Log uploaded image
                if new_image:
                    print(f"[DEBUG] New image uploaded: {new_image.name}")
                else:
                    print("[DEBUG] No new image uploaded.")

                # Delete old profile image if new one provided and old isn't default
                if new_image and old_image and old_image.name != 'default.jpg':
                    try:
                        if os.path.exists(old_image.path):
                            print(f"[DEBUG] Deleting old image: {old_image.path}")
                            default_storage.delete(old_image.path)
                    except Exception as e:
                        print("[ERROR] Failed to delete old image:", e)
                        traceback.print_exc()

                if new_image:
                    profile.profile_pic = new_image

                profile.user = request.user
                profile.save()

                print(f"[SUCCESS] Profile saved. Image: {profile.profile_pic.url}")
                messages.success(request, "Profile updated successfully.")
                return redirect('profile')

            except Exception as e:
                print("[ERROR] Exception during save:")
                traceback.print_exc()
                messages.error(request, "Something went wrong while updating your profile.")

        else:
            print("[FORM ERROR] User form errors:", user_form.errors)
            print("[FORM ERROR] Profile form errors:", profile_form.errors)

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'accounts/edit_account.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {
        'profile': request.user.profile
    })
