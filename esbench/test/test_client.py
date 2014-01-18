# -*- coding: UTF-8 -*-
# (c)2013 Mik Kocikowski, MIT License (http://opensource.org/licenses/MIT)
# https://github.com/mkocikowski/esbench

import datetime
import os.path
import unittest
import json
import contextlib
import types
import collections

import esbench.client


class ClientTest(unittest.TestCase):

    def test_args_run(self):

        parser = esbench.client.args_parser()
        args = parser.parse_args("run".split())
        self.assertEqual(args.__dict__,
            {
                'no_optimize_calls': False,
#                 'record_segments': False,
                'verbose': False,
                'segments': None,
                'repetitions': 100,
                'maxsize': '1mb',
                'name': args.name, # cheating, but no clean way around it as it contains timestamp
                'no_load': False,
                'command': 'run',
                'observations': 10,
                'data': None,
                'append': False,
                'config_file_path': os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../", "config.json")),
                'host': 'localhost',
                'port': 9200,
                'shards': None,
            }
        )


    def test_args_show(self):

        parser = esbench.client.args_parser()
        args = parser.parse_args("show".split())
#         print(args)
        self.assertEqual(args.__dict__,
            {
                'command': 'show',
                'fields': '(?!observation.segments.segments)((benchmark.meta.benchmark_start)|(observation.meta.benchmark_id)|(observation.meta.observation_id)|(observation.meta.observation_sequence_no)|(observation.segments.num_committed_segments)|(observation.segments.num_search_segments)|(observation.segments.t_optimize_in_millis)|(observation.stats.docs.count)|(observation.stats.store.size_in_bytes)|(observation.stats.fielddata.memory_size_in_bytes)|(observation.stats.search.groups.*query_time_in_millis_per_query$))',
                'host': 'localhost',
                'port': 9200,
                'format': 'csv',
                'verbose': False,
                'ids': ['all'],
            }
        )


#     def test_get_lines_iterator(self):
#
#         cm  = esbench.client.get_lines_iterator(path=None, count=10)
#         self.assertIsInstance(cm, contextlib.GeneratorContextManager)
#         with cm as lines:
#             self.assertIsInstance(lines, collections.Iterable) # http://stackoverflow.com/a/3023965/469997
#             self.assertEqual(10, len(list(lines)))


    def test_parse_maxsize(self):

        self.assertRaises(AttributeError, esbench.client.parse_maxsize, (10,))
        self.assertEqual((10, 0), esbench.client.parse_maxsize('10'))
        self.assertEqual((0, 1<<10), esbench.client.parse_maxsize('1kb'))
        self.assertEqual((0, 1<<20), esbench.client.parse_maxsize('1mb'))


if __name__ == "__main__":
    unittest.main()

