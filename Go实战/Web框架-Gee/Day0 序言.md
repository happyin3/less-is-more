# Web框架-Gee

> 摘录于以下文献：
>
> 1.[7天用Go从零实现](https://geektutu.com/post/gee.html)
>
> 练习写作习惯，所以本篇未做调整。
> 
> 后续会持续学习、持续更新；记录个人的学习、分享学习的过程。

## 设计一个框架

大部分时候，我们需要实现一个Web应用，第一反应是应该使用哪个框架。不同的框架设计理念和提供的功能有很大的差别。比如，Python语言的`django`和`flask`，前者大而全，后者小而美。Go语言也是如此，新框架层出不穷，比如`Beego`，`Gin`，`Iris`等。那为什么不直接使用标准库，而必须使用框架呢？在设计一个框架之前，我们需要回答框架核心为我们解决了什么问题。只有理解了这一点，才能想明白我们需要在框架中实现什么功能。

> 为什么没有一个“完备”的框架，集所有框架的优点于一身？

我们先看看标准库`net/http`如何处理一个请求。

```Go
func main() {
    http.HandleFunc("/", handler)
    http.HandleFunc("/count", counter)
    log.Fatal(http.ListenAndServer("localhost:8000", nil))
}

func handler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "URL.Path = %q\n", r.URL.Path)
}
```

`net/http`提供了基础的Web功能，即监听端口，映射静态路由，解析HTTP报文。一些Web开发中简单的需求并不支持，需要手工实现。

* 动态路由：例如`hello/:name`，`hello/*`这类的规则。
* 鉴权：没有分组/统一鉴权的能力，需要在每个路由映射的handler中实现。
* 模板：没有统一简化的HTML机制。
* ...

当我们离开框架，使用基础库时，需要频繁手工处理的地方，就是框架的价值所在。但并不是每一个频繁处理的地方都适合在框架中完成。Python有一个很著名的Web框架，名叫`bottle`，整个框架由`bottle.py`一个文件构成，共4400行，可以说是一个微框架。那么理解整个微框架提供的特性，可以帮助我们理解框架的核心能力。

* 路由（Routing）：将请求映射到函数，支持动态路由。例如：`/hello/:name`。
* 模板（Templates）：使用内置模板引擎提供模板渲染机制。
* 工具集（Utilites）：提供对cookies，headers等机制的处理。
* 插件（Plugin）：Bottle本身功能有限，但提供了插件机制；可以选择安装到全局，也可以只针对某几个路由生效。
* ...

## Gee框架

这个教程将使用 Go 语言实现一个简单的 Web 框架，起名叫做Gee，geektutu.com的前三个字母。我第一次接触的 Go 语言的 Web 框架是Gin，Gin的代码总共是14K，其中测试代码9K，也就是说实际代码量只有5K。Gin也是我非常喜欢的一个框架，与Python中的Flask很像，小而美。

7天实现Gee框架这个教程的很多设计，包括源码，参考了Gin，大家可以看到很多Gin的影子。

时间关系，同时为了尽可能地简洁明了，这个框架中的很多部分实现的功能都很简单，但是尽可能地体现一个框架核心的设计原则。例如Router的设计，虽然支持的动态路由规则有限，但为了性能考虑匹配算法是用Trie树实现的，Router最重要的指标之一便是性能。