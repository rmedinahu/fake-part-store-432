# fake_data_gen.py
# from partdb_app import fake_data_gen
import json
import random
from django.utils import timezone
import pytz


from loremipsum import get_sentences

from .models import *

def build_part_nums(n=0):
    part_nums = []
    for i in range(n):
        part_nums.append(i)
    return part_nums


def gen_cars():
    f = open('sample_data/make-models.json', 'r')
    data = json.loads(f.read())
    for make, models in data.items():
        car_make = CarMake(make=make)
        car_make.save()
        for model in models:
            for year in range(2010, 2019):
                car = Car(make=car_make, model=model, year=year)
                car.save()
    
    print 'Cars in db', Car.objects.all().count()

def gen_parts(num_parts=None):
    f = open('sample_data/parts.txt', 'r')
    data = []
    for line in f:
        data.append(line.rstrip('\n'))

    if num_parts:        
        for i in range(num_parts):
            p_num = random.randint(1000, 30000)
            p_index = random.randint(0, len(data)-1)
            p = data[p_index]
            part = Part(num=p_num, name=p, desc=get_sentences(1)[0])
            part.save()
    else:
        car_models = Car.objects.all().distinct('model')
        part_nums = build_part_nums(300000)
        for car in car_models:
            for part_name in data:
                r = random.randint(0, len(part_nums)-1)
                p_num = part_nums[r]
                del part_nums[r]                
                part = Part(num=p_num, name=part_name, desc=get_sentences(1)[0])
                part.save()
                cars = Car.objects.filter(model=car.model)
                for c in cars:
                    car_part =  CarPart(part=part, car=c)
                    car_part.save()
            print 'Generated parts for', car.make.make, car.model        

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
