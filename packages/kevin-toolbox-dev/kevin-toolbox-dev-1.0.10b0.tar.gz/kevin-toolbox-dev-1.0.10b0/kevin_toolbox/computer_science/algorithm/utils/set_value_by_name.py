from kevin_toolbox.computer_science.algorithm.utils import get_value_by_name


def set_value_by_name(var, name, value):
    """
        通过解释名字得到取值方式，然后到 var 中将对应部分的值修改为 value。

        参数：
            var:            任意支持索引取值的变量
            name:           <string> 取值方式
                                由多组 "<解释方式><键>" 组成。
                                解释方式支持以下几种:
                                    "@"     使用 eval() 读取键
                                    ":"     使用 str() 读取键
                                    "|"     依次尝试 str() 和 eval() 两种方式
                                示例:
                                    "@100"      表示指向 var[eval("100")]
                                    ":epoch"    表示指向 var["epoch"]
                                    "|1+1"    表示首先尝试指向 var["1+1"]，若不成功则尝试指向 var[eval("1+1")]
                                假设 var=dict(acc=[0.66,0.78,0.99])，如果你想将 var["acc"][1] 设置为 100，那么可以将 name 写成：
                                    ":acc@1" 或者 "|acc|1" 等。
                                注意，在 name 的开头也可以添加任意非解释方式的字符，本函数将直接忽略它们，比如下面的:
                                    "var:acc@1" 和 "xxxx|acc|1" 也能正常写入。
            value:          待赋给的值
    """
    assert isinstance(name, (str,))
    key = name
    for char in ":@|":
        key = key.rsplit(char, 1)[-1]
    assert len(key) < len(name), f'invalid name: {name}'

    item = get_value_by_name(var=var, name=name[:-1 - len(key)])

    flag = name[-1 - len(key)]
    if flag == "@":
        key = eval(key)
    elif flag == "|":
        try:
            _ = item[key]
        except:
            key = eval(key)

    item[key] = value
    return var


if __name__ == '__main__':
    print(set_value_by_name(var=dict(acc=[0.66, 0.78, 0.99]), name="|acc|0", value=1))
    print(set_value_by_name(var=dict(acc=[0.66, 0.78, 0.99]), name="www|acc|0", value=1))
