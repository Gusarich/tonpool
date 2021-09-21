from subprocess import check_output, PIPE
from time import sleep
from flask import Flask
from json import dumps
from threading import Thread


SEED, COMPLEXITY, JSON = -1, -1, '{}'

app = Flask(__name__)


def update():
    global SEED, COMPLEXITY, JSON

    a = check_output('/usr/bin/ton/lite-client/lite-client -C /usr/bin/ton/global.config.json -c "runmethod kf-kkdY_B7p-77TLn2hUhM6QidWrrsl8FYWCIvBMpZKprBtN get_pow_params"', shell=True)

    result = a.decode().split('result:  [ ')[1].split(']')[0]
    SEED, COMPLEXITY, *_ = map(int, result.split())
    JSON = dumps({'seed': SEED, 'complexity': COMPLEXITY})


def auto_updater():
    while True:
        try:
            update()
        except:
            pass
        sleep(10)


@app.route('/params')
def params():
    return JSON


Thread(target=auto_updater).start()

if __name__ == '__main__':
    app.run(port=8080)
