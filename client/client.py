from subprocess import check_output, PIPE
from random import randint
import requests


POOL_SERVER = 'http://3.137.150.46/'


def get_params(threads, difficulty_level):
    params = requests.get(f'{POOL_SERVER}params?difficulty={difficulty_level}').json()
    miner, seed, complexity, giver = params['miner'], params['seed'], params['complexity'], params['giver']
    filename = f'diff{difficulty_level}_{randint(1000000000, 9999999999)}.boc'
    cmd = f'pow-miner -vv -w{threads} -t20 {miner} {seed} {complexity} 999999999999999 {giver} {filename}'
    return cmd, filename


def mine(threads, difficulty_level):
    cmd, filename = get_params(threads, difficulty_level)
    result = check_output(cmd, shell=True)
    if result == b'':
        return False
    else:
        return filename


def main(threads, difficulty_level):
    while True:
        filename = mine(threads, difficulty_level)
        if not filename:
            continue
        # File [filename] contains valid share
        with open(filename, 'rb') as f:
            r = requests.post(POOL_SERVER + 'send', files={filename: f})
            print(r.text)


main(8, 7)
