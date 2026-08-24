```shell
# https://docs.astral.sh/uv/getting-started/installation/
# https://gitee.com/wangnov/uv-custom/releases
uv venv
uv pip install aiohttp

uv run python ./test/test_apis.py
uv run python ./test/test_apis.py -c
uv run python ./test/test_apis.py -c 8
uv run python ./test/test_apis.py -c 32 -v
uv run python ./test/test_apis.py -c 512 -v --clear
```
