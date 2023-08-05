# lesscode_options

#### 介绍
lesscode_options是自定义全局配置项，一个地方定义，全局使用

#### 示例
```python
from lesscode_options.options import define, options

define(name="ceshi", type_=str, default="hello world", help_="说明", callback=str)
define(name="age", type_=int, default=5, help_="年龄", callback=str)

print(options.ceshi)
print(type(options.age))

options.ceshi = "hello"
print(options.ceshi)
```