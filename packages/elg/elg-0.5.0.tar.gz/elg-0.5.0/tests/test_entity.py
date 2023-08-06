import unittest
from unittest import TestCase

from elg import Entity
from elg.entity import MetadataRecordObj

IDS_TO_TEST = [474, 2334, 8575, 14943, 16109, 5381, 1162, 14001, 7509, 13490, 14164, 3967, 4122, 394]


class EntityTestCase(TestCase):
    def test_from_id(self):
        for id in IDS_TO_TEST:
            with self.subTest():
                entity = Entity.from_id(id=id, use_cache=False)
                self.assertIsNotNone(entity)
                self.assertIsInstance(entity.record, MetadataRecordObj)
        for id in IDS_TO_TEST:
            with self.subTest():
                entity = Entity.from_id(id=id, use_cache=True)
                self.assertIsNotNone(entity)
                self.assertIsInstance(entity.record, MetadataRecordObj)
        for id in IDS_TO_TEST:
            with self.subTest():
                entity = Entity.from_id(id=id, use_cache=False, display_and_stat=True)
                self.assertIsNotNone(entity)
                self.assertIsInstance(entity.record, MetadataRecordObj)
        for id in IDS_TO_TEST:
            with self.subTest():
                entity = Entity.from_id(id=id, use_cache=True, display_and_stat=True)
                self.assertIsNotNone(entity)
                self.assertIsInstance(entity.record, MetadataRecordObj)
