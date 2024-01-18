from django.db import models

# Create your models here.
class settingsLog(models.Model):
    input = models.CharField(max_length=300)
    output = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
class Device(models.Model):
    name = models.CharField(max_length=100)
    interface = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=20, null=True, blank=True)
    mask = models.CharField(max_length=20, null=True, blank=True)
    vlan = models.IntegerField(null=True, blank=True)
    is_host = models.BooleanField(default=False)
    firewall = models.IntegerField()

    def __str__(self):
        return self.nombre