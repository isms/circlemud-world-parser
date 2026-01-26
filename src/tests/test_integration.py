# coding: utf-8
import glob
import os

import parse
from utils import parse_from_file


class TestParsingActualTinyworldFiles:
    def get_all_filenames(self, file_type):
        if file_type not in parse.PARSER_LOOKUP:
            raise KeyError('No parser found for file type: "{}"'.format(file_type))

        caw_path = os.path.join(os.path.abspath('.'), 'world')
        pattern = os.path.join(caw_path, file_type, '*.' + file_type)
        filenames = glob.glob(pattern)

        return filenames

    def test_parse_all_files(self):
        """
        parse all of the stock CircleMUD files in the CAW archive
        """
        for file_type, args in parse.PARSER_LOOKUP.items():
            filenames = self.get_all_filenames(file_type)

            for filename in filenames:
                payload, errors = parse_from_file(filename, *args)

                if os.path.split(filename)[1] == '0.obj':
                    assert len(errors) == 1
                    expected = '0\nbug~\na bug~\nThis object is BAD!'
                    assert expected in errors[0]['text']
                else:
                    assert errors == []
