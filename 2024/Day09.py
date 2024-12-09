import unittest

from helper.file import load_file_and_split


def load_data(fp: str) -> str:
    """Read the file at filepath returning the raw string."""
    return load_file_and_split(fp)[0]


def split_string_to_list(s: str) -> list[int | None]:
    """Split the string at every character."""
    disk_map = [None for _ in range(sum(int(c) for c in s))]

    odd = True
    pointer = 0
    file_id = 0

    for char in s:
        number = int(char)
        if odd:
            disk_map[pointer : pointer + number] = [file_id for _ in range(number)]
            file_id += 1

        odd = not odd
        pointer += number

    return disk_map


def split_string_to_blocks(s: str) -> list[tuple[int | None, int]]:
    """Given a string split it into tuples containing the file ID and the block length.
    The file ID is None if the block is empty.
    """
    blocks = []
    odd = True
    file_id = 0

    for char in s:
        number = int(char)
        if odd:
            blocks.append((file_id, number))
            file_id += 1
        else:
            blocks.append((None, number))
        odd = not odd

    return blocks


def visualize_list(chars: list[int | None]) -> str:
    """Visualize the list as a string."""
    return "".join(str(i) if i is not None else "." for i in chars)


def visualize_blocks(blocks: list[tuple[int | None, int]]) -> str:
    """Visualize the list of blocks as a string."""
    return "".join(
        str(i) * length if i is not None else "." * length for i, length in blocks
    )


def fragment_disk(disk: list[int | None]) -> list[int | None]:
    """Compress the disk by moving the rightmost value to an empty space. Modifies ``disk`` in place."""
    for i, val in enumerate(disk):
        if val is None:
            # pop all None values from the end
            while disk[-1] is None:
                disk.pop(-1)
            # move the rightmost value to the empty space
            disk[i] = disk.pop(-1)

    return disk


def compress_blocks(
    blocks: list[tuple[int | None, int]]
) -> list[tuple[int | None, int]]:
    """Compress the blocks by moving the rightmost block of values to an empty space."""
    # initialize values to a large number
    block_length = 999
    file_id = -1
    block_idx = -1

    # remove blocks of length 0
    blocks = [(file_id, length) for file_id, length in blocks if length > 0]

    # one of the last two blocks has to include the largest file ID before the compression was run
    for f_id in range(
        max(file_id for file_id, _ in blocks[-2:] if file_id is not None), -1, -1
    ):
        # get block index of the block with this file ID
        for block_idx, (file_id, block_length) in enumerate(blocks):
            if file_id == f_id:
                break
        assert (
            block_idx >= 0 and file_id is not None and file_id >= 0
        ), f"File ID {f_id} not found."
        # get the first empty block that is large enough for the whole block
        for empty_idx, (other_file_id, other_block_length) in enumerate(blocks):
            # break if block would be moved right
            if empty_idx >= block_idx:
                break
            if other_file_id is None and other_block_length >= block_length:

                # replace the old block with an empty block of the correct length
                blocks[block_idx] = (None, block_length)
                # check whether there are resulting empty blocks before and after the new block and merge them
                if block_idx + 1 < len(blocks) and blocks[block_idx + 1][0] is None:
                    _, length = blocks.pop(block_idx + 1)
                    blocks[block_idx] = (None, blocks[block_idx][1] + length)
                if block_idx - 1 >= 0 and blocks[block_idx - 1][0] is None:
                    _, length = blocks.pop(block_idx - 1)
                    blocks[block_idx - 1] = (None, blocks[block_idx - 1][1] + length)

                # remove the empty block if it is empty afterward, otherwise keep it and reduce its size
                if other_block_length == block_length:
                    _ = blocks.pop(empty_idx)
                else:
                    blocks[empty_idx] = (None, other_block_length - block_length)

                # insert the last block before the empty block (at the same index)
                blocks.insert(empty_idx, (file_id, block_length))

                break
    return blocks


def part1(s: str) -> int:
    """Part1: Compute the checksum of the string after rearranging."""
    disk_map = split_string_to_list(s)
    compressed = fragment_disk(disk_map)
    return sum(i * val for i, val in enumerate(compressed) if val is not None)


def part2(s: str) -> int:
    """Part2: ..."""
    blocks = split_string_to_blocks(s)
    compressed = compress_blocks(blocks)
    total = 0
    i = 0
    for file_id, length in compressed:
        if file_id is None:
            i += length
        else:
            for j in range(i, i + length):
                total += j * file_id
            i += length
    return total


class Test2024Day09(unittest.TestCase):

    fp = "./data/09-test.txt"
    test_data = load_data(fp)

    def test_split_list_and_visualize(self):
        for string, result in [
            ("12345", "0..111....22222"),
            (self.test_data, "00...111...2...333.44.5555.6666.777.888899"),
        ]:
            with self.subTest(msg="string: {}, result: {}".format(string, result)):
                disk_map = split_string_to_list(string)
                self.assertEqual(len(disk_map), len(result))
                vis = visualize_list(disk_map)
                self.assertEqual(vis, result)

    def test_split_blocks_and_visualize(self):
        for string, result in [
            ("12345", "0..111....22222"),
            (self.test_data, "00...111...2...333.44.5555.6666.777.888899"),
        ]:
            with self.subTest(msg="string: {}, result: {}".format(string, result)):
                blocks = split_string_to_blocks(string)
                vis = visualize_blocks(blocks)
                self.assertEqual(vis, result)

    def test_block_compression(self):
        s = self.test_data
        blocks = split_string_to_blocks(s)
        new_blocks = compress_blocks(blocks)
        vis = visualize_blocks(new_blocks)
        self.assertEqual(vis, "00992111777.44.333....5555.6666.....8888..")

    def test_p1(self):
        self.assertEqual(part1(self.test_data), 1928)

    def test_p2(self):
        self.assertEqual(part2(self.test_data), 2858)


if __name__ == "__main__":
    print(">>> Start Main 09:")
    puzzle_data = load_data("./data/09.txt")
    print("Part 1): ", part1(puzzle_data))
    print("Part 2): ", part2(puzzle_data))
    print("End Main 09<<<")
