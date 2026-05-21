"""
Test suite for DiaModality.ModalityPlot
Run with: pytest test_diamodality.py -v
"""

import pytest
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend — essential for CI / headless runs

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import DiaModality.ModalityPlot as mp


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def simple_data():
    """Minimal valid 3-column dataset."""
    return [
        [1.0, 0.0, 0.0],
        [0.0, 2.0, 0.0],
        [0.0, 0.0, 3.0],
        [1.5, 1.5, 0.0],
        [1.0, 1.0, 1.0],
    ]

@pytest.fixture
def simple_bin():
    """Corresponding binarization."""
    return [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 1, 0],
        [1, 1, 1],
    ]

@pytest.fixture
def plot(simple_data, simple_bin):
    """A freshly constructed ModalityPlot (closes its figure on teardown)."""
    import matplotlib.pyplot as plt
    p = mp.ModalityPlot(simple_data, simple_bin)
    yield p
    plt.close('all')


# ---------------------------------------------------------------------------
# 1. Construction & basic smoke tests
# ---------------------------------------------------------------------------

class TestConstruction:

    def test_basic_construction(self, simple_data, simple_bin):
        """Should not raise with valid minimal input."""
        import matplotlib.pyplot as plt
        p = mp.ModalityPlot(simple_data, simple_bin)
        plt.close('all')

    def test_numpy_input_accepted(self, simple_bin):
        """numpy arrays should be accepted as input."""
        import matplotlib.pyplot as plt
        data = np.array([[1.0, 0.5, 0.0], [0.0, 1.0, 2.0]])
        binarization = np.array([[1, 0, 0], [0, 1, 1]])
        p = mp.ModalityPlot(data, binarization)
        plt.close('all')

    def test_custom_angles(self, simple_data, simple_bin):
        import matplotlib.pyplot as plt
        p = mp.ModalityPlot(simple_data, simple_bin, angles=[0, 120, 240])
        plt.close('all')

    def test_custom_modality_names(self, simple_data, simple_bin):
        import matplotlib.pyplot as plt
        p = mp.ModalityPlot(simple_data, simple_bin,
                            modalities=('Alpha', 'Beta', 'Gamma'))
        plt.close('all')

    def test_normalization_linear(self, simple_data, simple_bin):
        import matplotlib.pyplot as plt
        p = mp.ModalityPlot(simple_data, simple_bin,
                            normalization_func='linear')
        plt.close('all')

    def test_normalization_sigmoid(self, simple_data, simple_bin):
        import matplotlib.pyplot as plt
        p = mp.ModalityPlot(simple_data, simple_bin,
                            normalization_func='sigmoid')
        plt.close('all')


# ---------------------------------------------------------------------------
# 2. Input validation / assertions
# ---------------------------------------------------------------------------

class TestInputValidation:

    def test_mismatched_lengths_raises(self):
        import matplotlib.pyplot as plt
        data = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
        binarization = [[1, 0, 0]]           # one row short
        with pytest.raises((AssertionError, ValueError)):
            mp.ModalityPlot(data, binarization)
        plt.close('all')

    def test_wrong_column_count_raises(self):
        """Only 2 columns instead of 3 should fail."""
        import matplotlib.pyplot as plt
        data = [[1.0, 2.0], [3.0, 4.0]]
        binarization = [[1, 0], [0, 1]]
        with pytest.raises((AssertionError, ValueError, IndexError)):
            mp.ModalityPlot(data, binarization)
        plt.close('all')

    def test_empty_data_raises(self):
        import matplotlib.pyplot as plt
        with pytest.raises((AssertionError, ValueError)):
            mp.ModalityPlot([], [])
        plt.close('all')

    def test_none_values_handled(self):
        """None / empty cells (from CSV parsing) should be treated as 0."""
        import matplotlib.pyplot as plt
        data = [[1.0, None, 0.0], [0.0, 2.0, None]]
        binarization = [[1, 0, 0], [0, 1, 0]]
        p = mp.ModalityPlot(data, binarization)   # should not raise
        plt.close('all')


# ---------------------------------------------------------------------------
# 3. Internal helpers — private-name-mangled access
# ---------------------------------------------------------------------------

