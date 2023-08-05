import os
import subprocess
import sys
import time
import re


def read(path):
    with open(path, mode='r', encoding='utf-8') as f:
        return f.read()


def write(path, data):
    with open(path, mode='w', encoding='utf-8') as f:
        return f.write(data)


class ProjectManager:
    def __init__(self, project_parent_dir=None, project_name=None, template_path=None, uwsgi_local_ip_port=None,
                 nginx_port=None, nginx_conf_path=None, python_environment=None):
        self.project_parent_dir = project_parent_dir or f'/django_par_{int(time.time())}'
        self.project_name = project_name or 'new_object'
        self.template_path = template_path or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template-1.0')
        self.uwsgi_local_ip_port = uwsgi_local_ip_port or '127.0.0.2:8000'
        self.nginx_port = nginx_port or '81'
        self.nginx_conf_path = nginx_conf_path or '/etc/nginx/nginx.conf'
        self.venv_name = f'{self.project_name}_venv'
        self.python_environment = python_environment or ('python3' if sys.platform == 'linux' else 'python')
        self.cmd_activate_venv = f'source {self.venv_name}/bin/activate' if sys.platform == 'linux' else f'{self.venv_name}\\Scripts\\activate'
        self.last_result = 0

    def configure_production_environment(self):
        self.ide_uwsgi_ini()
        self.install_uwsgi()
        if sys.platform == 'linux':
            self.append_nginx_config()
        return 0

    def execute(self, cmd):
        try:
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.wait()
            if process.returncode == 0:
                print(f"执行成功: {cmd}")
            else:
                print(f"执行失败: {cmd}")
            self.last_result = process.returncode
            result_lines = []
            for line in process.stdout.readlines():
                result_lines.append(line.decode('utf-8').strip())
            return result_lines
        except Exception as e:
            print(f"执行命令时发生异常: {e}")
            return []

    @staticmethod
    def join_cmd(cmd_list):
        return " && ".join(cmd_list)

    def create_project(self, template_path=''):
        if template_path:
            self.template_path = template_path
        template = f'--template={self.template_path}' if self.template_path else ''
        dic_cmd = {
            '创建项目父文件夹': f'mkdir {self.project_parent_dir}',
            '创建虚拟环境': self.join_cmd([
                f'cd {self.project_parent_dir}',
                f'{self.python_environment} -m venv {self.venv_name}'
            ]),
            '激活虚拟环境;升级pip;安装django;创建django项目': self.join_cmd([
                f'cd {self.project_parent_dir}',
                f'{self.cmd_activate_venv}',
                # 'pip install --upgrade pip',
                'pip install django==3.2.11 -i https://mirrors.aliyun.com/pypi/simple/',
                f'django-admin startproject {self.project_name} {template}',
            ]),
        }
        for key, cmd in dic_cmd.items():
            result_lines = self.execute(cmd)
            for result in result_lines:
                print(result)
            print(f'-------------{key}------------------------')
            if self.last_result != 0:
                print('出现错误，已退出脚本!!')
                return -1
        print(f'远程Django项目映射路径为：{os.path.join(self.project_parent_dir, self.project_name)}')
        return 0

    def install_uwsgi(self):
        if self.last_result == 0:
            return -1
        cmd_install_uwsgi = self.join_cmd([
            f'cd {self.project_parent_dir}',
            self.cmd_activate_venv,
            'pip install uwsgi==2.0.20'
        ])
        result_lines = self.execute(cmd_install_uwsgi)
        for result in result_lines:
            print(result)
        print('------------------------------------')
        return 0

    def ide_uwsgi_ini(self):
        path_uwsgi_ini = os.path.join(self.project_parent_dir, self.project_name, self.project_name, 'uwsgi.ini')
        data_ini = read(path_uwsgi_ini)
        data_ini = data_ini.replace('{{project_name}}', self.project_name)
        data_ini = re.sub(r'socket=(.*)', f'socket={self.uwsgi_local_ip_port}', data_ini)
        write(path_uwsgi_ini, data_ini)
        print(f'修改 {path_uwsgi_ini} 文件完成')
        return 0

    def append_nginx_config(self, nginx_conf_path='', nginx_port=''):
        if self.last_result != 0:
            return -1
        if nginx_conf_path:
            self.nginx_conf_path = nginx_conf_path
        if nginx_port:
            self.nginx_port = nginx_port
        if not os.path.isfile(self.nginx_conf_path):
            print(f'请检查参数或者路径： nginx配置文件: {self.nginx_conf_path} 不存在')
            return -2
        data_nginx_conf = read(self.nginx_conf_path)
        new_server = f'''
        server {{
            listen       {self.nginx_port};
            listen       [::]:{self.nginx_port};
            server_name  _;
            root         /usr/share/nginx/html;
            # Load configuration files for the default server block.
            include /etc/nginx/default.d/*.conf;
            location / {{
                uwsgi_pass {self.uwsgi_local_ip_port};
                include /etc/nginx/uwsgi_params;
            }}
            location /static/ {{
                root {os.path.join(self.project_parent_dir, self.project_name)};
                allow all;
            }}
            error_page 404 /404.html;
            location = /40x.html {{
            }}
            error_page 500 502 503 504 /50x.html;
            location = /50x.html {{
            }}
        }}  
        '''
        for index in range(len(data_nginx_conf)-1, -1, -1):
            if data_nginx_conf[index] == '}':
                write(self.nginx_conf_path, data_nginx_conf[0:index:1] + new_server + '\n}')
                break
        else:
            print('nginx配置文件解析失败')
            return -3
        result_lines_nginx_t = self.execute('nginx -t')
        result_ok = False
        for result in result_lines_nginx_t:
            if 'syntax is ok' in result:
                result_ok = True
        if result_ok:
            print('nginx配置文件修改成功，nginx语法检查通过')
            return 0
        else:
            write(self.nginx_conf_path, data_nginx_conf)
            print(f'nginx代理设置操作失败：已经还原 {self.nginx_conf_path} 文件')
            return -4


if __name__ == '__main__':
    """
        自动脚本化创建Django项目：  
        填写参数后 可以执行设置。 
    """

    django_project = ProjectManager(project_parent_dir='new_obj_parent',
                                                  project_name='new_obj',
                                                  )
    print(django_project.cmd_activate_venv)
    # django_project.create_project()

    """
       文件结构
        |项目总目录
            -> Python虚拟环境|
                -> ...      
                    * 虚拟环境内的文件夹 省略
            -> Django项目目录|:
                -> 项目同名目录
                -> static(静态ROOT目录 )               
                -> static_debug(静态文件_调试目录)
                -> app_test(自动创建的自带的项目连通性测试应用)   
    """

