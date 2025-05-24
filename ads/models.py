from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Ads(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    # ссылка на Амазон bucket, если я правильно понял
    image_url = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=100)
    # либо можно создать другую модель и соединить с помощью ForeignKey
    condition = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.title}"


class ExchangeProposal(models.Model):
    id = models.AutoField(primary_key=True)
    # не нужно ли напрямую добавить и самого user foreign key?
    ad_sender = models.ForeignKey(Ads, on_delete=models.CASCADE, related_name='ad_sender')
    ad_receiver = models.ForeignKey(Ads, on_delete=models.CASCADE, related_name='ad_receiver')
    comment = models.TextField()
    status_choices = [("wait", "Ожидает"), ("accept", "Принята"), ("reject", "Отклонена")]
    status = models.CharField(max_length=10, choices=status_choices, default="wait")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ad_sender} : {self.ad_receiver}"
