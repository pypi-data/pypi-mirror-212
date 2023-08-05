import time
import psycopg2
import os
import yaml
# 数据库连接字符串


def conn_postgres(database):
    rootPath = os.path.dirname(os.path.abspath(__file__))
    configPath = os.path.join(rootPath, "env.yaml")
    env = yaml.safe_load(open(configPath))
    try:
        conn = psycopg2.connect(
            host=env["login"]["host"],
            port=env["login"]["port"],
            database=database,
            user=env["login"]["user"],
            password=env["login"]["password"]
        )
    except psycopg2.Error as e:
        print("Warning: Failed to connect to database.\nError message: ",e)
        conn = None
    return conn

def get_backup(database):
# 获取数据库中的所有表
    conn=conn_postgres(database)
    if conn is None:
        return
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'")
    table_names = cur.fetchall()
    cur.close()
    print(table_names)
    # 创建备份文件名
    backup_file_name = 'backup_' + str(int(time.time()*1000)) + '.sql'

    # 将每个表备份到备份文件中
    cur = conn.cursor()
    with open(backup_file_name, 'w') as backup_file:
        for table in table_names:
            cur.copy_to(backup_file, table[0], sep='|')
    conn.commit()
    cur.close()

    # 关闭数据库连接
    conn.close()


if __name__ == '__main__':
    conn_postgres("teamtest_scm")