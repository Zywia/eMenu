import os
import random
from django.conf import settings
import django
from faker import Faker
import pytz

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eMenu.settings')
django.setup()
fake = Faker()

from menuCard.models import Card, Meal, User


def populate_cards(param):
    for x in range(param):
        title = fake.company()
        description = fake.catch_phrase()
        Card.objects.get_or_create(title=title[:20], description=description)


def populate_cards_with_meals(param):
    meals = {x: [] for x in range(param)}

    for x in range(param * 3):
        title = fake.company()
        description = fake.catch_phrase()
        price = random.randint(0, 30)
        time_to_prepare = fake.time()
        create_date = fake.date_time(tzinfo=pytz.timezone(settings.TIME_ZONE))
        meal_object = Meal.objects.get_or_create(title=title, description=description, price=price,
                                                 time_to_prepare=time_to_prepare)[0]

        if random.randint(0, 1):
            meal_object.create_date = create_date
            meal_object.save()
        meals[random.randint(0, param - 1)].append(meal_object.id)

    for x in range(param):
        title = fake.company()
        description = fake.catch_phrase()
        card = Card.objects.create(title=title[:20], description=description)
        card.meal.set(meals[x])
        create_date = fake.date()
        card.create_date = create_date
        card.save()


def populate_users(N):
    for x in range(N):
        user = fake.unique.user_name()
        email = fake.ascii_free_email()
        User.objects.create_user(user, email, 'admin')


if __name__ == '__main__':
    email = fake.ascii_free_email()
    User.objects.create_superuser("admin", email, 'admin')

    print("populating script!")
    populate_users(10)
    populate_cards(5)
    populate_cards_with_meals(5)

    print("population complete")
