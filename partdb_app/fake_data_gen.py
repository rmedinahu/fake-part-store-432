# fake_data_gen.py
# from partdb_app import fake_data_gen
import json
import random
from django.utils import timezone
import pytz


from loremipsum import get_sentences

from .models import *

def gen_cars():
    f = open('sample_data/make-models.json', 'r')
    data = json.loads(f.read())
    for make, models in data.items():
        car_make = CarMake(make=make)
        car_make.save()
        for model in models:
            for year in range(2015, 2019):
                car = Car(make=car_make, model=model, year=year)
                car.save()
    
    print 'Cars in db', Car.objects.all().count()

def gen_parts(num_parts=0):
    f = open('sample_data/parts.txt', 'r')
    data = []
    for line in f:
        data.append(line.rstrip('\n'))

    for i in range(num_parts):
        p_num = random.randint(1000, 30000)
        p_index = random.randint(0, len(data)-1)
        p = data[p_index]
        part = Part(num=p_num, name=p, desc=get_sentences(1)[0])
        part.save()

    print 'Parts in db', Part.objects.all().count()

def gen_car_parts():
    parts = Part.objects.all()
    cars = Car.objects.all()
    for i in parts:
        num_cars = random.randint(1, 6)
        for j in range(num_cars):
            car_part = CarPart(part=i, car=cars[random.randint(0, len(cars)-1)])
            car_part.save()

    print 'Fittings in db', CarPart.objects.all().count()

def gen_customers(num_users=0, num_purchases=0):
    parts = Part.objects.all()
    f = open('sample_data/users.json', 'r')
    data = json.loads(f.read())
    for i in range(num_users):
        customer = Customer(name=data[i]['first_name'])
        customer.save()
        for j in range(num_purchases):
            part = parts[random.randint(0, len(parts)-1)]
            purchase = CustomerPurchase(customer=customer, part=part, date=timezone.now())
            purchase.save()
    
    print 'Customers in db', Customer.objects.all().count()
