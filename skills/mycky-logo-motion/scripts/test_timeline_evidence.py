#!/usr/bin/env python3
"""Fast unit tests of the PTS evidence selection logic, no video assets needed."""
import importlib.util
import pathlib
import unittest

p = pathlib.Path(__file__).with_name("timeline_evidence.py")
spec = importlib.util.spec_from_file_location("timeline_evidence", p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TimelineEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.frames = [
            {"ordinal": 0, "pts_s": 0., "duration_s": .033333},
            {"ordinal": 1, "pts_s": .033333, "duration_s": .066667},
            {"ordinal": 2, "pts_s": .1, "duration_s": .033333},
            {"ordinal": 3, "pts_s": .133333, "duration_s": .033333}
        ]
    def test_pts_not_ordinal_div_fps(self):
        self.assertNotAlmostEqual(self.frames[2]["pts_s"], self.frames[2]["ordinal"]/30.)
    def test_choose_nearest_pts(self):
        shots = m.choose(self.frames,.05,(0.,.13),10)
        self.assertEqual([x["ordinal"] for x in shots],[0,1,2,3])
    def test_dedupe(self):
        shots = m.choose(self.frames,.005,(0.,.03),10)
        self.assertEqual([x["ordinal"] for x in shots],[0,1])
    def test_bad_window(self):
        with self.assertRaises(ValueError): m.choose(self.frames,.2,(1.,0.),10)
    def test_shot_cap(self):
        with self.assertRaises(ValueError): m.choose(self.frames,.03,(0.,.13),2)

if __name__ == "__main__":
    unittest.main()
