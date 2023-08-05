#### black_tortoise 项目介绍 ####

##### 项目背景 #####
待完善

##### 项目结构 #####
1. 源码查看项目结构 tree 方法
```shell
tree -I "venv|__pycache__|*.pyc|*.pyo|*.so|*.egg-info|*.egg|*.log|*.txt|*.md|*.json|*.yaml|*.yml|*.ini|*.cfg|*.conf|*.xml|*.html|*.rst|*.rst.txt|*.rst"
```
2. 项目结构说明
```shell
 dosc
│   └── deployment -- 发布相关文档介绍 
├── mock_data  -- mock 数据
│   ├── __init__.py
│   └── user
│       └── __init__.py
├── setup.py -- 项目打包配置文件
├── tests -- 测试用例
│   └── __init__.py
└── utils -- 工具类
    ├── FileUtils.py
    ├── __init__.py
    └── logger.py
```