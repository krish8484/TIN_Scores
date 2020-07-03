from multiqc.modules.base_module import BaseMultiqcModule
import logging
from collections import OrderedDict
from multiqc.plots import bargraph, beeswarm

# Initialise the logger
log = logging.getLogger(__name__)


class MultiqcModule(BaseMultiqcModule):
    def __init__(self):
        # Initialise the parent object
        super(MultiqcModule, self).__init__(name='zarp', anchor='zarp',
                                            href="https://git.scicore.unibas.ch/zavolan_group/pipelines/zarp",
                                            info="is an example analysis module used for writing documentation.")
        self.mod_data = dict()
        log.info("gg")
        self.GSM1502498 = dict()
        self.GSM1502500 = dict()
        self.data2 = dict()
        for f in self.find_log_files('zarp'):
            self.add_data_source(f)
            parsed_data = self.parse_zarp_logs2(f)
            self.mod_data[f['s_name']] = parsed_data
            print(parsed_data)
            print("found")
            self.data2 = parsed_data
        s_name = f['s_name']
        '''
        self.GSM1502498[s_name] = parsed_data['GSM1502498']
        self.GSM1502500[s_name] = parsed_data['GSM1502500']
	'''
        if len(self.mod_data) == 0:
            raise UserWarning

        '''self.add_section(
            name='Sum os 2 cols',
            anchor='anchor',
            description="Description comes here",
            plot=self.boxchart(s_name)
        )'''

        self.add_section(
            name='Name of the chart',
            anchor='anchor',
            description="Description comes here",
            plot=self.beechart(s_name)
        )

    def parse_zarp_logs(self, f):
        j = 0
        word = []
        words = []
        listToStr1 = []
        listToStr = []
        for l in f['f']:
            if(l != '\t' and l != '\n'):
                # print(l)
                word.append(l)
            else:
                words.append(word)
                word = []
        for k in words:
            listToStr1.append(''.join([str(elem) for elem in k]))
        for k in listToStr1:
            listToStr.append(''.join([str(elem) for elem in k]))
        # print(listToStr)
        col1 = 0
        col2 = 0
        i = -1
        # print(f['f'])
        for l in listToStr:
            # print(l)
            i = i+1
            if i == 1 or i == 2 or i % 3 == 0:
                continue
            # print(s)
            if(i % 3 == 1):
                col1 = col1 + float(l)
            else:
                col2 = col2 + float(l)
        col11 = {'sum3': col1}
        col22 = {'sum3': col2}
        return {'GSM1502498': col11, 'GSM1502500': col22}

    def parse_zarp_logs2(self, f):
        j = 0
        bee = dict()
        word = []
        words = []
        listToStr1 = []
        listToStr = []
        bee = dict()
        for l in f['f']:
            if(l != '\t' and l != '\n'):
                # print(l)
                word.append(l)
            else:
                words.append(word)
                word = []
        for k in words:
            listToStr1.append(''.join([str(elem) for elem in k]))
        for k in listToStr1:
            listToStr.append(''.join([str(elem) for elem in k]))
        #print(listToStr)
        col1 = 0
        col2 = 0
        i = -1
        # print(f['f'])
        for l in listToStr:
            print(i)
            i = i+1
            if i == 1 or i == 2 or i == 0:
                continue
            if i % 3 == 0:
                bee.update({l: {'GSM1502498': float(listToStr[i+1]),
                                'GSM1502500': float(listToStr[i+2])
                                }})
        return bee

    def boxchart(self, s_name):
        data = {
            'GSM1502498': {
                'sum': self.GSM1502498[s_name]['sum3'],
            },
            'GSM1502500': {
                'sum': self.GSM1502500[s_name]['sum3'],
            }
        }
        return bargraph.plot(data, ['sum'])

    def beechart(self, s_name):
        print("gg", self.data2)
        return beeswarm.plot(self.data2)
