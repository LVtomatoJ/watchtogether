redis安装
https://redis.io/docs/stack/get-started/install/

生成秘钥
openssl rand -hex 32

python3 -m uvicorn fastapi-project.main:app --reload