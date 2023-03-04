
"""Functions around generating and modifying elements utilizing a lexicographical ranking system"""
from math import floor

from .utils import (
    convert_to_base10,
    convert_to_base26,
    decipher_rank,
    find_mean,
    get_greater_length,
    normalize_rank,
    recipher,
)

LOWEST_RANK = "aaaaaa"
LOWEST_RANK_VALUE = 0
HIGHEST_RANK = "eeeeee"
HIGHEST_RANK_VALUE = 49426524
INITIAL_CIPHER_LENGTH = 6


def create_bulk_ranks(count: int):
    ordered_ranks = [LOWEST_RANK]
    if count > 1:
        interval = floor(HIGHEST_RANK_VALUE / (count - 1))
        for i in range(count - 1):
            numerical_rank = interval * (i + 1)
            base26_rank = convert_to_base26(numerical_rank, INITIAL_CIPHER_LENGTH)
            rank = recipher(base26_rank)
            ordered_ranks.append(rank)
    return ordered_ranks


def create_mean_rank(prev_rank: str, next_rank: str) -> str:
    """Generate a new rank inbetween two given ranks"""
    cipher_length = get_greater_length(prev_rank, next_rank)

    low_deciphered = decipher_rank(prev_rank)
    low_normalized = normalize_rank(low_deciphered, cipher_length)
    low_base10 = convert_to_base10(low_normalized)

    high_deciphered = decipher_rank(next_rank)
    high_normalized = normalize_rank(high_deciphered, cipher_length)
    high_base10 = convert_to_base10(high_normalized)

    mean = find_mean(low_base10, high_base10)
    print(f"{low_base10=}")
    print(f"{high_base10=}")
    print(f"{mean=}")
    mean_base26 = convert_to_base26(mean, cipher_length)
    new_rank = recipher(mean_base26)
    print(f"{mean_base26=}")

    return new_rank


def create_highest_rank():
    pass


# """
# OK stanley, here's the planley:
#     if prev:
#         find next rank
#         if next:
#             generate between prev and next
#          else: (this is the last rank)
#              new = rank + 1000
#      else (no prev):
#          try 'aaaaaa'
#          except:
#              find next
#              old top = mean(aaaaaa, next)
#              new rank = aaaaaa
# """
