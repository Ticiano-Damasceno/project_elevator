import subprocess

def get_docker_ip() -> str:
    wsl = subprocess.run(['wsl', 'ip', 'addr'], capture_output=True, text=True)
    lista = [x.strip() for x in wsl.stdout.split('\n')]
    ip = [x for x in lista if 'inet' in x and 'global eth0' in x][0].split(' ')[1].replace('/20','')
    return ip