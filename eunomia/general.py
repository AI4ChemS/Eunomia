from fuzzywuzzy import fuzz

def match_MOF_names(prediction_dict, ground_truth_dict, threshold=80):
    """
    Match MOF names between prediction and ground truth dictionaries based on similarity.

    This function takes two dictionaries, prediction_dict and ground_truth_dict,
    where the keys represent MOF names and the values are dictionaries containing
    information related to the MOFs. It uses fuzzy matching to find matching pairs
    of MOF names between the two dictionaries based on similarity.

    Parameters:
        prediction_dict (dict): A dictionary containing predicted MOF data.
        ground_truth_dict (dict): A dictionary containing ground truth MOF data.
        threshold (int, optional): The minimum similarity score required to consider
            two keys as a match. The default threshold is 80.

    Returns:
        tuple: A tuple containing two elements:
            - A dictionary (combined_dict) that contains the combined information of
              the matched MOFs between prediction_dict and ground_truth_dict.
            - A list (matched_pairs) that contains tuples of matched key pairs from
              prediction_dict and ground_truth_dict.
    """

    combined_dict = {}
    matched_pairs = []
    matched_ground_truth_keys = set()  # Set to store matched ground_truth_dict keys

    for key_1, value_1 in prediction_dict.items():
        matched_key = None
        highest_similarity = 0

        for key_2 in ground_truth_dict.keys():
            # Check if the key_2 is already matched, if so, skip it
            if key_2 in matched_ground_truth_keys:
                continue

            similarity = fuzz.token_sort_ratio(key_1, key_2)
            if similarity > threshold and similarity > highest_similarity:
                matched_key = key_2
                highest_similarity = similarity

        if matched_key is not None:
            combined_dict[key_1] = {**value_1, **ground_truth_dict[matched_key]}
            matched_pairs.append((key_1, matched_key))
            # Add the matched ground_truth_dict key to the set
            matched_ground_truth_keys.add(matched_key)

    return combined_dict, matched_pairs