from socketio import Client
import cfg
import json
sio = Client()


@sio.on('event')
def on_message(data):
    holder2 = json.dumps(data)
    holder = json.loads(holder2)
    # print(data)
    if 'streamlabels' in holder['type'] or \
            'unpauseQueue' in holder['type'] or \
            'pauseQueue' in holder['type'] or \
            'muteVolume' in holder['type'] or  \
            'unmuteVolume' in holder['type']:
        i = 0
    elif 'donation' in holder['type']:
        holder = holder['message'][0]
        user = holder['name']
        amt = "{:.2f}".format(float(holder['amount']), 2)
        currency = holder['currency']
        print(user, amt, currency)
    elif 'twitch_account' in holder['for']:
        if 'follow' in holder['type']:
            holder = holder['message'][0]
            print(holder['name'])
        elif 'bits' in holder['type']:
            holder = holder['message'][0]
            user = holder['name']
            amount = holder['amount']
            print(user, amount)
    if 'streamlabels.underlying' in holder['type']:
        print()
        # print(f"Test {holder['message']['data']}")


@sio.on('disconnect')
def on_disconnect():
    sio.connect('https://sockets.streamlabs.com?token=' + cfg.STREAM_LABS_SOCKET)

def start():
    sio.connect('https://sockets.streamlabs.com?token=' + cfg.STREAM_LABS_SOCKET)
    sio.wait()
