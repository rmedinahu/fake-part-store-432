# fake_data_gen.py
# from partdb_app import fake_data_gen
import json
import random
from django.utils import timezone
import pytz

from loremipsum import get_sentences

from .models import *

PART_NUM_RANGE = 500000


def gen_cars():
    f = open('sample_data/make-models.json', 'r')
    data = json.loads(f.read())
    for make, models in data.items():
        car_make = CarMake(name=make)
        car_make.save()
        for model in models:
            for year in range(2010, 2019):
                car = Car(make=car_make, model=model, year=year)
                car.save()
    
    print 'Cars in db', Car.objects.all().count()

def gen_car_parts():
    print 'Generating parts and car fittings.'
    
    f = open('sample_data/parts.txt', 'r')
    data = []
    for line in f:
        data.append(line.rstrip('\n'))
    f.close()

    car_models = Car.objects.all().distinct('model')
    print car_models.count(), 'distinct models'
    
    part_nums = range(PART_NUM_RANGE)
    for car in car_models:
        for part_name in data:
            r = random.randint(0, len(part_nums)-1)
            p_num = part_nums[r]
            del part_nums[r]  # don't reuse part nums              
            
            part = Part(num=p_num, name=part_name, desc=get_sentences(1)[0])
            part.save()
            cars = Car.objects.filter(model=car.model)
            for c in cars:
                car_part = CarPart(part=part, car=c)
                car_part.save()
        
        print 'Generated parts for', car.make.name, car.model        

    print 'Parts in db', Part.objects.all().count()
    print 'Fittings in db', CarPart.objects.all().count()

def gen_customers(purchase_range=1):
    parts = Part.objects.all()
    f = open('sample_data/users.json', 'r')
    data = json.loads(f.read())
    for user_info in data:
        customer = Customer(name=user_info['first_name'], last_name=user_info['last_name'])
        customer.save()
        for j in range(random.randint(1, purchase_range)):
            part = parts[random.randint(0, len(parts)-1)]
            purchase = CustomerPurchase(customer=customer, part=part, date=timezone.now())
            purchase.save()
    
    print 'Customers in db', Customer.objects.all().count()

def gen_data():
    gen_cars()
    gen_car_parts()
    gen_customers(purchase_range=10)

