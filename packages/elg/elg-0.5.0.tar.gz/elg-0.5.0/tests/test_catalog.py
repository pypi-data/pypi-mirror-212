import unittest
from unittest import TestCase

from elg import Catalog, Entity, Service


class CatalogTestCase(TestCase):
    def test_catalog_search(self):
        catalog = Catalog()
        results = catalog.search(limit=10)
        entities = list(results)
        self.assertEqual(len(entities), 10)
        for entity in entities:
            self.assertIsInstance(entity, Entity)

    def test_tool_service(self):
        catalog = Catalog()
        results = catalog.search(entity="LanguageResource", resource="Tool/Service", limit=10)
        entities = list(results)
        for entity in entities:
            self.assertIsInstance(entity, Entity)
            self.assertEqual(entity.resource_type, "Tool/Service")

    def test_lexical_conceptual_resource(self):
        catalog = Catalog()
        results = catalog.search(entity="LanguageResource", resource="Lexical/Conceptual resource", limit=10)
        entities = list(results)
        for entity in entities:
            self.assertIsInstance(entity, Entity)
            self.assertEqual(entity.resource_type, "Lexical/Conceptual resource")

    def test_corpus(self):
        catalog = Catalog()
        results = catalog.search(entity="LanguageResource", resource="Corpus", limit=10)
        entities = list(results)
        for entity in entities:
            self.assertIsInstance(entity, Entity)
            self.assertEqual(entity.resource_type, "Corpus")

    def test_model(self):
        catalog = Catalog()
        results = catalog.search(entity="LanguageResource", resource="Model", limit=10)
        entities = list(results)
        for entity in entities:
            self.assertIsInstance(entity, Entity)
            self.assertEqual(entity.resource_type, "Model")

    def test_grammar(self):
        catalog = Catalog()
        results = catalog.search(entity="LanguageResource", resource="Grammar", limit=10)
        entities = list(results)
        for entity in entities:
            self.assertIsInstance(entity, Entity)
            self.assertEqual(entity.resource_type, "Grammar")

    def test_uncategorized_language_description(self):
        catalog = Catalog()
        results = catalog.search(entity="LanguageResource", resource="Uncategorized Language Description", limit=10)
        entities = list(results)
        for entity in entities:
            self.assertIsInstance(entity, Entity)
            self.assertEqual(entity.resource_type, "Uncategorized Language Description")

    def test_organization(self):
        catalog = Catalog()
        results = catalog.search(entity="Organization", limit=10)
        entities = list(results)
        for entity in entities:
            self.assertIsInstance(entity, Entity)
            self.assertEqual(entity.entity_type, "Organization")

    def test_project(self):
        catalog = Catalog()
        results = catalog.search(entity="Project", limit=10)
        entities = list(results)
        for entity in entities:
            self.assertIsInstance(entity, Entity)
            self.assertEqual(entity.entity_type, "Project")

    def test_elg_compatible_service(self):
        catalog = Catalog()
        results = catalog.search(elg_compatible_service=True, limit=10)
        entities = list(results)
        for entity in entities:
            self.assertIsInstance(entity, Entity)
            self.assertEqual(entity.resource_type, "Tool/Service")

    def test_elg_hosted_data(self):
        catalog = Catalog()
        results = catalog.search(elg_hosted_data=True, limit=10)
        entities = list(results)
        for entity in entities:
            self.assertIsInstance(entity, Entity)
            self.assertEqual(entity.resource_type, "Corpus")

    @unittest.expectedFailure
    def test_elg_compatible_service_and_elg_hosted_data(self):
        catalog = Catalog()
        results = catalog.search(elg_compatible_service=True, elg_hosted_data=True, limit=10)
        entities = list(results)
