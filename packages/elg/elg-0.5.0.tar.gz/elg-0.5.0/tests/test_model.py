from __future__ import annotations

import unittest
from email import generator
from unittest import TestCase

from elg.model import (AnnotationsResponse, AudioRequest, AudioResponse,
                       ClassificationResponse, ImageRequest,
                       StructuredTextRequest, TextRequest, TextsResponse)


class ServiceTestCase(TestCase):
    def test_structured_text_request(self):
        r = StructuredTextRequest(texts=[{"texts": [{"content": "a"}, {"content": "b"}]}])
        self.assertEqual(r.texts[0].texts[0].content, "a")
        self.assertEqual(r["texts"][0]["texts"][0]["content"], "a")
        self.assertEqual(r.get("texts")[0].get("texts")[0].get("content"), "a")

    def test_text_request_from_file(self):
        r = TextRequest.from_file("./tests/files/sample.txt")
        self.assertEqual(r.content, "Nikolas Tesla lives in Berlin.\n")
        self.assertEqual(r["content"], "Nikolas Tesla lives in Berlin.\n")
        self.assertEqual(r.get("content"), "Nikolas Tesla lives in Berlin.\n")

    def test_text_request(self):
        r = TextRequest(content="a", annotations={"a": [{"start": 0, "end": 3.3}]})
        self.assertEqual(r.content, "a")
        self.assertEqual(r["content"], "a")
        self.assertEqual(r.get("content"), "a")
        self.assertEqual(r.annotations["a"][0].start, 0)
        self.assertEqual(r["annotations"]["a"][0]["start"], 0)
        self.assertEqual(r.get("annotations").get("a")[0].get("start"), 0)
        self.assertEqual(r.annotations["a"][0].end, 3.3)
        self.assertEqual(r["annotations"]["a"][0]["end"], 3.3)
        self.assertEqual(r.get("annotations").get("a")[0].get("end"), 3.3)

    def test_audio_request_from_file(self):
        r = AudioRequest.from_file("./tests/files/sample.mp3")
        self.assertIsInstance(r, AudioRequest)
        self.assertIsNone(r.generator)
        self.assertIsInstance(r.content, bytes)
        self.assertIsInstance(r["content"], bytes)
        self.assertIsInstance(r.get("content"), bytes)

    def test_audio_request_from_file_generator(self):
        r = AudioRequest.from_file("./tests/files/sample.mp3", streaming=True)
        self.assertIsInstance(r, AudioRequest)
        self.assertIsNone(r.content)
        self.assertIsNotNone(r.generator)
        self.assertIsNotNone(r["generator"])
        self.assertIsNotNone(r.get("generator"))

    def test_image_request_from_file(self):
        r = ImageRequest.from_file("./tests/files/sample.png")
        self.assertIsInstance(r, ImageRequest)
        self.assertIsNone(r.generator)
        self.assertIsInstance(r.content, bytes)
        self.assertIsInstance(r["content"], bytes)
        self.assertIsInstance(r.get("content"), bytes)

    def test_image_request_from_file_generator(self):
        r = ImageRequest.from_file("./tests/files/sample.png", streaming=True)
        self.assertIsInstance(r, ImageRequest)
        self.assertIsNone(r.content)
        self.assertIsNotNone(r.generator)
        self.assertIsNotNone(r["generator"])
        self.assertIsNotNone(r.get("generator"))

    def test_annotations_response(self):
        r = AnnotationsResponse(annotations={"a": [{"start": 0, "end": 3.3}]})
        self.assertEqual(r.annotations["a"][0].start, 0)
        self.assertEqual(r["annotations"]["a"][0]["start"], 0)
        self.assertEqual(r.get("annotations").get("a")[0].get("start"), 0)
        self.assertEqual(r.annotations["a"][0].end, 3.3)
        self.assertEqual(r["annotations"]["a"][0]["end"], 3.3)
        self.assertEqual(r.get("annotations").get("a")[0].get("end"), 3.3)

    def test_texts_response(self):
        r = TextsResponse(texts=[{"texts": [{"content": "a"}, {"content": "b"}]}])
        self.assertEqual(r.texts[0].texts[0].content, "a")
        self.assertEqual(r["texts"][0]["texts"][0]["content"], "a")
        self.assertEqual(r.get("texts")[0].get("texts")[0].get("content"), "a")

    def test_classification_response(self):
        r = ClassificationResponse(classes=[{"class": "a", "score": 1.0}])
        self.assertEqual(r.classes[0].class_field, "a")
        self.assertEqual(r["classes"][0]["class_field"], "a")
        self.assertEqual(r.get("classes")[0].get("class_field"), "a")
        self.assertEqual(r.classes[0].score, 1.0)
        self.assertEqual(r["classes"][0]["score"], 1.0)
        self.assertEqual(r.get("classes")[0].get("score"), 1.0)
        r = ClassificationResponse(classes=[{"class": "a", "score": 1}])
        self.assertEqual(r.classes[0].score, 1.0)
        self.assertEqual(r["classes"][0]["score"], 1.0)
        self.assertEqual(r.get("classes")[0].get("score"), 1.0)
