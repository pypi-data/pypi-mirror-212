
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
    insert_query=[]
    delete_query=[]
    for line in lines:
        # print(line+"\n")
        if line.startswith('+'):
            insert_lines.append(line[1:])
        elif line.startswith('-'):
            delete_lines.append(line[1:])
    for insert_line in insert_lines[1:]:
        values = insert_line.split('|')
        for i in range(len(values)):
            if isinstance(values[i], str):
                values[i] = "'{}'".format(values[i])
        insert_query.append('INSERT INTO table_name VALUES ({})'.format(', '.join(values)))

    # 删除先不写了，用不上
    procedure = '''\
CREATE OR REPLACE FUNCTION restore_backup()
RETURNS void AS $$
BEGIN
    {};
END;
$$ LANGUAGE plpgsql;
'''.format(';\n    '.join(insert_query))
    with open('restore_backup.sql', 'w') as f:
        f.write(procedure)
    return procedure

def run_compare():
    backup_files = [f for f in os.listdir('.') if f.startswith('backup_')]
    file1 = backup_files[0]
    file2 = backup_files[1]
    # 比较时间戳
    if int(file1.split('_')[1].split('.')[0]) > int(file2.split('_')[1].split('.')[0]):
        file1, file2 = file2, file1
    procedure = generate_procedure(file1, file2)
    print(procedure)


    
 





