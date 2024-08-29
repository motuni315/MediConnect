from django.db import models
from django.utils import timezone


class Tabyouin(models.Model):
    tabyouinid = models.CharField(max_length=8, primary_key=True)
    tabyouinmei = models.CharField(max_length=64)
    tabyouinaddres = models.CharField(max_length=64)
    tabyouintel = models.CharField(max_length=20)
    tabyouinshihonkin = models.IntegerField()
    kyukyu = models.IntegerField()


class Employee(models.Model):
    empid = models.CharField(max_length=8, primary_key=True)
    empfname = models.CharField(max_length=64)
    emplname = models.CharField(max_length=64)
    emppasswd = models.CharField(max_length=256)
    emprole = models.IntegerField()


class Patient(models.Model):
    patid = models.CharField(max_length=8, primary_key=True)
    patfname = models.CharField(max_length=64)
    patlname = models.CharField(max_length=64)
    hokenmei = models.CharField(max_length=64)
    hokenexp = models.DateField()
    birthday = models.DateField(default='2000-01-01')  # 生年月日
    gender = models.CharField(max_length=10,default="NULL")  # 性別
    address = models.CharField(max_length=64,default="NULL")  # 住所


class Medicine(models.Model):
    medicineid = models.CharField(max_length=8, primary_key=True)
    medicinename = models.CharField(max_length=64)
    unit = models.CharField(max_length=8)


class Treatment(models.Model):
    patid = models.CharField(max_length=64)
    medicineid = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='treatments')
    quantity = models.IntegerField()
    impdate = models.DateField()


class Shiiregyosya(models.Model):
    shiireid = models.CharField(max_length=8, primary_key=True)
    shiiremei = models.CharField(max_length=64)
    shiireaddress = models.CharField(max_length=64)
    shiiretel = models.CharField(max_length=20)
    shihonkin = models.IntegerField()
    nouki = models.IntegerField()