class TestInternals:

    def test_format_input_converts_none_to_zero(self):
        """__format_input must replace None with 0 in the data array."""
        # Access through name-mangling
        p_class = mp.ModalityPlot
        # Build a minimal instance to call the method:
        import matplotlib.pyplot as plt
        data   = [[1.0, None, 0.5]]
        bindata = [[1, 0, 0]]
        obj = mp.ModalityPlot(data, bindata)
        # After formatting, no NaN/None should remain
        assert not np.isnan(obj.data).any(), "NaNs found after __format_input"
        assert obj.data[0][1] == 0.0, "None was not replaced with 0.0"
        plt.close('all')

    def test_vector_addition_single_row(self):
        """A single-axis unit vector should land on the unit circle."""
        import matplotlib.pyplot as plt
        data = [[1.0, 0.0, 0.0]]
        bindata = [[1, 0, 0]]
        obj = mp.ModalityPlot(data, bindata, angles=[90, 210, 330],
                              whole_sum=False)
        # resultant magnitude should be 1.0 for a pure first-axis point
        resultants = obj._ModalityPlot__vector_addition(obj.data, obj.binarization)
        assert len(resultants) == 1
        # magnitude ≈ 1 (allowing float tolerance)
        assert abs(abs(resultants[0]) - 1.0) < 1e-5, \
            f"Expected |resultant| ≈ 1.0, got {abs(resultants[0])}"
        plt.close('all')

    def test_normalization_sigmoid_range(self):
        """Sigmoid output must stay within (0, 1)."""
        import matplotlib.pyplot as plt
        obj = mp.ModalityPlot([[1,0,0],[0,1,0]], [[1,0,0],[0,1,0]],
                              normalization_func='sigmoid')
        values = np.linspace(-10, 10, 100)
        normed = obj._ModalityPlot__normalization(values)
        assert all(0 < v < 1 for v in normed), "Sigmoid output out of (0, 1) range"
        plt.close('all')

    def test_normalization_linear_range(self):
        """Linear normalization must output [0, 1]."""
        import matplotlib.pyplot as plt
        obj = mp.ModalityPlot([[1,0,0],[0,1,0]], [[1,0,0],[0,1,0]],
                              normalization_func='linear')
        values = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        normed = obj._ModalityPlot__normalization(values)
        assert abs(min(normed)) < 1e-9, "Linear min should be 0"
        assert abs(max(normed) - 1.0) < 1e-9, "Linear max should be 1"
        plt.close('all')

    def test_find_match_modality_hit(self):
        """Should return the correct index when a matching pattern exists."""
        import matplotlib.pyplot as plt
        obj = mp.ModalityPlot([[1,0,0],[0,1,0]], [[1,0,0],[0,1,0]])
        patterns = [(True, False, False), (False, True, False)]
        idx = obj._ModalityPlot__find_match_modality((False, True, False), patterns)
        assert idx == 1
        plt.close('all')

    def test_find_match_modality_miss_returns_zero(self):
        """Should return 0 when no pattern matches."""
        import matplotlib.pyplot as plt
        obj = mp.ModalityPlot([[1,0,0],[0,1,0]], [[1,0,0],[0,1,0]])
        patterns = [(True, False, False)]
        idx = obj._ModalityPlot__find_match_modality((False, True, False), patterns)
        assert idx == 0
        plt.close('all')


# ---------------------------------------------------------------------------
# 4. Save / output
# ---------------------------------------------------------------------------

class TestOutput:

    def test_save_creates_file(self, plot, tmp_path):
        outfile = str(tmp_path / 'test_output')
        plot.save(outfile, file_type='png')
        assert (tmp_path / 'test_output.png').exists(), "save() did not create a file"

    def test_save_svg(self, plot, tmp_path):
        outfile = str(tmp_path / 'test_output')
        plot.save(outfile, file_type='svg')
        assert (tmp_path / 'test_output.svg').exists()

    def test_save_transparent(self, plot, tmp_path):
        """transparent=True should not raise."""
        outfile = str(tmp_path / 'test_transparent')
        plot.save(outfile, file_type='png', transparent=True)


# ---------------------------------------------------------------------------
# 5. Edge / boundary cases
# ---------------------------------------------------------------------------

class TestEdgeCases:

    def test_all_zero_data(self):
        """All-zero data should not crash (vectors are skipped)."""
        import matplotlib.pyplot as plt
        data = [[0.0, 0.0, 0.0]] * 5
        binarization = [[0, 0, 0]] * 5
        # The assertion `self.data.any()` will fire — that's expected behaviour.
        with pytest.raises(AssertionError):
            mp.ModalityPlot(data, binarization)
        plt.close('all')

    def test_single_row(self):
        import matplotlib.pyplot as plt
        data = [[1.0, 2.0, 3.0]]
        binarization = [[1, 1, 1]]
        p = mp.ModalityPlot(data, binarization)
        plt.close('all')

    def test_large_dataset(self):
        """Should handle 1000 rows without error or significant slowdown."""
        import matplotlib.pyplot as plt
        rng = np.random.default_rng(42)
        data = rng.uniform(0, 5, (1000, 3)).tolist()
        binarization = (rng.uniform(0, 1, (1000, 3)) > 0.5).astype(int).tolist()
        p = mp.ModalityPlot(data, binarization)
        plt.close('all')

    def test_whole_sum_false(self):
        import matplotlib.pyplot as plt
        data = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
        binarization = [[1, 0, 0], [0, 1, 0]]
        p = mp.ModalityPlot(data, binarization, whole_sum=False)
        plt.close('all')

    def test_same_scale_true(self):
        import matplotlib.pyplot as plt
        data = [[1.0, 2.0, 0.5], [0.5, 0.5, 0.5]]
        binarization = [[1, 1, 0], [1, 0, 1]]
        p = mp.ModalityPlot(data, binarization, same_scale=True)
        plt.close('all')

    def test_full_center_false(self):
        import matplotlib.pyplot as plt
        data = [[1.0, 1.0, 1.0], [1.0, 0.0, 0.0]]
        binarization = [[1, 1, 1], [1, 0, 0]]
        p = mp.ModalityPlot(data, binarization, full_center=False)
        plt.close('all')

if __name__ == '__main__':
    pytest.main([__file__, '-v'])