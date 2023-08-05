 
import yaml
from backup import conn_postgres

def login():
    with open('env.yaml', 'r') as f:
        env = yaml.safe_load(f)
    host = input('\033[34m·\033[0mhost: ').strip()
    port = input('\033[34m·\033[0mport: ').strip()
    username = input('\033[34m·\033[0musername: ').strip()
    password = input('\033[34m·\033[0mpassword: ').strip()
    env['login']['host'] = host
    env['login']['port'] = port
    env['login']['username'] = username
    env['login']['password'] = password
    with open('env.yaml', 'w') as f:
        yaml.dump(env, f)
    conn_postgres('postgres')


if __name__ == '__main__':

    login()