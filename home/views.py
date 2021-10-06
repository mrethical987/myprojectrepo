from home.models import Contact
from django.contrib import messages
from django.shortcuts import render , HttpResponse, redirect
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login, logout
from blog.models import Post
from math import ceil

# Create your views here.
def home(request):
    allposts = Post.objects.all()
    n = len(allposts)
    nSlides = n//4 + ceil ((n/4) - (n//4))
    context = {'no_of_slides':nSlides,'range':range(1,nSlides), 'allposts':allposts}
    return render(request, 'home/home.html', context)
    


def addPost(request):
    if request.user.is_authenticated:  
        allposts = Post.objects.all()
        context = {'allposts':allposts}
        return render(request, 'home/addPost.html', context)



def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        if len(name)<3 or len(email)<3 or len(phone)<10 or len(content)<5:
            messages.error(request, "Please fill correct data")
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your query has been sucessfully sent")
    return render(request, 'home/contact.html')


def about(request):
    return render(request, 'home/about.html')

def search(request):
    query = request.GET.get('query')
    if len(query)>80:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent, allPostsAuthor)

    if allPosts.count() == 0:
        messages.warning(request, "no search results found Please try again")
    params = {'allPosts': allPosts, 'query':query}
    return render(request, 'home/search.html', params)

def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if len(username) > 10:
            messages.error(request, "Sorry Username must be under 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Sorry Username must only contain Numbers and Character")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Sorry your Passwords does not match")
            return redirect('home')
    

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        user = myuser.save()
        
        messages.success(request, "your weThink account has been created successfully, now to your weThink account to start your journey sucessfully")
        return redirect('home')


    else:
        return HttpResponse('404-not found')


def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername ,password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect('home')

        else:
            messages.error(request, "Invalid Credentials, please try again !!!")
            return redirect('home')

def handleLogout(request):
    logout(request)    
    messages.success(request, "Logged out successfully")
    return redirect('home')

