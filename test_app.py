import unittest
from streamlit.testing.v1 import AppTest

class AppTests(unittest.TestCase):
    def test_presets_and_custom(self):
        app = AppTest.from_file('app.py').run(timeout=30)
        self.assertFalse(app.exception)
        app.sidebar.selectbox[0].set_value('Custom').run(timeout=30)
        app.sidebar.slider[0].set_value(2.0).run(timeout=30)
        self.assertFalse(app.exception)
        self.assertEqual(len(app.metric),4)
        app.sidebar.selectbox[0].set_value('Proportional only').run(timeout=30)
        self.assertFalse(app.exception)
