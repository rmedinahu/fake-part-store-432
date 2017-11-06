# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class CarMake(models.Model):
    make = models.CharField(max_length=128, unique=True)


class Part(models.Model):
    num = models.IntegerField()
    name = models.CharField(max_length=128)
    desc = models.TextField()


class Car(models.Model):
    make = models.ForeignKey(CarMake)
    model = models.CharField(max_length=128)
    year = models.IntegerField()


class Customer(models.Model):
    name = models.CharField(max_length=128)


class CarPart(models.Model):
    part = models.ForeignKey(Part)
    car = models.ForeignKey(Car, related_name='parts_that_fit')


class CustomerPurchase(models.Model):
    customer = models.ForeignKey(Customer)
    part = models.ForeignKey(Part)
    date = models.DateTimeField()
