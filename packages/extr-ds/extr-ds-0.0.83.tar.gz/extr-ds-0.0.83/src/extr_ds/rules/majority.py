from typing import List
from collections import defaultdict

from .validators import assert_same_length


class Majority():
    def merge(self, instances: List[List[str]]) -> List[str]:
        assert_same_length(instances)

        merged_instance: List[str] = []
        for index in range(0, len(instances[0])):
            merged_instance.append(
                self._get_majority(index, instances)
            )

        return merged_instance

    def _get_majority(self, index: int, instances: List[str]) -> str:
        votes = defaultdict(int)
        for instance in instances:
            item = instance[index]
            votes[item] += 1

        votes = sorted(votes.items(), key=lambda v: v[1], reverse=True)[:2]
        if len(votes) == 1:
            return votes[0][0]

        vote1 = votes[0]
        vote2 = votes[1]

        if vote1[1] == vote2[1]:
            return instances[0][index]

        return vote1[0]
