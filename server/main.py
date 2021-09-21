from subprocess import check_output, PIPE
from time import sleep
from flask import Flask, request
from json import dumps
from threading import Thread


SEED, COMPLEXITY, PARAMS = -1, -1, {}

app = Flask(__name__)


def update():
    global SEED, COMPLEXITY, JSON

    a = check_output('/usr/bin/ton/lite-client/lite-client -C /usr/bin/ton/global.config.json -c "runmethod kf-kkdY_B7p-77TLn2hUhM6QidWrrsl8FYWCIvBMpZKprBtN get_pow_params"', shell=True)

    result = a.decode().split('result:  [ ')[1].split(']')[0]
    SEED, COMPLEXITY, *_ = result.split()
    json = {
        'miner': 'EQDImbp84rsu1k1pHzCe8DeX1jA3quSbenldkWUsGxbZCYme',
        'seed': SEED,
        'complexity': COMPLEXITY,
        'giver': 'kf8gf1PQy4u2kURl-Gz4LbS29eaN4sVdrVQkPO-JL80VhOe6'
    }
    for i in range(1, 6):
        PARAMS[i] = json.copy()
        PARAMS[i]['complexity'] += '0' * i
        PARAMS[i] = dumps(PARAMS[i])


def auto_updater():
    while True:
        try:
            update()
        except:
            pass
        sleep(10)


@app.route('/params', methods=['GET'])
def params():
    difficulty_level = int(request.args.get('difficulty'))
    return PARAMS[difficulty_level]


Thread(target=auto_updater).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
