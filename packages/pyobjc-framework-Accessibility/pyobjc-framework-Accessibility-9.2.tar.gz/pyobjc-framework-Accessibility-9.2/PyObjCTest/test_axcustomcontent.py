from PyObjCTools.TestSupport import TestCase

import Accessibility


class TestAXCustomContent(TestCase):
    def test_enum_types(self):
        self.assertIsEnumType(Accessibility.AXCustomContentImportance)

    def test_constants(self):
        self.assertEqual(Accessibility.AXCustomContentImportanceDefault, 0)
        self.assertEqual(Accessibility.AXCustomContentImportanceHigh, 1)

    def test_protocols(self):
        self.assertProtocolExists("AXCustomContentProvider")
