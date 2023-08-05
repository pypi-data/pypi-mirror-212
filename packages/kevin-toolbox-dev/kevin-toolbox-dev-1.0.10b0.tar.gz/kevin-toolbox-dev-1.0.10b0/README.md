# kevin_toolbox

一个通用的工具代码包集合



环境要求

```shell
numpy>=1.19
pytorch>=1.2
```

安装方法：

```shell
pip install kevin-toolbox  --no-dependencies
```



[项目地址 Repo](https://github.com/cantbeblank96/kevin_toolbox)

[使用指南 User_Guide](./notes/User_Guide.md)

[免责声明 Disclaimer](./notes/Disclaimer.md)

[版本更新记录](./notes/Release_Record.md)：

- v 1.0.10（2023-06-02）
  - move get_value_by_name() from patches.utils to computer_science.algorithm.utils
  - add set_value_by_name() to computer_science.algorithm.utils
  - 增加了 computer_science.algorithm.scheduler ，其中包含
    - Trigger 触发器
    - Strategy_Manager 策略管理器
    - 利用这两个类，就可以根据状态来调用对应策略，进而去调整变量中对应的部分。
- v 1.0.10b（2023-06-04）
  - kevin_toolbox.data_flow.file
    - 让 kevin_notation 中的 column_dict 方式支持单行写入




