#!/bin/bash

# 激活虚拟环境
source venv/bin/activate

# 运行测试
pytest -v

# 如果测试失败，退出码为非零
exit $?