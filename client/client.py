from subprocess import check_output, PIPE
import requests


POOL_SERVER = 'http://3.137.150.46:8080/'


def get_params(threads, difficulty_level):
    params = requests.get(f'{POOL_SERVER}params?difficulty={difficulty_level}').json()
    miner, seed, complexity, giver = params
    cmd = f'pow-miner -vv -w{threads} -t20 {miner} {seed} {complexity} 999999999999999 {giver} diff{difficulty_level}_{randint(1000000000, 9999999999)}.boc'
    return cmd


def mine(threads, difficulty_level):
    cmd = get_params(threads, difficulty_level)
    result = check_output(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    print([result])


mine(8, 1)
