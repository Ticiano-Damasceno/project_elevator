import subprocess

def get_docker_ip() -> str:
    result = subprocess.run(
        ["wsl", "ip", "-4", "addr", "show", "eth0"],
        capture_output=True,
        text=True,
        check=True
    )
 
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.startswith("inet "):
            return line.split()[1].split("/")[0]
 
    raise RuntimeError("Docker IP not found")
 