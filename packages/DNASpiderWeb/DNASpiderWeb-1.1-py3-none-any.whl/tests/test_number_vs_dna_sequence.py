from random import seed, randint
from unittest import TestCase

from dsw import dna_to_number, number_to_dna


class TestNumber(TestCase):

    def setUp(self):
        seed(2021)
        self.dna_length = 10
        self.test_dna_sequences = ["".join(["ACGT"[randint(0, 3)] for _ in range(self.dna_length)])
                                   for _ in range(10)]
        self.verify_numbers = [937770, 807052, 502551, 991128, 88040, 531838, 908835, 656257, 889866, 144398]

    def test(self):
        results = [int(dna_to_number(dna_sequence=dna_sequence)) for dna_sequence in self.test_dna_sequences]
        self.assertEqual(results, self.verify_numbers)
        results = [dna_to_number(dna_sequence=dna_sequence, is_string=False)
                   for dna_sequence in self.test_dna_sequences]
        self.assertEqual(results, self.verify_numbers)


class TestOligo(TestCase):

    def setUp(self):
        seed(2021)
        self.dna_length = 10
        self.test_numbers = [randint(0, 4 ** self.dna_length) for _ in range(10)]
        self.verify_dna_sequences = ["TATGTTCAAA", "GATCGGTCAC", "CTTGGGAGCC", "ACACGTTTAG", "TGATAATTGG",
                                     "TTAGGCCAGT", "AGAAGGAGGG", "GGAAATAAAA", "GAGGATCGAG", "GCCTGCGACG"]

    def test(self):
        results = [number_to_dna(decimal_number=str(number), dna_length=self.dna_length)
                   for number in self.test_numbers]
        self.assertEqual(results, self.verify_dna_sequences)
        results = [number_to_dna(decimal_number=number, dna_length=self.dna_length)
                   for number in self.test_numbers]
        self.assertEqual(results, self.verify_dna_sequences)


class TestTransform(TestCase):

    def setUp(self):
        self.oligo_length = 8

    def test(self):
        for requested in range(4 ** self.oligo_length):
            dna_sequence = number_to_dna(decimal_number=str(requested), dna_length=self.oligo_length)
            predicted_1 = int(dna_to_number(dna_sequence=dna_sequence))
            predicted_2 = dna_to_number(dna_sequence=dna_sequence, is_string=False)
            self.assertEqual(requested, predicted_1)
            self.assertEqual(requested, predicted_2)
