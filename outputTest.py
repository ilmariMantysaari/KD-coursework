import unittest
import output
import pathlib

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


class TestClusterOutput(unittest.TestCase):

    def test_parseClusterName(self):
        self.assertEqual(output.parseClusterNames([], 'whatever'), [])
        self.assertEqual(output.parseClusterNames(DATA_1, 'cluster'), ['cluster1', 'cluster2'])
        self.assertEqual(output.parseClusterNames(DATA_2, 'cluster'), ['cluster1', 'cluster2'])
        self.assertEqual(output.parseClusterNames(DATA_3, 'c'), ['cluster1', 'cluster2', 'cluster3', 'cluster4'])

    def test_ClusterImageWriterInit(self):
        writer = output.ClusterImageWriter('test_output_file', '_suffix')
        self.assertEqual(writer.id, 'test_output_file_suffix')

    def test_writeImage(self):
        writer = output.ClusterImageWriter('test_output_file', '_suffix')
        writer.writeImage(DATA_1, 'cluster', 'a', 'a', 'b', 'b')
        outputFile = pathlib.Path('test_output_file_suffix_1.png')
        self.assertTrue(outputFile.is_file())
