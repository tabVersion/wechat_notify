import sys
import os
import subprocess
import requests
import time

def build_parser():
    if len(sys.argv) == 1:
        raise ValueError('please input command')
    return sys.argv[1:]


def send_request(output, err, process, token, command, start, duration, is_win):
    if output is not None:
        output = output.decode('utf-8').split('\r\n') if is_win else output.decode('utf-8').split('\n')
        with open('stdout', 'w') as f:
            f.write('\n'.join(output))
    if err is not None:
        err = err.decode('utf-8').split('\r\n') if is_win else err.decode('utf-8').split('\n')
        with open('stderr', 'w') as f:
            f.write('\n'.join(err))
    temp = None
    # import ipdb; ipdb.set_trace()
    if process.poll() == 0:
        if output is not None:
            output = [''] * 3  + output
            temp = 'the following are last three lines of stdout:\n' + '\n'.join(output[-3:])
        post_str = r'https://sc.ftqq.com/' + token + '.send?' + f'text=[Success] command: ' + ' '.join(command) + f'&desp=start at {time.ctime(int(start))}\ttake time: {duration}\t' + (temp if temp is not None else '')
        requests.post(post_str)
    else:
        if err is not None:
            err = [''] * 3 + err
            temp = 'the following are last three lines of stderr:\n' + '\n'.join(err[-3:])
        # import ipdb; ipdb.set_trace()
        post_str = r'https://sc.ftqq.com/' + token + '.send?' + f'text=[Failed] command: ' + ' '.join(command) + f'&desp=start at {time.ctime(int(start))}\ttake time: {duration}\terror code: {process.poll()}'+ (temp if temp is not None else '')
        print(post_str)
        requests.post(post_str)



def init():
    try:
        token = os.environ['SERVER_CHAN_TOKEN']
    except KeyError:
        print('environment variable `SERVER_CHAN_TOKEN` unfound')
        exit(1)
    return token

def main():
    token = init()
    start = time.time()
    try:
        command = build_parser()
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = process.communicate()

    except KeyboardInterrupt:
        print('keyboard')
        process.kill()
        requests.post(r'https://sc.ftqq.com/' + token + '.send?' + f'text=[Failed] command: ' + ' '.join(command) + f'&desp=start at {time.ctime(int(start))}\nbecause of Keyboard Interrupt')
        exit(0)

    duration = time.time() - start
    is_win = (sys.platform == 'win32')
    send_request(output=output, err=err, duration=duration, is_win=is_win,start=start, token=token, command=command, process=process)



if __name__ == "__main__":
    main()
