import io
from collections import defaultdict
from functools import lru_cache
from pprint import pprint

import yaml


class Tools:
    @property
    @lru_cache()
    def situations(self):
        with open('.situations.yaml', encoding='utf8') as inn:
            return yaml.safe_load(inn)

    @property
    @lru_cache
    def equipments(self):
        with open('.equipment.yaml', encoding='utf8') as inn:
            return yaml.safe_load(inn)

    @property
    def passed_situations(self):
        situations = []
        for name, descr in self.situations.items():
            problems = False
            for eq in descr['equipments']:
                if eq not in self.equipments:
                    problems = True
                    break
                if self.equipments[eq]['status'] != 'pass':
                    problems = True
                    break
            if not problems:
                situations.append(name)
        return situations

    @property
    def non_passed_situations(self):
        situations = {}
        for name, descr in self.situations.items():
            problems = {}
            for eq in descr['equipments']:
                if eq not in self.equipments:
                    problems[eq] = 'not mentioned'
                    continue
                if self.equipments[eq]['status'] != 'pass':
                    problems[eq] = self.equipments[eq].get('comment', 'No comment')
            if problems:
                situations[name] = problems
        return situations

    @property
    def problem_equipment_for_active_situations(self):
        # class Problem(dict):
        #     def __init__(self):
        #         super().__init__()
        #         self['will caused'] = set()
        equipments = defaultdict(dict)
        for name, descr in self.situations.items():
            if descr['status'] != 'active':
                continue
            for eq in descr['equipments']:
                if eq not in self.equipments:
                    equipments[eq]['problem'] = 'not mentioned'
                    if 'will caused' not in equipments[eq]:
                        equipments[eq]['will caused'] = set()
                    equipments[eq]['will caused'].add(name)
                    continue
                if self.equipments[eq]['status'] != 'pass':
                    equipments[eq]['problem'] = self.equipments[eq].get('comment', 'No comment')
                    if 'will caused' not in equipments[eq]:
                        equipments[eq]['will caused'] = set()
                    equipments[eq]['will caused'].add(name)
        return sorted(map(list, equipments.items()), key=lambda e: len(e[1]['will caused']), reverse=True)



if __name__ == '__main__':
    s = io.StringIO()
    yaml.dump(Tools().problem_equipment_for_active_situations, s, allow_unicode=True)
    print(s.getvalue())
