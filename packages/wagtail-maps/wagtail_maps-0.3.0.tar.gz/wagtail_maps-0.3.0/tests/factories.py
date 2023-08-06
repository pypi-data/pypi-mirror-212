import factory
from factory.django import DjangoModelFactory

from wagtail_maps import models


class PointFactory(DjangoModelFactory):
    title = factory.Sequence(lambda n: "Point #%d" % n)
    content = "<p>Lorem ipsum.</p>"
    latitude = factory.Faker('latitude')
    longitude = factory.Faker('longitude')

    class Meta:
        model = models.Point


class MapFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: "Map #%d" % n)
    center_latitude = factory.Faker('latitude')
    center_longitude = factory.Faker('longitude')
    points = factory.RelatedFactoryList(PointFactory, 'map', size=3)

    class Meta:
        model = models.Map
