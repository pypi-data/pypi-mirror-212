# -*- coding: utf-8 -*-

import time
import psycopg2
import os
import yaml


# 数据库连接字符串
def conn_postgres(database):
    env = yaml.safe_load(open("env.yaml"))
    try:
        conn = psycopg2.connect(
            host=env["login"]["host"],
            port=env["login"]["port"],
            database=database,
            user=env["login"]["user"],
            password=env["login"]["password"]
        )
    except psycopg2.Error as e:
        print("Warning: Failed to connect to database.\nError message: ", e)
        conn = None
    return conn


def get_backup(database):
    # 获取数据库中的所有表
    conn = conn_postgres(database)
    if conn is None:
        return
    cur = conn.cursor()
    cur.execute(
        "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'")
    table_names = cur.fetchall()
    cur.close()
    # 创建备份文件名
    backup_file_name = 'backup_' + str(int(time.time() * 1000)) + '.sql'

    # 将每个表备份到备份文件中
    cur = conn.cursor()
    with open(backup_file_name, 'w') as backup_file:
        for table in table_names:
            cur.execute("SELECT * FROM " + table[0])
            rows = cur.fetchall()
            for row in rows:
                backup_file.write(table[0] + '|' + '|'.join(map(str, row)) + '\n')

    # 需要修改成提张表存入一个文件下，从而降低时间复杂度。


    conn.commit()
    cur.close()

    # 关闭数据库连接
    conn.close()
    print('\033[32m·\033[0m生成备份成功: ' + database)


if __name__ == '__main__':
    get_backup("teamtest_scm")
