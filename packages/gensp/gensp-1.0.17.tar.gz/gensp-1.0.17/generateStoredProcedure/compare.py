# -*- coding: utf-8 -*-

import difflib
import os


def compare_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        diff = difflib.unified_diff(f1.readlines(), f2.readlines())
        return ''.join(diff)


def generate_procedure(file1, file2):
    diff = compare_files(file1, file2)
    lines = diff.split('\n')
    insert_lines = []
    delete_lines = []
    insert_query = []
    delete_query = []
    for line in lines:
        if line.startswith('+'):
            insert_lines.append(line[1:])
        elif line.startswith('-'):
            delete_lines.append(line[1:])
    for insert_line in insert_lines[1:]:
        values = insert_line.split('|')
        values2=values[1:]
        for i in range(len(values2)):
            if isinstance(values2[i], str):
                values2[i] = "'{}'".format(values2[i])
        insert_query.append('INSERT INTO {} VALUES ({})'.format(values[0],', '.join(values2)))

    # 删除先不写了，用不上
    procedure = '''\
CREATE OR REPLACE FUNCTION restore_backup(numbegin NUMERIC,numend NUMERIC)
RETURNS NUMERIC AS $$
DECLARE a int DEFAULT 1;
DECLARE
BEGIN
    a:=numbegin;
    while a < numend LOOP
        {};
        a = a + 1 ;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
SELECT restore_backup(0,2);
'''.format(';\n        '.join(insert_query))
    with open('restore_backup.sql', 'w') as f:
        f.write(procedure)
    return procedure


def run_compare():
    backup_files = [f for f in os.listdir('.') if f.startswith('backup_')]
    if len(backup_files) < 2:
        print('\033[33m·\033[0m数据库备份数量不够2个，请先gensp backup备份数据库')
    file1 = backup_files[0]
    file2 = backup_files[1]
    # 比较时间戳
    if int(file1.split('_')[1].split('.')[0]) > int(file2.split('_')[1].split('.')[0]):
        file1, file2 = file2, file1
    procedure = generate_procedure(file1, file2)
    print(procedure)