from django.contrib import admin
from .models import UserProfile, GameSession, Achievement, UserAchievement

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_score', 'level')
    search_fields = ('user__username',)
    list_filter = ('level',)

@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'game_type', 'score', 'correct_answers', 'wrong_answers', 'duration', 'created_at')
    list_filter = ('game_type', 'created_at')
    search_fields = ('user__username',)
    date_hierarchy = 'created_at'

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'earned_at')
    list_filter = ('achievement', 'earned_at')
    search_fields = ('user__username', 'achievement__name')
    date_hierarchy = 'earned_at'
