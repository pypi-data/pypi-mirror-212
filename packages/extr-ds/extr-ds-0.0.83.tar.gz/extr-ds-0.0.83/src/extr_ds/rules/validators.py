from typing import List


def assert_same_length(instances: List[List[str]]) -> bool:
    assert len(instances) > 0

    n = len(instances[0])
    for instance in instances:
        assert len(instance) == n
