import os.path
import unittest
from unittest import TestCase

from elg import Catalog, Corpus, Entity
from elg.model import ResponseObject


class CorpusTestCase(TestCase):
    def test_from_id(self):
        corpus = Corpus.from_id(913)
        corpus.download(filename="1", folder="/tmp/")
        self.assertTrue(os.path.exists("/tmp/1.zip"))

    def test_from_catalog(self):
        catalog = Catalog()
        result = next(catalog.search(search="2006 CoNLL Shared Task - Ten Languages"))
        corpus = Corpus.from_entity(result)
        corpus.download(filename="2", folder="/tmp/")
        self.assertTrue(os.path.exists("/tmp/2.zip"))
