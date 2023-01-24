# unit tests

import generatefixtures
import unittest

import pandas
import os
import sys

from csv_combiner import CombineCsvClass
from io import StringIO

class TestCsvCombiner(unittest.TestCase):
    # initializing test files
    output_path = "./output.csv"
    program_path = "./csv_combiner.py"

    # use test_fixtures dir to keep fixtures
    accessories_path = "./test_fixtures/accessories.csv"
    clothing_path = "./test_fixtures/clothing.csv"
    householdcleaners_path = "./test_fixtures/household_cleaners.csv"

    # initialize the test output
    test_output = open(output_path, 'w+')
    combiner = CombineCsvClass()

    @classmethod
    def setUpClass(cls):
        # setup before testing
        # generate the test fixture files located in ./test_fixtures using generatefixtures
        generatefixtures.main()
        # put output to ./output.csv so we can assert
        sys.stdout = cls.output_path

    @classmethod
    def tearDownClass(cls):
        # tear down after testing
        cls.test_output.close()
        # remove all initialized test files
        if os.path.exists(cls.output_path):
            os.remove(cls.output_path)
        if os.path.exists(cls.accessories_path):
            os.remove(cls.accessories_path)
        if os.path.exists(cls.clothing_path):
            os.remove(cls.clothing_path)
        if os.path.exists(cls.householdcleaners_path):
            os.remove(cls.householdcleaners_path)

    def setUp(self):
        # setup before each test
        self.output = StringIO()
        sys.stdout = self.output
        self.test_output = open(self.output_path, 'w+')

    def tearDown(self):
        # tear down before each test
        self.test_output.close()

    def test_no_file(self):
        # run csv_combiner with no files for the arguments
        argv = [self.program_path]
        self.combiner.combinefiles(argv)

        self.assertIn("error: no files for the arguments", self.output.getvalue())

    def test_file_no_exist(self):
        # run csv_combiner with a temp file that doesn't exist
        argv = [self.program_path, "temp.csv"]
        self.combiner.combinefiles(argv)

        self.assertIn("error: file or directory invalid", self.output.getvalue())

    def test_filename_column(self):
        # run csv_combiner with valid arguments using test_fixtures
        argv = [self.program_path, self.accessories_path, self.clothing_path, self.householdcleaners_path]
        self.combiner.combinefiles(argv)

        # update the output csv file
        self.test_output.write(self.output.getvalue())
        self.test_output.close()

        # check to see if filename column is in the output
        with open(self.output_path) as f:
            df = pandas.read_csv(filepath_or_buffer=f, lineterminator='\n')
        # check if filename exists in the columns
        self.assertIn('filename', df.columns.values)

    def test_all_data_exist(self):
        # run csv_combiner with valid arguments using test_fixtures
        argv = [self.program_path, self.accessories_path, self.clothing_path, self.householdcleaners_path]
        self.combiner.combinefiles(argv)

        # update the output csv file
        self.test_output.write(self.output.getvalue())
        self.test_output.close()

        # initialize all test_fixtures
        accessories_df = pandas.read_csv(filepath_or_buffer=self.accessories_path, lineterminator='\n')
        clothing_df = pandas.read_csv(filepath_or_buffer=self.clothing_path, lineterminator='\n')
        householdcleaners_df = pandas.read_csv(filepath_or_buffer=self.householdcleaners_path, lineterminator='\n')

        # check to see if all the data from the test_fixtures are in the output
        with open(self.output_path) as f:
            df = pandas.read_csv(filepath_or_buffer=f, lineterminator='\n')
        # if all data is there the lengths should equal after merge
        self.assertEqual(len(accessories_df.merge(df)), len(df))
        self.assertEqual(len(clothing_df.merge(df)), len(df))
        self.assertEqual(len(householdcleaners_df.merge(df)), len(df))