from deon.data.datasource import DataSource
import deon.util as util
import os
import urllib.request
from deon.data.np_extractor import NPExtractor


class MsResearchSource(DataSource):
    KEY = 'msresearch'
    _LINK = 'http://taln.upf.edu/web_old/system/files/resources_files/ms_research_defs-nodefs.txt'
    _OUT_DEF_FILE = 'msresearch.def.tsv'
    _OUT_NODEF_FILE = 'msresearch.nodef.tsv'

    def pull(self, dest, download):
        print('Pulling from msresearch dataset...')
        f_path = os.path.join(dest, 'msresearch.txt')
        if download:
            with open(f_path, 'wb') as f_out:
                f_out.write(urllib.request.urlopen(self._LINK).read())

        if util.tsv_already_exist(dest, [self._OUT_DEF_FILE, self._OUT_NODEF_FILE]):
            return

        source = open(f_path)
        f_out_def_path = os.path.join(dest, self._OUT_DEF_FILE)
        f_out_nodef_path = os.path.join(dest, self._OUT_NODEF_FILE)
        for line in source:
            line = line.strip()
            if not line:
                continue

            is_def, phrase = line.split('/', 1)
            def_flag = is_def == 'DEF'
            _def = 1 if def_flag else 0
            f_out_path = f_out_nodef_path
            topic, pos = self._extract_topic_pos(phrase)
            if _def:
                f_out_path = f_out_def_path
            phrase = ' '.join(util.tokenize(phrase))
            util.save_output(f_out_path, phrase, _def, self.KEY, topic, pos)

        print('\tDONE\n')
        return

    def _extract_topic_pos(self, phrase):
        topic = phrase.split(' is ')
        if len(topic) == 1:
            np_extractor = NPExtractor(phrase)
            result = np_extractor.extract()
            if len(result) > 0:
                topic = result[0]
            else:
                topic = phrase.split()[0]
            return topic, '?'
        else:
            topic = topic[0].lower()
            topic = topic.split('(')[0].strip()

            topics = topic.split()
            start = 0
            if topics[0] in set(['a', 'an', 'the']):
                start = 1

            _t = ' '.join(topics[start:])
            _p = ','.join([str(x) for x in range(start, len(topics))])

        return _t, _p
