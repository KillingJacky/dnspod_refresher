mount a volume to the container's `/data` path, e.g.

~/dnspod <=> /data

Put a configuration file into ~/dnspod

```
#API Token, How to generate: https://support.dnspod.cn/Kb/showarticle/tsid/227/
#ID, Token
login_token = "xxxx,xxxxxxxxxxxxxxxxxxxxxx"

domain = "v2smart.zzz"

sub_list = ["aaa", "bbb", "ccc"]
```