from day_10.src.main import read_input, identify_corrupted_characters, calculate_autocomplete_scores

input_for_corrupted_characters = read_input("input_for_testing.txt")
input_for_autocompletes_scores = read_input("input_for_autocomplete.txt")


def test_identify_corrupted_characters():
    assert identify_corrupted_characters(input_for_corrupted_characters)[0] == ["}", ")", "]", ")", ">"]


def test_calculate_autocomplete_scores():
    assert calculate_autocomplete_scores(input_for_autocompletes_scores) == [288957, 5566, 1480781, 995444, 294]
