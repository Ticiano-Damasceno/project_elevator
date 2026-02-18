# não utilizar

# import subprocess
# import redis

# def start_redis() -> bool:
#     try:
#         subprocess.run(['docker','start','redis'],check=True)
#     except:
#         subprocess.run(
#             ['docker', 
#              'run', 
#              '--name', 'redis', '-d', 
#              '-p', '6379:6379', 
#              'redis:latest'
#             ], check=True
#         )
#     finally:
#         print('Redis iniciado via Docker.')


# def check_redis(ip:str) -> bool:
#     client = redis.Redis(host=ip, port=6379)
#     try:
#         client.ping()
#         print("Redis está rodando ✅")
#         return True
#     except redis.exceptions.ConnectionError:
#         print("Redis não está rodando. Subindo via Docker...")
#         start_redis()
#         return True

