# gensp

[![Coverage Status](https://coveralls.io/repos/github/yourusername/yourproject/badge.svg?branch=master)](https://github.com/zerobyte1o1/gensp?branch=main)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 比对postgres数据库备份的数据，得出新增的存储过程，目前不支持更新和删除，所有数据库备份区别都以新增的格式输出成存储过程。

## Installation

```
pip install gensp
```

## Usage example

```
gensp help          # 帮助
gensp login         # 配置数据库链接信息
gensp backup        # 备份数据库
gensp compare       # 比较两次数据库备份，并生成存储过程
gensp clear         # 清理本地数据库备份
```


## Release History

* v0.0.1
    * ADD: Initial version

#