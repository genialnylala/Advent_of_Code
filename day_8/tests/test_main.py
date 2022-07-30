from day_8.src.main import identify_number_codes, identify_output

output = ['cdfeb', 'fcadb', 'cdfeb', 'cdbaf']
output_identified = 5353
number_codes = ['acedgfb', 'cdfbe', 'gcdfa', 'fbcad', 'dab', 'cefabd', 'cdfgeb', 'eafb', 'cagedb', 'ab']
number_codes_identified = ['cagedb', 'ab', 'gcdfa', 'fbcad', 'eafb', 'cdfbe', 'cdfgeb', 'dab', 'acedgfb', 'cefabd']
number_codes_identified_sets = [set(i) for i in number_codes_identified]


def test_identify_number_codes():
    assert identify_number_codes(number_codes) == number_codes_identified_sets


def test_identify_output():
    assert identify_output(number_codes_identified_sets, output) == output_identified
