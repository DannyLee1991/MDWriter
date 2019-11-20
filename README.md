# MDWiter

一款可以用python生成markdown的工具

## 安装

`pip3 install app`

## 使用方式

此README是由MDWriter生成，具体使用方式可以参考[demo.py](/demo.py "")

## 效果演示:

---

测试文本*倾斜***加粗*****又粗又斜***[添加超链接http://studyai.site](http://studyai.site "")~~删掉这句话~~`Hello MDWriter`

---

- a
- b
- c
   - d
   - e
   - f
      - 1
      - 2
      - 3


---

```

import mdwriter as mdw

code = ""

with mdw.MDWriter("./README.md") as m:
    m.write_element(mdw.MDTitle("MDWiter"))
    m.write_element(mdw.MDTextArea(["一款可以用python生成markdown的工具"]))

    m.write_element(mdw.MDTitle("安装", level=2))
    m.write_element(mdw.MDTextArea([mdw.MDText("pip3 install app", type='`')]))

    m.write_element(mdw.MDTitle("使用方式", level=2))
    m.write_element(mdw.MDTextArea(["此README是由MDWriter生成，具体使用方式可以参考",
                                    mdw.MDHyperlink("demo.py", '/demo.py')]))

    m.write_element(mdw.MDTitle("效果演示:", level=2))

    m.write_element(mdw.MDLine())

    m.write_element(mdw.MDTextArea(
        ["测试文本",
         mdw.MDText("倾斜", type="*"),
         mdw.MDText("加粗", type="**"),
         mdw.MDText("又粗又斜", type="***"),
         mdw.MDHyperlink("添加超链接http://studyai.site", 'http://studyai.site'),
         mdw.MDText('删掉这句话', "~~"),
         mdw.MDText('Hello MDWriter', "`"),
         ]))
    m.write_element(mdw.MDLine())
    m.write_element(mdw.MDList(["a", 'b', 'c', ['d', 'e', 'f', ['1', '2', '3']]]))
    m.write_element(mdw.MDLine())
    m.write_element(mdw.MDCode(code))
    m.write_element(mdw.MDQuote("这是一句引用"))
    m.write_element(mdw.MDImage(img_url='http://b-ssl.duitang.com/uploads/item/201208/30/20120830173930_PBfJE.jpeg',
                                img_title="热气球"))
    m.write_element(mdw.MDTable(headers=["姓名", "技能", "排行"],
                                rows=[
                                    ["刘备", '哭', '大哥'],
                                    ['关于', '打', '二哥'],
                                    ['张飞', '骂', '三弟']
                                ]))

```

> 这是一句引用

![](http://b-ssl.duitang.com/uploads/item/201208/30/20120830173930_PBfJE.jpeg "热气球")

| 姓名 | 技能 | 排行 |
|:-:|:-:|:-:|
| 刘备 | 哭 | 大哥 |
| 关于 | 打 | 二哥 |
| 张飞 | 骂 | 三弟 |


