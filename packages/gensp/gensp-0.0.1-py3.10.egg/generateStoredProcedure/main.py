 
import sys
from login import login
from backup import get_backup
from compare import run_compare
import os
def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == 'login':
            login()
        elif sys.argv[1] == 'backup':
            file_number = 0
            for file in os.listdir():
                if file.startswith('backup_') and file.endswith('.sql'):
                    file_number += 1
            print('\033[32m·\033[0m已存在备份数量: '+str(file_number))
            if file_number >= 2:
                print('\033[33m·\033[0m备份数量已满，请执行gsp compare生成存储过程，或执行gsp clear清空备份')
                sys.exit()
            database_name=input('\033[34m·\033[0mdatabase: ').strip()
            get_backup(database_name)
        elif sys.argv[1] == 'compare':
            print('\033[32m·\033[0m生成存储过程如下: ')
            run_compare()
        elif sys.argv[1] == 'clear':
            for file in os.listdir():
                if file.startswith('backup_') and file.endswith('.sql'):
                    os.remove(file)
            print('\033[32m·\033[0mcompleted!')
        elif sys.argv[1] == 'lasttime':
            with open('restore_backup.sql', 'r') as f:
                content = f.read()
                print(content)



        else:
            print("\033[31m·\033Invalid argument")
    else:
        print("\033[31m·\033Invalid number of arguments")


