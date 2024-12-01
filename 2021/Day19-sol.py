# pylint: skip-file
"""
existing solution from:
https://www.reddit.com/r/adventofcode/comments/rjpf7f/comment/hqmf51j/?utm_source=share&utm_medium=web2x&context=3
"""
import copy

ScannerBeaconMaster = []
with open("data/19.txt", "r") as data:
    LineList = []
    for t in data:
        Line = t.strip()
        if Line.startswith("---"):
            pass
        elif len(Line) > 1:
            NewList = list(map(int, t.split(",")))
            LineList.append(NewList)
        else:
            ScannerBeaconMaster.append(LineList)
            LineList = []
    ScannerBeaconMaster.append(LineList)

ScannerNum = len(ScannerBeaconMaster)
print("ScannerNum:", ScannerNum)
OrientationList = [
    ["x", "y", "z"],
    ["x", "z", "-y"],
    ["x", "-y", "-z"],
    ["x", "-z", "y"],
    ["-x", "-y", "z"],
    ["-x", "z", "y"],
    ["-x", "y", "-z"],
    ["-x", "-z", "-y"],
    ["y", "z", "x"],
    ["y", "x", "-z"],
    ["y", "-z", "-x"],
    ["y", "-x", "z"],
    ["-y", "-z", "x"],
    ["-y", "x", "z"],
    ["-y", "z", "-x"],
    ["-y", "-x", "-z"],
    ["z", "x", "y"],
    ["z", "y", "-x"],
    ["z", "-x", "-y"],
    ["z", "-y", "x"],
    ["-z", "-x", "y"],
    ["-z", "y", "x"],
    ["-z", "x", "-y"],
    ["-z", "-y", "-x"],
]

ScannerAddedtoGrid = []
ScannerLocations = []
ScannerBeaconDistances = []
CheckBeacons = []
# ScAtG is 0 if no, 1 if yes
for a in range(ScannerNum):
    ScannerAddedtoGrid.append(0)
    ScannerLocations.append([0, 0, 0])
ScannerAddedtoGrid[0] += 1
PermanentBeacons = []
ScannerCopy = copy.deepcopy(ScannerBeaconMaster)
for i in ScannerCopy[0]:
    PermanentBeacons.append(i)
    CheckBeacons.append(i)
print(PermanentBeacons)

for ScanNum, Scanner in enumerate(ScannerBeaconMaster):
    BeaconDistances = []
    for x, Beacon1 in enumerate(Scanner):
        for y, Beacon2 in enumerate(Scanner):
            if x > y:
                DistSq = (
                    ((Beacon1[0] - Beacon2[0]) ** 2)
                    + ((Beacon1[1] - Beacon2[1]) ** 2)
                    + ((Beacon1[2] - Beacon2[2]) ** 2)
                )
                BeaconDistances.append(DistSq)
    ScannerBeaconDistances.append(BeaconDistances)

BeaconDistanceCheckSet = set()
for b in ScannerBeaconDistances[0]:
    BeaconDistanceCheckSet.add(b)

Continue = True
CycleCount = 0
while Continue:
    CycleCount += 1
    ScannerFoundThisCycle = False
    NewBeaconDistanceSet = set()
    NewCheckBeacons = []
    for u in range(ScannerNum):
        if ScannerAddedtoGrid[u] == 0:
            ValidScannerFound = False
            DistanceValidCount = 0
            for d in ScannerBeaconDistances[u]:
                if d in BeaconDistanceCheckSet:
                    DistanceValidCount += 1
                if DistanceValidCount == 66:
                    ValidScannerFound = True
                    break

            if ValidScannerFound:
                for orientation in OrientationList:
                    NewBeaconTestList = []
                    for t in ScannerBeaconMaster[u]:
                        NewBeacon = []
                        for dir_ in orientation:
                            if dir_ == "x":
                                NewBeacon.append(t[0])
                            elif dir_ == "-x":
                                NewBeacon.append(t[0] * -1)
                            elif dir_ == "y":
                                NewBeacon.append(t[1])
                            elif dir_ == "-y":
                                NewBeacon.append(t[1] * -1)
                            elif dir_ == "z":
                                NewBeacon.append(t[2])
                            elif dir_ == "-z":
                                NewBeacon.append(t[2] * -1)
                        NewBeaconTestList.append(NewBeacon)
                    ValidBeaconListFound = False
                    for d in NewBeaconTestList:
                        for e in CheckBeacons:
                            XOffset = e[0] - d[0]
                            YOffset = e[1] - d[1]
                            ZOffset = e[2] - d[2]
                            Count = 0
                            for r in NewBeaconTestList:
                                TestList = [
                                    r[0] + XOffset,
                                    r[1] + YOffset,
                                    r[2] + ZOffset,
                                ]
                                if TestList in CheckBeacons:
                                    Count += 1
                                if Count >= 12:
                                    ValidBeaconListFound = True
                                    break
                            if ValidBeaconListFound:
                                ScannerLocations[u] = [XOffset, YOffset, ZOffset]
                                break
                        if ValidBeaconListFound:
                            break
                    if ValidBeaconListFound:
                        for j in NewBeaconTestList:
                            NewPotentialBeacon = [
                                j[0] + XOffset,
                                j[1] + YOffset,
                                j[2] + ZOffset,
                            ]
                            NewCheckBeacons.append(NewPotentialBeacon)
                            if NewPotentialBeacon not in PermanentBeacons:
                                PermanentBeacons.append(NewPotentialBeacon)
                        for b in ScannerBeaconDistances[u]:
                            NewBeaconDistanceSet.add(b)
                        ScannerAddedtoGrid[u] += 1
                        print(f"Scanner Beacon list {u} syncronized!")
                        print(len(PermanentBeacons))
                        ScannerFoundThisCycle = True
                        break
            if not ValidScannerFound:
                print(f"Scanner {u} failed to synchronize")
    BeaconDistanceCheckSet.clear()
    BeaconDistanceCheckSet = NewBeaconDistanceSet
    CheckBeacons.clear()
    for t in range(len(NewCheckBeacons)):
        CheckBeacons.append(NewCheckBeacons.pop())

    ScannerCount = 0
    print(f"{CycleCount = }")
    for p in ScannerAddedtoGrid:
        ScannerCount += p
    if ScannerCount == ScannerNum:
        print("All scanners syncronized!")
        Continue = False
    if not ScannerFoundThisCycle:
        print("No valid scanner found this cycle, debug")
        Continue = False

MaxDistance = 0
for t in ScannerLocations:
    for y in ScannerLocations:
        if t != y:
            DistanceX = abs(t[0] - y[0])
            DistanceY = abs(t[1] - y[1])
            DistanceZ = abs(t[2] - y[2])
            TotalDistance = DistanceX + DistanceY + DistanceZ
            if TotalDistance > MaxDistance:
                MaxDistance = TotalDistance

print(ScannerLocations)
print(PermanentBeacons)
print(ScannerAddedtoGrid)
NumBeacons = len(PermanentBeacons)
print(f"Part One Answer: {NumBeacons = }")
print(f"Part Two Answer: {MaxDistance = }")
