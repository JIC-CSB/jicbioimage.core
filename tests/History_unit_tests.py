"""Tests for the :class:`jicbioimage.core.image.History` class."""

import unittest

class HistoryUnitTests(unittest.TestCase):

    def test_import(self):
        from jicbioimage.core.image import History
        # Raises ImportError if it does not exist.

    def test_initialisation(self):
        from jicbioimage.core.image import History
        history = History()
        self.assertTrue(isinstance(history, History))
        self.assertEqual(len(history), 0)

    def test_add_event(self):
        from jicbioimage.core.image import History
        history = History()
        def null(): return None
        args = ["arg1", "arg2"]
        kwargs = dict(kwarg1="kwarg1", kwarg2="kwarg2")
        event = history.add_event(function=null, args=args, kwargs=kwargs)
        self.assertEqual(len(history), 1)
        self.assertTrue(isinstance(event, History.Event))
        self.assertEqual(event.function, null)
        self.assertEqual(event.args, args)
        self.assertEqual(event.kwargs, kwargs)


class EventUnitTests(unittest.TestCase):

    def test_initialisation(self):
        from jicbioimage.core.image import History
        def null(): return None
        args = ["arg1", "arg2"]
        kwargs = dict(kwarg1="kwarg1", kwarg2="kwarg2")
        event = History.Event(function=null, args=args, kwargs=kwargs)
        self.assertTrue(isinstance(event, History.Event))
        self.assertEqual(event.function, null)
        self.assertEqual(event.args, args)
        self.assertEqual(event.kwargs, kwargs)

    def test_event_apply_to(self):
        from jicbioimage.core.image import History
        def split(s, sep, maxsplit):
            return s.split(sep, maxsplit)
        args = [","]
        kwargs = {"maxsplit": 1}
        event = History.Event(split, args, kwargs)
        result = event.apply_to("1,2,3,4")
        self.assertEqual(result, ["1", "2,3,4"])

    def test_event_str(self):
        from jicbioimage.core.image import History
        def split(s, sep, maxsplit):
            return s.split(sep, maxsplit)
        args = [","]
        kwargs = {"maxsplit": 1}
        event = History.Event(split, args, kwargs)
        self.assertEqual(str(event), "<History.Event(split(image, ',', maxsplit=1))>")

    def test_event_repr(self):
        from jicbioimage.core.image import History
        def split(s, sep, maxsplit):
            return s.split(sep, maxsplit)
        args = [","]
        kwargs = {"maxsplit": 1}
        event = History.Event(split, args, kwargs)
        self.assertEqual(repr(event), "<History.Event(split(image, ',', maxsplit=1))>")

    def test_event_repr_no_kwargs(self):
        from jicbioimage.core.image import History
        def split(s, sep, maxsplit):
            return s.split(sep, maxsplit)
        args = [","]
        kwargs = {}
        event = History.Event(split, args, kwargs)
        print(event)
        self.assertEqual(repr(event), "<History.Event(split(image, ','))>")

    def test_event_repr_no_args(self):
        from jicbioimage.core.image import History
        def split(s, sep, maxsplit):
            return s.split(sep, maxsplit)
        args = []
        kwargs = {"maxsplit": 1}
        event = History.Event(split, args, kwargs)
        self.assertEqual(repr(event), "<History.Event(split(image, maxsplit=1))>")

    def test_event_repr_no_args_and_no_kwargs(self):
        from jicbioimage.core.image import History
        def split(s, sep, maxsplit):
            return s.split(sep, maxsplit)
        args = []
        kwargs = {}
        event = History.Event(split, args, kwargs)
        self.assertEqual(repr(event), "<History.Event(split(image))>")
