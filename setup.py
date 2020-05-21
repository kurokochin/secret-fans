import subprocess

subprocess.call(['pip', 'install', '-r', 'requirements.txt'])
subprocess.call(['sqlite3', 'secret_fans.db', 'CREATE TABLE post_tab(recipient text not null, content text not null);'])