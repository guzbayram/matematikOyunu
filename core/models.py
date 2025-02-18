from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """Kullanıcı profil modeli"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.user.username} Profili"

# Kullanıcı oluşturulduğunda otomatik profil oluştur
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Yeni kullanıcı oluşturulduğunda profil oluştur"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Kullanıcı güncellendiğinde profili de güncelle"""
    instance.userprofile.save()

class GameSession(models.Model):
    """Oyun oturumu modeli"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_type = models.CharField(max_length=50)  # multiplication, quick_math, practice
    score = models.IntegerField()
    correct_answers = models.IntegerField()
    wrong_answers = models.IntegerField()
    duration = models.IntegerField()  # seconds
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.game_type} - {self.created_at}"

class Achievement(models.Model):
    """Başarı rozeti modeli"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='achievements/')
    users = models.ManyToManyField(User, through='UserAchievement')
    
    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    """Kullanıcı başarıları ara tablosu"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"
