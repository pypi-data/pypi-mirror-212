def traverse(var, match_cond, action_mode="remove", converter=None):
    """
        遍历 var 找到符合 match_cond 的元素，将其按照 action_mode 指定的操作进行处理

        参数：
            var:                待处理数据
                                    当 var 不是 dict 或者 list 时，将直接返回 var 而不做处理
            match_cond:         <func> 元素的匹配条件
                                    函数类型为 def(parent_type, idx, value): xxxx
                                    其中：
                                        parent_type     该元素源自哪种结构体，有两个可能传入的值： list，dict
                                        idx             该元素在结构体中的位置，对于列表是 index，对于字典是 key
                                        value           元素的值
            action_mode:        <str> 如何对匹配上的元素进行处理
                                    目前支持：
                                        "remove"        将该元素移除
                                        "replace"       将该元素替换为 converter() 处理后的结果
            converter:          <func> 参见 action_mode 中的 "replace" 模式
                                    函数类型为 def(idx, value): xxxx
                                    其中 idx 和 value 的含义参见参数 match_cond 介绍
    """
    assert callable(match_cond)
    assert action_mode in {"replace", "remove"}
    if action_mode == "replace":
        assert callable(converter)

    return recursive_(var, match_cond, action_mode, converter)


def recursive_(var, match_cond, action_mode, converter):
    if isinstance(var, (list, dict)):
        items = reversed(list(enumerate(var))) if isinstance(var, list) else list(var.items())
        for k, v in items:
            if match_cond(type(var), k, v):
                if action_mode == "remove":
                    var.pop(k)
                else:
                    var[k] = converter(k, v)
            else:
                var[k] = recursive_(v, match_cond, action_mode, converter)
    else:
        pass
    return var


if __name__ == '__main__':
    import numpy as np

    x = [
        dict(d=3, c=4),
        np.array([[1, 2, 3]])
    ]

    y1 = traverse(var=x, match_cond=lambda _, k, v: type(v) is np.ndarray, action_mode="replace",
                  converter=lambda k, v: v.tolist())
    print(y1)

    y2 = traverse(var=y1, match_cond=lambda _, k, v: v == 3, action_mode="remove")
    print(y2)
