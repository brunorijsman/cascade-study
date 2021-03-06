from joblib import Parallel, delayed

import os
import random

from bitstring import BitArray

from utils.key import Key
from utils.study_utils import DATASET_SIZE


def _generate_keypair(keylength, error_rate):
    s = random.randint(0, 2 ** keylength - 1)

    correct_key = BitArray(uint=s, length=keylength)
    key = BitArray(correct_key)

    for i in range(0, len(key)):
        rand = random.randint(0, 100000)
        if rand < error_rate*100000:
            key.invert(i)

    return correct_key, key


def _write_keypair(filename, keylength, error_rate):
    correct_key, initial_key = _generate_keypair(keylength, error_rate)
    with open(filename, 'a') as f:
        f.write('%s,%s,%s\n' % (correct_key.hex, initial_key.hex, error_rate))


def read_keypair(filename, line_number):
    with open(filename, 'r') as f:
        line = f.readline()

        f.seek(line_number*len(line))
        line = f.readline()

        line = line.split(',')
        return Key(line[0]), Key(line[1]), float(line[2])


def generate_dataset(filename, keylength, error_rate, num_cores, dataset_size, verbosity):
    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
    with open(filename, 'w'):
        pass
    Parallel(n_jobs=num_cores, verbose=verbosity)(
        delayed(_write_keypair)(filename, keylength, error_rate) for _ in range(0, dataset_size))
