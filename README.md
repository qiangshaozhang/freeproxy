使用fofa进行搜索socks5，需要key，如果没有key可以使用下面的语法进行查询

```
protocol=="socks5" && "Version:5 Method:No Authentication(0x00)" && country="CN"
```

将查询后的导出到fofa_results.txt

示范格式

```
127.0.0.1:1080
```

爆破用户名密码可以自行添加到user.txt和pass.txt

可食用的地址输出在valid_proxies.txt中

