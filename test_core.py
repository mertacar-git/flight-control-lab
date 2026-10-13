import unittest
from core import simulate, metrics

class ControlTests(unittest.TestCase):
    def test_equilibrium(self):
        self.assertTrue(all(r['altitude_m'] == 0 for r in simulate(target=0)))
    def test_actuator_bound(self):
        self.assertTrue(all(abs(r['command_ms2']) <= 10 for r in simulate(target=100)))
    def test_convergence(self):
        self.assertLess(abs(simulate()[-1]['error_m']), 0.4)
    def test_invalid_step(self):
        with self.assertRaises(ValueError): simulate(dt=0)
    def test_settling_equilibrium(self):
        self.assertEqual(metrics(simulate(target=0),0)['settling_time_s'],0)
    def test_unreachable_target(self):
        self.assertIsNone(metrics(simulate(0,0,0),20)['settling_time_s'])
    def test_step_convergence(self):
        coarse = simulate(dt=0.02)[-1]['altitude_m']
        fine = simulate(dt=0.01)[-1]['altitude_m']
        self.assertLess(abs(coarse-fine),0.05)
    def test_disturbance_recovery(self):
        self.assertLess(abs(simulate(gust=3,duration=80)[-1]['error_m']),0.1)
    def test_invalid_gain(self):
        with self.assertRaises(ValueError): simulate(kp=float('nan'))

if __name__ == '__main__': unittest.main()
