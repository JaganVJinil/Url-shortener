from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.views.decorators.cache import never_cache
from .forms import URLForm, SignupForm
from .models import ShortURL
import re

@never_cache
def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('url_list')
        messages.error(request, 'Invalid credentials')
    return render(request, 'core/login.html')

@never_cache
def logout_view(request):
    logout(request)
    return redirect('login')

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('url_list')
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})

@never_cache
@login_required
def add_url(request):
    if ShortURL.objects.filter(user=request.user).count() >= 5:
        messages.error(request, "ERROR, only 5 urls can be created ") 
        return redirect('url_list')

    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.save(commit=False)
            url.user = request.user
            url.save()
            return redirect('url_list')
    else:
        form = URLForm()
    return render(request, 'core/add_url.html', {'form': form})

@never_cache
@login_required
def url_list(request):
    query = request.GET.get('q')
    urls = ShortURL.objects.filter(user=request.user)

    if query:
        urls = urls.filter(Q(title__icontains=query) | Q(original_url__icontains=query))

    paginator = Paginator(urls.order_by('-created_at'), 3)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'core/url_list.html', {'urls': page_obj})

@never_cache
@login_required
def edit_url(request, pk):
    url = get_object_or_404(ShortURL, pk=pk, user=request.user)
    if request.method == 'POST':
        form = URLForm(request.POST, instance=url)
        if form.is_valid():
            form.save()
            return redirect('url_list')
    else:
        form = URLForm(instance=url)
    return render(request, 'core/edit_url.html', {'form': form})

@never_cache
@login_required
def delete_url(request, pk):
    url = get_object_or_404(ShortURL, pk=pk, user=request.user)
    url.delete()
    return redirect('url_list')

def redirect_short_url(request, short_code):
    try:
        short_url = ShortURL.objects.get(short_url=short_code)
        if not re.match(r'^https?://', short_url.original_url):
            short_url.original_url = 'http://' + short_url.original_url
        return HttpResponseRedirect(short_url.original_url)
    except ShortURL.DoesNotExist:
        raise Http404("Short URL not found")
