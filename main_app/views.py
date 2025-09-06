from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Count, Avg
from .models import Game, Category
from .forms import GameForm, CategoryForm

def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def dashboard(request):
    games = Game.objects.filter(owner=request.user)
    total_games = games.count()
    used_categories = games.values('category').distinct().count()
    top_platform = games.values('platform').annotate(count=Count('platform')).order_by('-count').first()
    average_rating = games.aggregate(avg=Avg('rating'))['avg']

    stats = {
        'total_games': total_games,
        'used_categories': used_categories,
        'top_platform': top_platform['platform'] if top_platform else '—',
        'average_rating': round(average_rating, 1) if average_rating else '—',
    }

    return render(request, 'dashboard.html', {'games': games, 'stats': stats})

@login_required
def game_list(request):
    q = request.GET.get('q', '').strip()
    category_id = request.GET.get('category')
    platform = request.GET.get('platform')

    games = Game.objects.filter(owner=request.user)

    if q:
        games = games.filter(name__icontains=q)
    if category_id:
        games = games.filter(category_id=category_id)
    if platform:
        games = games.filter(platform__iexact=platform)

    categories = Category.objects.all()
    platforms = Game.objects.values_list('platform', flat=True).distinct()

    context = {
        'games': games,
        'q': q,
        'categories': categories,
        'platforms': platforms,
        'selected_category': category_id,
        'selected_platform': platform,
    }
    return render(request, 'game_list.html', context)

@login_required
def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'game_detail.html', {'game': game})

@login_required
def game_create(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save(commit=False)
            game.owner = request.user
            game.save()
            return redirect('game_detail', pk=game.pk)
    else:
        form = GameForm()
    return render(request, 'game_form.html', {'form': form, 'title': 'Create game'})

@login_required
def game_update(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.user != game.owner:
        return redirect('game_list')
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            return redirect('game_detail', pk=game.pk)
    else:
        form = GameForm(instance=game)
    return render(request, 'game_form.html', {'form': form, 'title': 'Update game'})

@login_required
def game_delete(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.user != game.owner:
        return redirect('game_list')
    if request.method == 'POST':
        game.delete()
        return redirect('game_list')
    return render(request, 'game_confirm_delete.html', {'game': game})

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form, 'title': 'Create category'})

@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form, 'title': 'Update category'})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'category_confirm_delete.html', {'category': category})