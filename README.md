# 简介

MdAutoPub：文章多平台发布小工具，主要使用selenium,autogui实现

# 实现方案

## 登录

通过selenium进行平台登录, 登录后保留cookie下次使用

随便使用自己的登录方式，但是登录时间只有30秒哦, 加油

## 代码设计

采用面向对象的思路设计整体架构, 提高扩展性

通过代码或者html标签操作都会涉及到网页变更，但是给用户的操作界面一般变动不大,
所以直接用autogui配合更靠谱,
使用selenium与autogui进行MarkDown文章的格式化与发布

这里目前直接采用 **坐标** 的方式操作，测试使用图标定位方式不准确,
所以，实际使用过程中需要自己调整坐标, 主要就是各个Pusher中的write方法

# 编写MarkDown

MarkDown文件的编写按照旧的形式编写则可，为了获取文章的标题与分类，你需要在MarkDown文件中添加类似如下的开头:

``` example
---
title: 这里是个标题
tag: 这里是文章的一些标签, 逗号分割
---
```

# 使用

## 安装依赖

pip install -r requirements.txt

## 进入 conf 目录，配置平台url和是否启用

如：想自动将文章发送到简书，则修改conf/jianshu.json, Enable为true

``` example
{
  "ENABLE":true,
  "URL":"https://www.jianshu.com/"
}
```

其他平台类似

## 博客markdown文件

将自己的博客md文件放入到项目markdown目录下

## 运行

**注: 调整各个Pusher中的坐标** python Main.py xx.md

## 使用pyinstaller对程序进行打包

pyinstaller -i xxx.ico -n xxx -w -D tkmain.py

# 平台支持

- [x] 博客园 

- [x] 简书 

- [ ] 知乎 

- [ ] CSDN 

- [ ] 豆瓣日志 

- [ ] segmentfault 

- [x] 开源中国 

- [x] 掘金 

- [ ] 今日头条 

- [ ] 微博 

- [ ] 百度百家号 

- [ ] 51CTO 

- [ ] 开发者头条 

- [ ] 微信公众号 

# 代码结构

## conf 相关配置文件

## cookie 登录后保留cookie信息

## core 核心目录, 一般情况勿动

## markdown 放置要处理的markdown文件

## position 界面需要点击的一些定位文件

# 扩展

conf目录下增加配置文件如cnblog.json

core目录下增加同名目录如cnblog, 同时增加文件Pusher.py

# 参考

## [AUTOPUBLISH](https://gitee.com/mirrors/AutoPublish)

## [现有工具-ArtiPub](https://github.com/crawlab-team/artipub)

## [我自己](https://gitee.com/zhaozhiwei_1992/md-auto-pub)

# 问题列表

## driver.get后会阻塞代码，如何处理?

目前是在浏览器增加页签，再关闭就会往后走了, 可以用autogui操作下

## autogui.typewrire输入的文字乱码或者无法输入

这玩意儿就不是用来输入文章的，如果输入汉字还要切换输入法，所以最好ctrl+c,
ctrl+v, 通过pyperclip实现

不过这里pyperclip.paste不管用，目前先用autogui的hotkey直接搞定
