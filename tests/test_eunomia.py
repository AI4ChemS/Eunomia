#!/usr/bin/env python

"""Tests for `eunomia` package."""

import unittest


from eunomia import eunomia

class TestMatchMOFNames(unittest.TestCase):
    def test_match_MOF_names(self):
        combined_dict, matched_pairs = match_MOF_names(prediction_dict, ground_truth_dict)

        # Test if the combined dictionary has the correct keys and values
        self.assertDictEqual(combined_dict['bio-MOF-11'], {
            'Predicted Stability': 'Unstable',
            'Paper id': '1',
            'Ground-truth Stability': 'Unstable'
        })
        self.assertDictEqual(combined_dict['bio-MOF-12'], {
            'Predicted Stability': 'Stable',
            'Paper id': '1',
            'Ground-truth Stability': 'Unstable'
        })
        self.assertDictEqual(combined_dict['bio-MOF-13'], {
            'Predicted Stability': 'Stable',
            'Paper id': '1',
            'Ground-truth Stability': 'Stable'
        })
        self.assertDictEqual(combined_dict['bio-MOF-14'], {
            'Predicted Stability': 'Stable',
            'Paper id': '1',
            'Ground-truth Stability': 'Stable'
        })

        # Test if the matched pairs list contains the correct tuples
        self.assertIn(('bio-MOF-11', 'Bio-MOF-11'), matched_pairs)
        self.assertIn(('bio-MOF-12', 'Bio-MOF-12'), matched_pairs)
        self.assertIn(('bio-MOF-13', 'Bio-MOF-13'), matched_pairs)
        self.assertIn(('bio-MOF-14', 'Bio-MOF-14'), matched_pairs)

        # Test for some non-matching keys (optional)
        self.assertNotIn(('bio-MOF-15', 'Bio-MOF-14'), matched_pairs)

if __name__ == '__main__':
    unittest.main()