#!/usr/bin/env python

"""Tests for `eunomia` package."""

import unittest

import eunomia


class TestGeneral(unittest.TestCase):
    def test_match_MOF_names(self):
        # Sample test data
        ground_truth_dict = {
            "Bio-MOF-14": {"Ground-truth Stability": "Stable", "Paper id": "1"},
            "Bio-MOF-13": {"Ground-truth Stability": "Stable", "Paper id": "1"},
            "Bio-MOF-12": {"Ground-truth Stability": "Unstable", "Paper id": "1"},
            "Bio-MOF-11": {"Ground-truth Stability": "Unstable", "Paper id": "1"},
            "MIL-101(Cr)": {"Ground-truth Stability": "Stable", "Paper id": "2"},
            "ZIF-8": {"Ground-truth Stability": "Stable", "Paper id": "2"},
            "MIL-53(Al)": {"Ground-truth Stability": "Stable", "Paper id": "2"},
            "HKUST-1": {"Ground-truth Stability": "Unstable", "Paper id": "2"},
            "Zn-MOF-74": {"Ground-truth Stability": "Unstable", "Paper id": "2"},
            "MIL-110(Al)": {"Ground-truth Stability": "Unstable", "Paper id": "2"},
            "MOF-5": {"Ground-truth Stability": "Unstable", "Paper id": "2"},
            "MOF-508": {"Ground-truth Stability": "Unstable", "Paper id": "2"},
            "MOF-69C": {"Ground-truth Stability": "Unstable", "Paper id": "2"},
        }

        prediction_dict = {
            "bio-MOF-11": {"Predicted Stability": "Unstable", "Paper id": "1"},
            "bio-MOF-12": {"Predicted Stability": "Stable", "Paper id": "1"},
            "MOF-74": {"Predicted Stability": "Stable", "Paper id": "2"},
            "MOF-508b": {"Predicted Stability": "Stable", "Paper id": "2"},
            "Zn-BDC-DABCO": {"Predicted Stability": "Stable", "Paper id": "2"},
            "HKUST-1": {"Predicted Stability": "Stable", "Paper id": "2"},
            "Cr-MIL-101": {"Predicted Stability": "Stable", "Paper id": "2"},
            "Al-MIL-110": {"Predicted Stability": "Not provided", "Paper id": "2"},
        }
        combined_dict, matched_pairs, unmatched_pairs = eunomia.match_MOF_names(
            prediction_dict, ground_truth_dict, threshold=70
        )

        # Test if the combined dictionary has the correct keys and values
        self.assertDictEqual(
            combined_dict["bio-MOF-11"],
            {
                "Predicted Stability": "Unstable",
                "Paper id": "1",
                "Ground-truth Stability": "Unstable",
            },
        )
        self.assertDictEqual(
            combined_dict["bio-MOF-12"],
            {
                "Predicted Stability": "Stable",
                "Paper id": "1",
                "Ground-truth Stability": "Unstable",
            },
        )
        self.assertDictEqual(
            combined_dict["MOF-74"],
            {
                "Predicted Stability": "Stable",
                "Paper id": "2",
                "Ground-truth Stability": "Unstable",
            },
        )
        self.assertDictEqual(
            combined_dict["MOF-508b"],
            {
                "Predicted Stability": "Stable",
                "Paper id": "2",
                "Ground-truth Stability": "Unstable",
            },
        )
        self.assertDictEqual(
            combined_dict["HKUST-1"],
            {
                "Predicted Stability": "Stable",
                "Paper id": "2",
                "Ground-truth Stability": "Unstable",
            },
        )

        # Test if the matched pairs list contains the correct tuples
        self.assertIn(("bio-MOF-11", "Bio-MOF-11"), matched_pairs)
        self.assertIn(("bio-MOF-12", "Bio-MOF-12"), matched_pairs)
        self.assertIn(("MOF-74", "Zn-MOF-74"), matched_pairs)
        self.assertIn(("MOF-508b", "MOF-508"), matched_pairs)
        self.assertIn(("HKUST-1", "HKUST-1"), matched_pairs)

        # Test for some non-matching keys (optional)
        self.assertNotIn(("bio-MOF-11", "Bio-MOF-14"), matched_pairs)
        self.assertNotIn(("MOF-74", "Bio-MOF-13"), matched_pairs)


if __name__ == "__main__":
    unittest.main()
