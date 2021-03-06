RPC

RPC（Remote Procedure Call）：远程过程调用，它是一种通过网络从远程计算机程序上请求服务，而不需要了解底层网络技术的思想。

RPC要解决的两个问题：
解决分布式系统中，服务之间的调用问题
远程调用时，要能够像本地调用一样方便，让调用者感知不到远程调用的逻辑

RPC是一种技术思想而非一种规范或协议，场景RPC技术和框架有：
应用级的服务框架：阿里的Dubbo/Dubbox、Google gRPC、Spring Boot/Spring Cloud
远程通信协议：RMI、Socket、SOAP(HTTP XML)、REST(HTTP JSON)
通信框架：MINA、Netty

下面重点介绍三种：
gRPC：是Google公布的开源软件，基于最新的HTTP 2.0协议，并支持常见的众多编程语言。RPC框架是基于HTTP协议实现的，底层使用到了Netty框架的支持；
Thrift：是Facebook的开源RPC框架，主要是一个跨语言的服务开发框架。用户只要在其之上进行二次开发就行，应用对于底层的RPC通讯等都是透明的，不过这个对于用户来说需要学习特定领域语言这个特性，还会有一定成本的；
Dubbo：是阿里集团开源的一个极为出名的RPC框架，在很多互联网公司和企业应用中广泛使用。协议和序列化框架都可以插拔是极其鲜明的特色。

*RPC框架好处

http接口在接口不多、系统与系统交互较少的情况下，解决信息孤岛初期常使用的一种通信手段，优点就是简单、直接、开发方便。

如果是一个大型的网站，内部子系统较多、接口非常多得情况下，RPC框架的好处就显示出来了。

首先就是长连接，不必每次通信都要像http一样去建立连接，减少了网络开销；

其次就是RPC框架一般都有注册中心，有丰富的监控管理；发布、下线接口、动态扩展等，对调用方来说是无感知、统一化的操作。

最后是安全性。

*RPC能解耦服务
完整的RPC框架

在一个典型RPC的使用场景中，包含了服务发现、负载、容错、网络传输、序列化等组件，其中“RPC协议”就指明了程序如何进行网络传输和序列化。


RPC核心功能

RPC的核心功能是指实现一个RPC最重要的功能模块，就是上图中的“RPC”协议部分。一个RPC的核心功能主要有5个部分组成，分别是：客户端、客户端Stub、网络传输模块、服务端Stub、服务端等。



下面分别介绍核心RPC框架的重要组成：
客户端（Client）：服务调用方；
客户端存根（Client Stub）：存放服务端地址信息，将客户端的请求参数数据信息打包成网络信息，再通过网络传输发送给服务端；
服务端存根（Server Stub）：接收客户端发送过来的请求消息并进行解包，然后再调用本地服务进行处理；
服务端（Server）：服务的真正提供者；
Network Service：底层传输，可以是TCP或HTTP。

一次RPC调用流程如下：
服务消费者（Client）客户端通过本地调用的方式调用服务；
客户端存根（Client Stub）接收到调用请求后负责将方法、入参等信息序列化成能够进行网络传输的消息体；
客户端存根（Client Stub）找到远程的服务地址，并且将消息通过网络发送给服务端；
服务端存根（Server Stub）收到消息后进行解码（反序列化操作）；
服务端存根（Server Stub）根据解码结果调用本地的服务进行相关处理；
服务端（Server）本地服务业务处理；
处理结果返回给服务端存根（Server Stub）；
服务端存根（Server Stub）序列化结果；
服务端存根（Server Stub）将结果通过网络发送至消费方；
客户端存根（Client Stub）接收到消息，并进行解码（反序列化）；
服务消费方得到最终结果。
RPC核心之功能实现

RPC的核心功能主要由5个模块组成，如果想要自己实现一个RPC，最简单的方式要实现三个技术点，分别是：
服务寻址
数据流的序列化和反序列化
网络传输
RPC核心之网络传输协议

在RPC中可选的网络传输方式有多种，可以选择TCP协议、UDP协议、HTTP协议。

每一种协议对整体的性能和效率都有不同的影响，如何选择一个正确的网络传输协议，首先要搞明白各种传输协议在RPC中的工作方式。
基于TCP协议的RPC调用

由服务的调用方与服务的提供方建立 Socket 连接，并由服务的调用方通过 Socket 将需要调用的接口名称、方法名称和参数序列化后传递给服务的提供方，服务的提供方反序列化后再利用反射调用相关的方法。

最后将结果返回给服务的调用方，整个基于 TCP 协议的 RPC 调用大致如此。

但是在实例应用中则会进行一系列的封装，如 RMI 便是在 TCP 协议上传递可序列化的 Java 对象。
基于HTTP协议的RPC调用

该方法更像是访问网页一样，只是它的返回结果更加单一简单。

其大致流程为：由服务的调用者向服务的提供者发送请求，这种请求的方式可能是 GET、POST、PUT、DELETE 等中的一种，服务的提供者可能会根据不同的请求方式做出不同的处理，或者某个方法只允许某种请求方式。

而调用的具体方法则是根据 URL 进行方法调用，而方法所需要的参数可能是对服务调用方传输过去的 XML 数据或者 JSON 数据解析后的结果，最后返回 JOSN 或者 XML 的数据结果。

由于目前有很多开源的 Web 服务器，如 Tomcat，所以其实现起来更加容易，就像做 Web 项目一样。
两种方式对比

基于 TCP 的协议实现的 RPC 调用，由于 TCP 协议处于协议栈的下层，能够更加灵活地对协议字段进行定制，减少网络开销，提高性能，实现更大的吞吐量和并发数。

但是需要更多关注底层复杂的细节，实现的代价更高。同时对不同平台，如安卓，iOS 等，需要重新开发出不同的工具包来进行请求发送和相应解析，工作量大，难以快速响应和满足用户需求。

基于 HTTP 协议实现的 RPC 则可以使用 JSON 和 XML 格式的请求或响应数据。

而 JSON 和 XML 作为通用的格式标准（使用 HTTP 协议也需要序列化和反序列化，不过这不是该协议下关心的内容，成熟的 Web 程序已经做好了序列化内容），开源的解析工具已经相当成熟，在其上进行二次开发会非常便捷和简单。

但是由于 HTTP 协议是上层协议，发送包含同等内容的信息，使用 HTTP 协议传输所占用的字节数会比使用 TCP 协议传输所占用的字节数更高。

因此在同等网络下，通过 HTTP 协议传输相同内容，效率会比基于 TCP 协议的数据效率要低，信息传输所占用的时间也会更长，当然压缩数据，能够缩小这一差距。

