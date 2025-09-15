from django.shortcuts import render, redirect, get_object_or_404
from .models import UserPost, User, UserProfile, ChildComment, Comment
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm, PostAddForm
import datetime
from django.db.models import Q


def user_profile_page(request, username):
    user = get_object_or_404(User, username=username)
    pk = user.id
    current_user = UserProfile.objects.get(id=pk)
    posts = UserPost.objects.filter(user=current_user.user).order_by('-date_time')
    return render(request, "user_profile_page.html", {"current_user": current_user, "posts":posts})

def tag(request, tag_item):
    tag = UserPost.objects.filter(Q(tag_category__name=tag_item)).distinct()
    return render(request, "tag.html", {"tag":tag})

def search_tag(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        searched = UserPost.objects.filter(Q(post_title__icontains=searched) | Q(tag_category__name__contains=searched))
        searched = searched.distinct()

        if not searched:
            messages.success(request, "No tag found, Search Another...")
            return render(request, "search_tag.html", {})
        else:
            return render(request, "search_tag.html", {"searched":searched})
    
    else:
        return render(request, "search_tag.html", {})
    
def search_user(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        searched = UserProfile.objects.filter(user__username__icontains=searched)
        searched = searched.distinct()

        if not searched:
            messages.success(request, "No user found, Search Another...")
            return render(request, "search_user.html", {})
        else:
            return render(request, "search_user.html", {"searched":searched})
    
    else:
        return render(request, "search_user.html", {})

def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            post_form = PostAddForm(request.POST, request.FILES)

            if post_form.is_valid():
                # Use form.save() with commit=False to get the instance without saving
                create_post = post_form.save(commit=False)
                
                # Set additional fields that aren't in the form
                create_post.user = request.user
                create_post.date_time = datetime.datetime.now()
                create_post.like = 0
                create_post.comment_count = 0
                
                # Save the instance first
                create_post.save()
                
                # Save ManyToMany relationships (this handles tag_category automatically)
                post_form.save_m2m()

                return redirect("home") 
        else:
            # FIX: Instantiate the form properly for GET requests
            post_form = PostAddForm()  # Add parentheses here!
            
        return render(request, "add_post.html", {"post_form": post_form})
    else:
        messages.success(request, "You must have been logged in first...")
        return redirect("login")

def update_info(request):
    if request.user.is_authenticated:
        current_user = UserProfile.objects.get(user__id=request.user.id)
        info_form = UserInfoForm(request.POST or None, request.FILES or None, instance=current_user)

        if info_form.is_valid():
            info_form.save()

            messages.success(request, ("Your Info Has Been Updated..."))
            return redirect('home')
        
        else:
            return render(request, "update_info.html", {"info_form":info_form, "current_user":current_user})
        
    else:
        messages.success(request, "You must be logged in at first...")
        return redirect("login")

def update_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # User object goes FIRST, then POST data
            password_form = ChangePasswordForm(request.user, request.POST)
            
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password successfully updated!")
                return redirect("home")
        else:
            # For GET request, only pass the user
            password_form = ChangePasswordForm(request.user)
        
        return render(request, "update_password.html", {'password_form': password_form})
    else:
        messages.error(request, "You must be logged in first.")
        return redirect("login")

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, "User Info Successfully Updated...")
            return redirect("home")
        
        else:
            return render(request, "update_user.html", {'user_form':user_form})
    else:
        messages.success(request, "You must be logged in at first...")
        return redirect("login")
        
def signup_user(request):
    signup_form = SignUpForm
    if request.method == "POST":
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()

            username = signup_form.cleaned_data["username"]
            password = signup_form.cleaned_data["password1"]

            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ("You have been registered successfully..."))
            return redirect('home')
        else:
            messages.success(request, ("There is a problem, please try again..."))
            return redirect('signup')
    else:
        return render(request, "signup.html", {'signup_form':signup_form})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in..."))
            return redirect('home')
        else:
            messages.success(request, ("There is a problem, please try again..."))
            return redirect('login')
    else:
        return render(request, "login.html", {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out..."))
    return redirect('home')

def post(request, pk):
    post = UserPost.objects.get(id=pk)
    comments = Comment.objects.filter(user_post=post).order_by("-id")
    current_user_posts = UserPost.objects.filter(user=post.user).exclude(pk=pk).order_by('-date_time')[:5]
    usr = UserProfile.objects.get(user=post.user)

    if request.method == "POST":
        if request.user.is_authenticated:
            current_user = UserProfile.objects.get(user__id=request.user.id)
            comment_text = request.POST.get("comment", "").strip()
            parent_comment_id = request.POST.get("parent_comment_id")

            if comment_text:
                if parent_comment_id:  # This is a child comment
                    try:
                        parent_comment = Comment.objects.get(id=parent_comment_id)
                        create_child_comment = ChildComment(
                            user_post=post, 
                            commenter_name=current_user, 
                            parent_comment=parent_comment, 
                            child_comment=comment_text
                        )
                        create_child_comment.save()
                    except Comment.DoesNotExist:
                        messages.error(request, "Parent comment not found.")
                else:  # This is a parent comment
                    create_comment = Comment(
                        user_post=post, 
                        commenter_name=current_user, 
                        comment=comment_text
                    )
                    create_comment.save()
                
                return redirect('post', pk=pk)
            else:
                messages.error(request, "Your comment cannot be empty...")
                return redirect('post', pk=pk)
        else:
            messages.success(request, "You Have To Login First...")
            return redirect("login")
    
    # Get child comments for each parent comment
    comments_with_children = []
    for comment in comments:
        child_comments = ChildComment.objects.filter(parent_comment=comment)
        comments_with_children.append({
            'comment': comment,
            'child_comments': child_comments
        })
    
    return render(request, "post.html", {
        "post": post, 
        "comments_with_children": comments_with_children,
        "current_user_posts": current_user_posts,
        "usr": usr
    })

def home(request):
    posts = UserPost.objects.order_by('-id')
    return render(request, "home.html", {"posts":posts})



