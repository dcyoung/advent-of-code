from typing import List, Union
import logging
from functools import cmp_to_key


def calculate_order(
    a: Union[List, int], b: Union[List, int], indent_str: str = ""
) -> int:
    logging.debug(f"{indent_str} Compare {a} vs {b}")
    # both integers
    if isinstance(a, int) and isinstance(b, int):
        if a == b:
            return 0
        if a < b:
            logging.debug(
                f"{indent_str}- Left side is smaller, so inputs are IN THE RIGHT ORDER"
            )
            return 1
        logging.debug(
            f"{indent_str}- Right side is smaller, so inputs are NOT in the right order"
        )
        return -1
    # mixed
    if isinstance(a, int) and isinstance(b, list):
        logging.debug(
            f"f{indent_str}- Mixed types; convert left to [{a}] and retry comparison"
        )
        return calculate_order([a], b, indent_str=indent_str + "\t")
    if isinstance(a, list) and isinstance(b, int):
        logging.debug(
            f"{indent_str}- Mixed types; convert right to [{b}] and retry comparison"
        )
        return calculate_order(a, [b], indent_str=indent_str + "\t")

    # both lists
    # logging.debug(f"{indent_str} a={len(a)}, b={len(b)}")
    for i, pa in enumerate(a):
        # logging.debug(
        #     f"{indent_str} idx: {i} Elements -> pa= {pa}, pb={b[i] if i < len(b) else None}"
        # )
        if i >= len(b):
            logging.debug(
                f"{indent_str}- Right side ran out of items, so inputs are NOT in the right order"
            )
            return -1

        pb = b[i]
        order = calculate_order(pa, pb, indent_str=indent_str + "\t")
        # logging.debug(f"{indent_str} order found to be {order}")
        if order == 0:
            continue
        return order
    if len(a) == len(b):
        return 0
    logging.debug(
        f"{indent_str}- Left side ran out of items, so inputs are IN THE RIGHT ORDER"
    )
    return 1


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    INPUT_FPATH = "input.txt"
    # INPUT_FPATH = "test_input.txt"
    with open(INPUT_FPATH, "r") as f:
        lines = f.readlines()

    packets = [eval(l.strip()) for l in lines if l.strip()]

    logging.info("Part #1")
    pairs = [packets[i : i + 2] for i in range(0, len(packets), 2)]
    # pair_idx = 1
    # for a, b in pairs:
    #     logging.debug(f"== Pair {pair_idx} ==")
    #     logging.debug(f"Result: {calculate_order(a, b)}")
    #     pair_idx += 1
    #     logging.debug("\n\n")s

    results = [calculate_order(a, b) for a, b in pairs]
    ordered_indices = [i + 1 for i, x in enumerate(results) if x > 0]
    logging.info(ordered_indices)
    logging.info(sum(ordered_indices))

    logging.info("Part #2")
    div_1 = [[2]]
    div_2 = [[6]]
    sorted_packets = sorted(
        packets + [div_1, div_2], key=cmp_to_key(calculate_order), reverse=True
    )
    div_idxs = [sorted_packets.index(div_1) + 1, sorted_packets.index(div_2) + 1]
    logging.info(div_idxs[0] * div_idxs[1])
