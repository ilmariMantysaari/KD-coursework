import unittest
import output
import pathlib
import os

DATA_1 = [
    {'a': 1, 'b': 2, 'cluster': 'cluster1'},
    {'a': 3, 'b': 5, 'cluster': 'cluster1'},
    {'a': 5, 'b': 6, 'cluster': 'cluster2'}
]

DATA_2 = [
    {'a': 5, 'b': 6, 'cluster': 'cluster2'},
    {'a': 1, 'b': 2, 'cluster': 'cluster1'},
    {'a': 3, 'b': 5, 'cluster': 'cluster1'},
]

DATA_3 = [
    {'a': 5, 'b': 6, 'c': 'cluster2'},
    {'a': 11, 'b': -5, 'c': 'cluster4'},
    {'a': -5, 'b': 1, 'c': 'cluster3'},
    {'a': 1, 'b': 2, 'c': 'cluster1'},
    {'a': 3, 'b': 5, 'c': 'cluster1'}
]

DATA_LIST = [
    [
        {'a': 1, 'b': 5, 'c': 'cluster1'},
        {'a': 2, 'b': 5, 'c': 'cluster1'},
        {'a': 5, 'b': 1, 'c': 'cluster2'},
        {'a': 6, 'b': 2, 'c': 'cluster2'},
        {'a': 3, 'b': 4, 'c': 'cluster2'}
    ],
    [
        {'a': 1, 'b': 5, 'c': 'cluster1'},
        {'a': 2, 'b': 5, 'c': 'cluster1'},
        {'a': 5, 'b': 1, 'c': 'cluster2'},
        {'a': 6, 'b': 2, 'c': 'cluster2'},
        {'a': 3, 'b': 4, 'c': 'cluster1'}
    ]
]

OUTPUT_1 = 'test_output_file_suffix_1.png'
OUTPUT_LIST_1 = 'test_output_file_list_1.png'
OUTPUT_LIST_2 = 'test_output_file_list_2.png'

OUTPUT_FILES = [OUTPUT_1, OUTPUT_LIST_1, OUTPUT_LIST_2]

class TestClusterOutput(unittest.TestCase):

    # Clean up output files
    def setup(self):
        for fileName in OUTPUT_FILES:
            if pathlib.Path(fileName).is_file():
                os.remove(fileName)

    def test_parseClusterName(self):
        self.assertEqual(output.parseClusterNames([], 'whatever'), [])
        self.assertEqual(output.parseClusterNames(DATA_1, 'cluster'), ['cluster1', 'cluster2'])
        self.assertEqual(output.parseClusterNames(DATA_2, 'cluster'), ['cluster1', 'cluster2'])
        self.assertEqual(output.parseClusterNames(DATA_3, 'c'), ['cluster1', 'cluster2', 'cluster3', 'cluster4'])

    def test_ClusterImageWriterInit(self):
        writer = output.ClusterImageWriter('test_output_file', 'suffix')
        self.assertEqual(writer.id, 'test_output_file_suffix')

    def test_writeImages(self):
        writer = output.ClusterImageWriter('test_output_file', 'list')
        writer.writeImages(DATA_LIST, 'c', 'a', 'b')
        outputFile1 = pathlib.Path(OUTPUT_LIST_1)
        outputFile2 = pathlib.Path(OUTPUT_LIST_2)
        self.assertTrue(outputFile1.is_file())
        self.assertTrue(outputFile2.is_file())

    def test_writeImage(self):
        writer = output.ClusterImageWriter('test_output_file', 'suffix')
        writer.writeImage(DATA_3, 'c', 'a', 'b', 1)
        outputFile = pathlib.Path(OUTPUT_1)
        self.assertTrue(outputFile.is_file())
