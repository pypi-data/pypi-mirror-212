import os,  sys, re
import subprocess
project_name = "{{ project_name }}"
settings_path = '{{ project_name }}/settings.py'
# if project_name == "{{ project_name }}":
#     settings_path = 'project_name/settings.py'
#     project_name = 'project_name'
ls_my_cmd = ['kill', 'start', 'add_api', 'debug', 'restart']
last_result = 0
project_folder = os.path.join(os.getcwd(), project_name)


def run_cmd(str_cmd):
    global last_result
    process = subprocess.Popen(str_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 等待命令执行完成
    process.wait()
    # 检查返回值来确定命令是否执行成功
    if process.returncode == 0:
        print("执行成功:\t{}".format(str_cmd))
    else:
        print("执行失败:\t{}".format(str_cmd))
    last_result = process.returncode
    ls_result_ = []
    for s in process.stdout.readlines():
        ls_result_.append(str(s, 'utf-8').strip())
    return ls_result_


def read(path):
    with open(path, mode='r', encoding='utf-8') as f:
        return f.read()


def write(path, data):
    with open(path, mode='w', encoding='utf-8') as f:
        return f.write(data)


def write_append(path, new_data):
    with open(path, mode='a', encoding='utf-8') as f:
        return f.write(new_data)


def restart():
    global last_result, project_folder
    for cmd in [f'cd {project_folder} && uwsgi --stop uwsgi.pid',
                f'cd {project_folder} && uwsgi --ini uwsgi.ini']:
        ls_result = run_cmd(cmd)
        for result in ls_result:
            print(result)
        print('----------------------')
        if last_result != 0:
            print('出现错误，已退出脚本!!')
            break
    else:
        print('重启uwsgi 成功')


def debug():
    s = read(settings_path)
    if sys.argv[2] == 'open':
        s = s.replace(re.findall('DEBUG\s*=\s*False', s)[0], 'DEBUG = True')
    elif sys.argv == 'close':
        s = s.replace(re.findall('DEBUG\s*=\s*True', s)[0], 'DEBUG = False')
    write(settings_path, s)


def kill():
    app_name = sys.argv[2] if len(sys.argv) >= 3 else ''
    if not app_name:
        return 0
    s = read(settings_path)
    pattern = f'INSTALLED_APPS.append\s*\(\s*\'*\"*{app_name}\'*\"*\s*\)'
    s = re.sub(pattern, '', s)
    s = re.sub('\n\n+', '\n\n', s)
    write(settings_path, s)
    print(f'关闭 {app_name} 成功')
    # 清除分布式路由：
    global project_folder
    project_folder_url = os.path.join(project_folder, 'urls.py')
    code = read(project_folder_url)
    pattern = r'urlpatterns\.append\s*\(\s*path\(\s*["\'][\w/]*["\']\s*,\s*include\s*\(\s*["\'][\w\.]*["\']\s*\)\s*\)\s*\)'
    code = re.sub(pattern, '', code)
    code = re.sub('\n\n+', '\n\n', code)
    write(project_folder_url, code)


def start():
    app_name = sys.argv[2] if len(sys.argv) >= 3 else ''
    if not app_name:
        return 0
    s = read(settings_path)
    pattern = f'INSTALLED_APPS.append\s*\(\s*\'*\"*{app_name}\'*\"*\s*\)'
    s = re.sub(pattern, '', s)
    s = s + f"INSTALLED_APPS.append(\'{app_name}\')\n"
    s = re.sub('\n\n+', '\n\n', s)
    write(settings_path, s)
    print('匹配成功 开启应用')
    # 增加分布式路由：
    global project_folder
    project_folder_url = os.path.join(project_folder, 'urls.py')
    code = read(project_folder_url)
    pattern = r'urlpatterns\.append\s*\(\s*path\(\s*["\'][\w/]*["\']\s*,\s*include\s*\(\s*["\'][\w\.]*["\']\s*\)\s*\)\s*\)'
    code = re.sub(pattern, '', code)
    code = code + f"urlpatterns.append(path(\'{app_name}/\', include(\'{app_name}.urls\')))\n"
    code = re.sub('\n\n+', '\n\n', code)
    write(project_folder_url, code)


def add_api():
    pass


if __name__ == '__main__':
    sys.argv.append('1')
    sys.argv.append('app_test')

    start()


    print('-----------------------')




