import unittest
import logging
import numpy as np
from qp.metrics.brier import Brier

LOGGER = logging.getLogger(__name__)

class BrierTestCase(unittest.TestCase):
    """ Test cases for the Brier metric. """

    def test_brier_base(self):
        """
        Test the base case, ensure output is expected.
        """
        pred = [[1,0,0], [1,0,0]]
        truth = [[1,0,0], [0,1,0]]
        brier_obj = Brier(pred, truth)
        result = brier_obj.evaluate()
        expected = 1.
        assert np.isclose(result, expected)

    def test_brier_result_is_scalar(self):
        """
        Verify output is scalar for input of NxM.
        """
        pred = [[1,0,0], [0,1,0], [0,0.5,0.5]]
        truth = [[1,0,0], [0,1,0], [0,0,1]]
        brier_obj = Brier(pred, truth)
        result = brier_obj.evaluate()
        assert np.isscalar(result)

    def test_brier_base_with_non_integers(self):
        """
        Verify output for non-integer prediction values.
        """
        pred = [[0.5,0.5,0]]
        truth = [[1,0,0]]
        brier_obj = Brier(pred, truth)
        result = brier_obj.evaluate()
        expected = 0.5
        assert np.isclose(result, expected)

    def test_brier_max_result(self):
        """
        Base case where prediction is completely wrong, should produce maximum
        possible result value, 2.
        """
        pred = [[0,1,0], [1,0,0]]
        truth = [[1,0,0], [0,1,0]]
        brier_obj = Brier(pred, truth)
        result = brier_obj.evaluate()
        expected = 2.
        assert np.isclose(result, expected)

    def test_brier_min_result(self):
        """
        Base case where prediction is perfect, should produce minimum possible
        result value, 0.
        """
        pred = [[1,0,0], [0,1,0]]
        truth = [[1,0,0], [0,1,0]]
        brier_obj = Brier(pred, truth)
        result = brier_obj.evaluate()
        expected = 0.
        assert np.isclose(result, expected)

    def test_brier_input_arrays_different_sizes(self):
        """
        Verify exception is raised when input arrays are different sizes.
        """
        pred = [[1,0,0], [0,1,0]]
        truth = [[1,0,0], [0,1,0], [0,0,0]]
        brier_obj = Brier(pred, truth)
        with self.assertRaises(ValueError):
            _ = brier_obj.evaluate()

    def test_brier_with_garbage_prediction_input(self):
        """
        Verify exception is raised when prediction input is non-numeric.
        """
        pred = ["foo", "bar"]
        truth = [[1,0,0],[0,1,0]]
        brier_obj = Brier(pred, truth)
        with self.assertRaises(TypeError):
            _ = brier_obj.evaluate()

    def test_brier_with_garbage_truth_input(self):
        """
        Verify exception is raised when truth input is non-numeric.
        """
        pred = [[1,0,0], [0,1,0]]
        truth = ["hello sky", "goodbye ground"]
        brier_obj = Brier(pred, truth)
        with self.assertRaises(TypeError):
            _ = brier_obj.evaluate()

    def test_brier_prediction_does_not_sum_to_one(self):
        """
        Verify exception is raised when prediction input rows don't sum to 1 This
        also verifies that while the total sum of values in the prediction array sum
        to 2, the individual rows do not, and thus logs a warning
        """
        pred = [[1,0.0001,0], [0,0.9999,0]]
        truth = [[1,0,0], [0,1,0]]
        LOGGER.info('Testing now...')
        brier_obj = Brier(pred, truth)
        with self.assertLogs() as captured:
            _ = brier_obj.evaluate()
        self.assertEqual(captured.records[0].getMessage(), "Input predictions do not sum to 1.")

    def test_brier_1d_prediction_does_not_sum_to_one(self):
        """
        Verify exception is raised when 1d prediction input rows don't sum to 1
        """
        pred = [0.3,0.8,0]
        truth = [1,0,0]
        LOGGER.info('Testing now...')
        brier_obj = Brier(pred, truth)
        with self.assertLogs(level=logging.WARNING) as captured:
        # with caplog.at_level(logging.WARNING):
            _ = brier_obj.evaluate()
        self.assertEqual(captured.records[0].getMessage(), "Input predictions do not sum to 1.")

    def test_brier_1d(self):
        """
        Verify 1 dimensional input produced the correct output. This exercises the
        condition in brier._calculate_metric that changes the axis upon which the
        np.mean operates.
        """
        pred = [1,0,0]
        truth = [1,0,0]
        brier_obj = Brier(pred, truth)
        result = brier_obj.evaluate()
        expected = 0.
        assert np.isclose(result, expected)
