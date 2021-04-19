import os
import random

import django
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eMenu.settings')
django.setup()
fake = Faker()

from menuCard.models import Card, Meal


def populate_cards(param):
    for x in range(param):
        title = fake.company()
        description = fake.catch_phrase()
        Card.objects.get_or_create(title=title[:20], description=description)


def populate_cards_with_meals(param):
    meals = {x: [] for x in range(param)}

    for x in range(param * 5):
        title = fake.company()
        description = fake.catch_phrase()
        price = random.randint(0, 30)
        time_to_prepare = fake.time()

        meals[random.randint(0, param - 1)].append(
            Meal.objects.get_or_create(title=title, description=description, price=price,
                                       time_to_prepare=time_to_prepare)[0].id)

    for x in range(param):
        title = fake.company()
        description = fake.catch_phrase()
        card = Card.objects.create(title=title[:20], description=description)
        card.meal.set(meals[x])
        card.save()


if __name__ == '__main__':
    print("populating script!")
    populate_cards(5)
    populate_cards_with_meals(5)

    print("population complete")
