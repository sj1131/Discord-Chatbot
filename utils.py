from time import localtime
import os

class Log():
    def __init__(self) -> None:
        if not os.path.exists('./data/logs'):
            os.mkdir('./data/logs')

    def event_log(self, f_path='', event=''):
        create_file(f_path)
        date = get_date()
        with open(f_path, 'a') as f:
            f.write(f"{date} - {event}\n")

    def message_log(self, f_path='', author_name='User', bot_name='Bot', user_text='', bot_text=''):
        create_file(f_path)
        date = get_date()
        with open(f_path, 'a') as f:
            f.write(date + ' - ' + author_name + ': ' + user_text + '\n')
            f.write(date + bot_name + ': ' + bot_text + '\n\n')

    def error_log(self, f_path='', event=''):
        create_file(f_path)
        date = get_date()
        with open(f_path, 'a') as f:
            f.write(date + ' - ' + event + '\n')

def create_file(path):
    if not os.path.exists(path):
        with open(path, 'w') as f:
            pass

def get_date():
        year, month, day, hour, minute, sec, _, _, _ = localtime()
        date = f"{year}/{month}/{day}-{hour}:{minute}:{sec}"
        return date