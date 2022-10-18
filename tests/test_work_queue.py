from unittest import TestCase

from pydantic import ValidationError

from src.models.message import Message
from src.models.wikibase.ia_sandbox_wikibase import IASandboxWikibase
from src.models.work_queue import WorkQueue


class TestWorkQueue(TestCase):
    def test_publish_with_wikibase(self):
        w = WorkQueue(wikibase=IASandboxWikibase())
        message = Message(wikibase=IASandboxWikibase(), title="Test")
        assert w.publish(message=message) is True

    def test_publish_without_wikibase(self):
        w = WorkQueue(wikibase=IASandboxWikibase())
        message = Message(title="Test")
        assert w.publish(message=message) is True

    def test_publish_no_message(self):
        w = WorkQueue(wikibase=IASandboxWikibase())
        with self.assertRaises(ValidationError):
            w.publish() # type: ignore

    def test_listen(self):
        w = WorkQueue(wikibase=IASandboxWikibase(), testing=True)
        w.listen_to_queue()
