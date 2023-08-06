import unittest
from unittest import TestCase

from elg import Catalog, Entity, Service
from elg.model import ResponseObject


class ServiceTestCase(TestCase):
    def test_from_id(self):
        service = Service.from_id(17471)
        result = service("Nikolas Tesla lives in Berlin.", verbose=False)
        self.assertIsInstance(result, ResponseObject)

    def test_from_entity(self):
        entity = Entity.from_id(17471)
        service = Service.from_entity(entity)
        result = service("Nikolas Tesla lives in Berlin.", verbose=False)
        self.assertIsInstance(result, ResponseObject)

    def test_from_catalog(self):
        catalog = Catalog()
        result = next(catalog.search(search="Cogito Discover Named Entity Recognizer"))
        service = Service.from_entity(result)
        result = service("Nikolas Tesla lives in Berlin.", verbose=False)
        self.assertIsInstance(result, ResponseObject)

    def test_output_func(self):
        service = Service.from_id(5228)
        pretty_result = service(
            "Ich habe diesen Film geliebt. Die Schauspieler, das Drehbuch: alles von einem Meisterwerk.",
            output_func="auto",
            verbose=False,
        )
        self.assertIsInstance(pretty_result, str)
