import unittest
import os, sys

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + '/../../src')

from modelmock.fakers import AgentsFaker
import unittest, random

LEVELS = ['ND', 'RD', 'DD', 'SM', 'ST', 'SA']

LEVEL_MAPPINGS = [
    {'level': 'ND', 'count': 1},
    {'level': 'RD', 'count': 2},
    {'level': 'DD', 'count': 2},
    {'level': 'SM', 'min': 2, 'max': 10},
    {'level': 'ST', 'count': 0},
    {'level': 'SA', 'count': 0}
]


class AgentFakerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__agent_fakers, self.__nums, self.__paddings = [], [], []
        for _ in range(10):
            self.__nums.append(random.randint(1, 20))
            self.__paddings.append(random.randint(1, 50))
            self.__agent_fakers.append(
                AgentsFaker(
                    total_agents=self.__nums[-1],
                    level_mappings=LEVEL_MAPPINGS,
                    id_method='incr',
                    id_prefix='AGENT',
                    id_padding=self.__paddings[-1],
                    id_shuffle=True
                )
            )

    # checking number of records
    def test_num_records(self):
        for num, agent_faker in zip(self.__nums, self.__agent_fakers):
            records = list(agent_faker.records)
            self.assertEqual(num, len(records))

    # checking size of ids: number of ids must be equal to number of records
    def test_ids_size(self):
        for num, agent_faker in zip(self.__nums, self.__agent_fakers):
            ids = list(agent_faker.ids)
            self.assertEqual(len(ids), num)

    """
    checking the content of each id
    - id must start with 'AGENT_'
    - size of numerical part must be greater than or equal to padding
    """
    def test_content_of_ids(self):
        for padding, agent_faker in zip(self.__paddings, self.__agent_fakers):
            ids = list(agent_faker.ids)
            for id in ids:
                self.assertTrue(id.startswith('AGENT_'))
                self.assertTrue(len(id) >= len('AGENT_') + padding)

    # checking tree structure: all nodes must be in the same tree
    def test_all_nodes_in_same_tree(self):
        for agent_faker in self.__agent_fakers:
            records = list(agent_faker.records)

            ancestor_nodes = []
            for record in records:
                if len(ancestor_nodes)==0:
                    ancestor_nodes.append(record['record']['index'])
                    continue
                # parent of this node must be in the ancestor_nodes
                self.assertTrue(record['record']['super'] in ancestor_nodes)
                ancestor_nodes.append(record['record']['index'])

    # checking levels in tree: level of parent must higher than level of children
    def test_levels_of_nodes(self):
        for agent_faker in self.__agent_fakers:
            records = list(agent_faker.records)

            temp = {}
            for record in records:
                id_current = record['record']['index']
                id_parent = record['record']['super']
                num_level_current = LEVELS.index(record['record']['level'])

                temp[id_current] = num_level_current
                if id_parent is None:
                    continue

                num_level_parent = temp[id_parent]
                self.assertTrue(num_level_current>num_level_parent)

    # checking ref properties
    def test_ref_properties(self):
        for agent_faker in self.__agent_fakers:
            records = list(agent_faker.records)

            temp = {}
            for record in records:
                id_current = record['record']['index']
                id_parent = record['record']['super']
                level_current = record['record']['level']

                if id_parent is None:
                    temp[id_current] = [(id_current, level_current)]
                else:
                    temp[id_current] = temp[id_parent] + [(id_current, level_current)]

                for id, level in temp[id_current]:
                    self.assertEqual(record['record']['REFS_'+level], id)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AgentFakerTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
