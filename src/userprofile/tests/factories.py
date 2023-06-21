import random

import factory
from factory.django import DjangoModelFactory
from faker import Faker

from userprofile.models import Wish

fake = Faker()


class WishFactory(DjangoModelFactory):
    class Meta:
        model = Wish

    title = fake.text(max_nb_chars=50)
    link = fake.url()
    description = fake.text(max_nb_chars=500)
    type = fake.text(max_nb_chars=50)
