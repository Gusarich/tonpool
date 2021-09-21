from subprocess import check_output
import requests


POOL_SERVER = 'http://localhost:8080/'


def mine(threads, difficulty_level):
    params = requests.get(f'{POOL_SERVER}params?difficulty={difficulty_level}').json()
    miner, seed, complexity, giver = params
    print(miner, seed, complexity, giver)
    cmd = f'pow-miner -vv -w{threads} -t20 {miner} {seed} {complexity} 999999999999999 {giver} diff{difficulty_level}_{randint(1000000000, 9999999999)}.boc'
    print(cmd)


mine(8, 1)
