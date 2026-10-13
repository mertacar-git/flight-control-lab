import unittest
from core import simulate

class ControlTests(unittest.TestCase):
    def test_equilibrium(self):
        self.assertTrue(all(r['altitude_m'] == 0 for r in simulate(target=0)))
    def test_actuator_bound(self):
        self.assertTrue(all(abs(r['command_ms2']) <= 10 for r in simulate(target=100)))
    def test_convergence(self):
        self.assertLess(abs(simulate()[-1]['error_m']), 0.4)
    def test_invalid_step(self):
        with self.assertRaises(ValueError): simulate(dt=0)

if __name__ == '__main__': unittest.main()
