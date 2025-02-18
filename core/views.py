from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import UserProfile, GameSession, Achievement
import random
import json
from django.http import JsonResponse
from django.db.models import Sum

def home(request):
    """Ana sayfa görünümü"""
    if request.user.is_authenticated:
        profile = UserProfile.objects.get_or_create(user=request.user)[0]
        context = {
            'profile': profile,
            'recent_games': GameSession.objects.filter(user=request.user).order_by('-created_at')[:5]
        }
    else:
        context = {}
    return render(request, 'core/home.html', context)

@login_required
def multiplication_game(request):
    """Çarpım tablosu oyunu görünümü"""
    if request.method == 'POST':
        data = json.loads(request.body)
        # Oyun sonuçlarını kaydet
        GameSession.objects.create(
            user=request.user,
            game_type='multiplication',
            score=data['score'],
            correct_answers=data['correct'],
            wrong_answers=data['wrong'],
            duration=data['duration']
        )
        return JsonResponse({'status': 'success'})
    
    return render(request, 'core/multiplication_game.html')

@login_required
def quick_math(request):
    """Hızlı matematik oyunu görünümü"""
    if request.method == 'POST':
        data = json.loads(request.body)
        GameSession.objects.create(
            user=request.user,
            game_type='quick_math',
            score=data['score'],
            correct_answers=data['correct'],
            wrong_answers=data['wrong'],
            duration=data['duration']
        )
        return JsonResponse({'status': 'success'})
    
    return render(request, 'core/quick_math.html')

@login_required
def practice_mode(request):
    """Alıştırma modu görünümü"""
    return render(request, 'core/practice_mode.html')

@login_required
def profile(request):
    """Kullanıcı profili görünümü"""
    profile = UserProfile.objects.get_or_create(user=request.user)[0]
    game_history = GameSession.objects.filter(user=request.user).order_by('-created_at')
    achievements = Achievement.objects.filter(users=request.user)
    
    # Toplam istatistikleri hesapla
    total_correct = game_history.aggregate(Sum('correct_answers'))['correct_answers__sum'] or 0
    total_wrong = game_history.aggregate(Sum('wrong_answers'))['wrong_answers__sum'] or 0
    total_duration = game_history.aggregate(Sum('duration'))['duration__sum'] or 0
    
    # Seviye ilerleme yüzdesi (her 1000 puan bir seviye)
    progress = (profile.total_score % 1000) / 10  # 0-100 arası yüzde
    
    context = {
        'profile': profile,
        'achievements': achievements,
        'game_history': game_history[:10],  # Son 10 oyun
        'total_correct': total_correct,
        'total_wrong': total_wrong,
        'total_duration': round(total_duration / 60, 1),  # Dakika cinsinden
        'progress': progress
    }
    return render(request, 'core/profile.html', context)

def generate_question(game_type, difficulty='medium'):
    """Oyun tipine göre soru üretme fonksiyonu"""
    if game_type == 'multiplication':
        if difficulty == 'easy':
            num1 = random.randint(1, 5)
            num2 = random.randint(1, 5)
        elif difficulty == 'medium':
            num1 = random.randint(2, 7)
            num2 = random.randint(2, 7)
        else:  # hard
            num1 = random.randint(6, 10)
            num2 = random.randint(6, 10)
        return {
            'question': f'{num1} × {num2}',
            'answer': num1 * num2
        }
    elif game_type == 'quick_math':
        operations = ['+', '-', '×', '÷']
        op = random.choice(operations)
        if op == '+':
            num1 = random.randint(1, 100)
            num2 = random.randint(1, 100)
            return {
                'question': f'{num1} + {num2}',
                'answer': num1 + num2
            }
        elif op == '-':
            num1 = random.randint(1, 100)
            num2 = random.randint(1, num1)  # num2 her zaman num1'den küçük olsun
            return {
                'question': f'{num1} - {num2}',
                'answer': num1 - num2
            }
        elif op == '×':
            num1 = random.randint(1, 12)
            num2 = random.randint(1, 12)
            return {
                'question': f'{num1} × {num2}',
                'answer': num1 * num2
            }
        else:  # division
            num2 = random.randint(1, 12)
            answer = random.randint(1, 12)
            num1 = num2 * answer  # tam bölünebilir sayılar üret
            return {
                'question': f'{num1} ÷ {num2}',
                'answer': answer
            }

def register(request):
    """Kullanıcı kayıt görünümü"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Kullanıcı profili oluştur
            UserProfile.objects.create(user=user)
            # Kullanıcıyı otomatik giriş yap
            login(request, user)
            messages.success(request, 'Hesabınız başarıyla oluşturuldu!')
            return redirect('core:home')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})
