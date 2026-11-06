import unittest
from precision_raster import np, place_rgba, coverage_difference


class PrecisionRasterTests(unittest.TestCase):
    def test_integer_pose_retains_exact_artwork(self):
        src = np.zeros((8, 7, 4), np.uint8); src[1:6, 2:5] = [70, 20, 190, 255]
        out = place_rgba(np.zeros((20, 20, 4), np.uint8), src, 3, 4)
        np.testing.assert_array_equal(out[4:12, 3:10], src)
        self.assertEqual(coverage_difference(out[:, :, 3], out[:, :, 3])['changed_pixels'], 0)

    def test_float_coverage_centroid_tracks_fractional_position(self):
        src = np.ones((4, 4, 4), np.float32)
        for x in (3.0, 3.25, 3.5, 3.75):
            out = place_rgba(np.zeros((14, 14, 4), np.float32), src, x, 2)
            alpha = out[:, :, 3]; xx = np.indices(alpha.shape)[1]
            self.assertAlmostEqual(float((xx*alpha).sum()/alpha.sum()), x+1.5, places=6)
            self.assertAlmostEqual(float(alpha.sum()), 16, places=6)

    def test_premultiplication_avoids_dark_edge(self):
        src = np.zeros((2, 2, 4), np.uint8); src[0, 0] = [255, 0, 0, 255]
        out = place_rgba(np.zeros((6, 6, 4), np.uint8), src, 1.5, 1.5)
        partial = (out[:, :, 3] > 0) & (out[:, :, 3] < 255)
        self.assertTrue(partial.any()); self.assertTrue((out[:, :, 0][partial] == 255).all())

    def test_negative_entry_clips_at_canvas_without_wrapping(self):
        src = np.full((4, 4, 4), 255, np.uint8)
        out = place_rgba(np.zeros((10, 10, 4), np.uint8), src, -2, 3)
        self.assertEqual(np.count_nonzero(out[:, :, 3]), 8)
        self.assertFalse(out[:, 5:, 3].any())
        self.assertFalse(place_rgba(out*0, src, -8, 0).any())

    def test_coverage_detects_endpoint_change_and_rejects_wrong_canvas(self):
        a = np.zeros((10, 10), np.uint8); b = a.copy(); b[2, 3] = 255
        report = coverage_difference(a, b)
        self.assertEqual(report['changed_pixels'], 1); self.assertEqual(report['max_alpha_error'], 1)
        with self.assertRaises(ValueError): coverage_difference(a, b[:, :-1])


if __name__ == '__main__': unittest.main()
