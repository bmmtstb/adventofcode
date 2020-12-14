import unittest
from parameterized import parameterized
from typing import Dict, List, Tuple, Set


def get_next_departure(curr_time: int, shedule: list) -> Tuple[int, int]:
    """get the next leaving bus and the waiting time"""
    departures = []
    for bus in shedule:
        if bus == "x":
            continue
        mult = int(curr_time / bus) + 1
        departures.append((bus, bus * mult))

    min_t = departures[0][1]
    best_bus = departures[0][0]
    for bus in departures[1:]:
        if bus[1] < min_t:
            min_t = bus[1]
            best_bus = bus[0]
    return best_bus, min_t - curr_time


def find_matching_timestamp(shedule: List) -> int:
    """find a timestamp that holds the definition of having the busses in the list depart n minutes after to for item
    at list[n] """
    timestemp = 1
    wait_time = 1  # there are only a few times we need to check, not every single one -> increment counter step by step
    for diff, bus in enumerate(shedule):
        # ignore empty slots
        if bus == "x":
            continue
        #
        while True:
            # all the subsequent items need to be multiple of the already found values
            if (timestemp + diff) % bus == 0:
                # we do not need to check times before all the current busses arrive (prime numbers!)
                wait_time *= bus
                break
            timestemp += wait_time
    return timestemp


class Test2020Day13(unittest.TestCase):
    @parameterized.expand([
        [939, [7, 13, "x", "x", 59, "x", 31, 19], (59, 5)],
    ])
    def test_departure_times(self, curr, shed, bus):
        self.assertEqual(get_next_departure(curr, shed), bus)

    @parameterized.expand([
        [[17, "x", 13, 19], 3417],
        [[67, 7, 59, 61], 754018],
        [[67, "x", 7, 59, 61], 779210],
        [[67, 7, "x", 59, 61], 1261476],
        [[1789, 37, 47, 1889], 1202161486],
        [[7, 13, "x", "x", 59, "x", 31, 19], 1068781],
    ])
    def test_find_timestemp(self, shed, ts):
        self.assertEqual(find_matching_timestamp(shed), ts)


if __name__ == '__main__':
    print(">>> Start Main 13:")
    timestemp, shedule = (1000391,
                          [19, "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", 37, "x", "x", "x", "x", "x",
                           383, "x", "x", "x", "x", "x", "x", "x", 23, "x", "x", "x", "x", 13, "x", "x", "x", "x", "x",
                           "x", "x", "x", "x", "x", "x", "x", "x", "x", "x", 29, "x", 457, "x", "x", "x", "x", "x", "x",
                           "x", "x", "x", 41, "x", "x", "x", "x", "x", "x", 17])
    print("Part 1):")
    b, t = get_next_departure(timestemp, shedule)
    print(b * t)
    print("Part 2):")
    print(find_matching_timestamp(shedule))
    print("End Main 13<<<")
