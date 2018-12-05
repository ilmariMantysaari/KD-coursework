import unittest
import output
import pathlib
import os

DATA_1 = [
    {'a': 1, 'b': 2, 'clust': 'cluster1', 'dist': 3.61},
    {'a': 3, 'b': 5, 'clust': 'cluster1', 'dist': 0},
    {'a': 5, 'b': 6, 'clust': 'cluster2', 'dist': 0}
]

DATA_2 = [
    {'a': 5, 'b': 6, 'clust': 'cluster2', 'dist': 0},
    {'a': 1, 'b': 2, 'clust': 'cluster1', 'dist': 3.61},
    {'a': 3, 'b': 5, 'clust': 'cluster1', 'dist': 0},
]

DATA_3 = [
    {'a': 5, 'b': 6, 'clust': 'cluster2', 'dist': 2.24},
    {'a': 6, 'b': 8, 'clust': 'cluster2', 'dist': 0},
    {'a': 9, 'b': 9, 'clust': 'cluster2', 'dist': 3.16},
    {'a': 10, 'b': 11, 'clust': 'cluster2', 'dist': 5},
    {'a': 1, 'b': 2, 'clust': 'cluster1', 'dist': 1},
    {'a': 3, 'b': 5, 'clust': 'cluster1', 'dist': 3.16}
]

DATA_3_CENTERS = [
    {'clust': 'cluster1', 'a': 2, 'b': 2},
    {'clust': 'cluster2', 'a': 6, 'b': 8}
]

DATA_LIST = [
    [
        {'a': 1, 'b': 5, 'clust': 'cluster1', 'dist': 1},
        {'a': 2, 'b': 5, 'clust': 'cluster1', 'dist': 0},
        {'a': 5, 'b': 1, 'clust': 'cluster2', 'dist': 0},
        {'a': 6, 'b': 2, 'clust': 'cluster2', 'dist': 1.41},
        {'a': 3, 'b': 4, 'clust': 'cluster2', 'dist': 3.6}
    ],
    [
        {'a': 1, 'b': 5, 'clust': 'cluster1', 'dist': 0.5},
        {'a': 2, 'b': 5, 'clust': 'cluster1', 'dist': 0.5},
        {'a': 5, 'b': 1, 'clust': 'cluster2', 'dist': 1.37},
        {'a': 6, 'b': 2, 'clust': 'cluster2', 'dist': 1.37},
        {'a': 3, 'b': 4, 'clust': 'cluster1', 'dist': 1.8}
    ]
]

DATA_LIST_CENTERS = [
    [
        {'clust': 'cluster1', 'a': 2, 'b': 5},
        {'clust': 'cluster2', 'a': 5, 'b': 1}
    ],
    [
        {'clust': 'cluster1', 'a': 1.5, 'b': 5},
        {'clust': 'cluster2', 'a': 4.67, 'b': 2.33}
    ]
]

OUTPUT_1 = 'test_output_file_suffix_1.png'
OUTPUT_LIST_1 = 'test_output_file_list_1.png'
OUTPUT_LIST_2 = 'test_output_file_list_2.png'
OUTPUT_GIF = 'test_output_file_list_combined.gif'

OUTPUT_FILES = [OUTPUT_1, OUTPUT_LIST_1, OUTPUT_LIST_2, OUTPUT_GIF]


class TestClusterOutput(unittest.TestCase):

    # Clean up output files
    def setup(self):
        for fileName in OUTPUT_FILES:
            if pathlib.Path(fileName).is_file():
                os.remove(fileName)

    def test_parseClusterName(self):
        self.assertEqual(output.parseClusterNames([], 'whatever'), [])
        self.assertEqual(output.parseClusterNames(DATA_1, 'clust'), ['cluster1', 'cluster2'])
        self.assertEqual(output.parseClusterNames(DATA_2, 'clust'), ['cluster1', 'cluster2'])

    def test_ClusterImageWriterInit(self):
        writer = output.ClusterImageWriter('test_output_file', 'suffix')
        self.assertEqual(writer.id, 'test_output_file_suffix')

    def test_writeKMeansImage(self):
        writer = output.ClusterImageWriter('test_output_file', 'suffix')
        writer.writeKMeansImage(DATA_3, DATA_3_CENTERS, 'clust', 'dist', 'a', 'b', 1)
        outputFile = pathlib.Path(OUTPUT_1)
        self.assertTrue(outputFile.is_file())

    def test_writeKMeansImages(self):
        writer = output.ClusterImageWriter('test_output_file', 'list')
        writer.writeKMeansImages(DATA_LIST, DATA_LIST_CENTERS, 'clust', 'dist', 'a', 'b')
        outputFile1 = pathlib.Path(OUTPUT_LIST_1)
        outputFile2 = pathlib.Path(OUTPUT_LIST_2)
        self.assertTrue(outputFile1.is_file())
        self.assertTrue(outputFile2.is_file())

    def test_writeGif(self):
        writer = output.ClusterImageWriter('test_output_file', 'list')
        writer.writeKMeansImages(DATA_LIST, DATA_LIST_CENTERS, 'clust', 'dist', 'a', 'b')
        writer.writeGif()
        outputGif = pathlib.Path(OUTPUT_GIF)
        self.assertTrue(outputGif.is_file())
