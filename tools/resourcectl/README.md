
### setting

スクリプトを所定のディレクトリに配置します。

```bash
$ sudo cp ~/k8s-mobilenetworks/tools/resourcectl/resourcectl /usr/local/bin/resourcectl
$ sudo chmod +x /usr/local/bin/resourcectl
$ cp ~/k8s-mobilenetworks/tools/resourcectl/.k8sfourgrc ~/
$ cp ~/k8s-mobilenetworks/tools/resourcectl/.k8sfivegrc ~/
```

### Use
---

`resourcectl`は環境変数`namespace`を読み取り対象namespace内のPodを操作します。

```bash
$ cat ~/.k8sfivegrc
export namespaces='f5gc'
<snip>
$
```

そのため、操作したいnamespaceに応じてrcファイルを読み込む必要があります。

- 4G

`open5gs`を操作する前に下記のコマンドを実行すること

```bash
$ source ~/.k8sfourgrc
```

- 5G

`free5gc`を操作する前に下記のコマンドを実行すること

```bash
$ source ~/.k8sfivegrc
```

### resourcectl
---

```bash
$ resourcectl -h
Commands to manipulate kubernetes resources

Usage:
  resourcectl [OPTIONS] | [Commands]

Commands:
  node                Operate node resources
  pods                Operate the main container of the Pod
  tcpdump             Operate the pod side container

Options:
  -h, --help          help for resourcectl
$ 
```

### node
---

nodeへsshログインします。

`Node Num`に`resourcectl node list`で得た数字を入力してください。

```bash
$ resourcectl node -h
Commands to manipulate kubernetes resources

Usage:
  resourcectl [Commands] | [Node Num] | [Options] 

Commands:
  list                Show nodes that can be operated

Options:
  -h, --help          help for resourcectl
$ 
```

### pods
---

Pod内のメインコンテナにログインします。

`Pod Num`に`resourcectl pods list`で得た数字を入力してください。

```bash
$ resourcectl pods -h
Commands to manipulate kubernetes resources

Usage:
  resourcectl [Commands] | [Pod Num] | [Options] 

Commands:
  list                Show nodes that can be operated
  deploy              Deploy NFs in sequence
  clear               Delete NFs in sequence

Options:
  -h, --help          help for resourcectl
$ 
```

`Pod Num`には`NF`名を入力してもログイン可能です。

```bash
$ resourcectl pods ue
root@f5gc-ue-77dbf848bf-mstvt:/UERANSIM# 
```


### tcpdump
---

Pod内のtcpdumpコンテナにログインします。

`Pod Num`に`resourcectl tcpdump list`で得た数字を入力してください。

```bash
$ resourcectl tcpdump -h
No resources found in f5gc namespace.
Commands to manipulate kubernetes resources

Usage:
  resourcectl [Commands] | [Pod Num] | [Options] 

Commands:
  list                Show nodes that can be operated
  dump                Start capture
  stop                Stop capture
  get                 Get the capture log

Options:
  -h, --help          help for resourcectl
$ 
```

`dump`を指定することでコンテナ内のシェル`tcpdump.sh`を起動することができます。

`tcpdump.sh`はコンテナ内のifを対象にキャプチャを取得することができます。

ターゲットはデプロイされている全てのコンテナです。

```bash
$ resourcectl tcpdump dump
```

`stop`をしているすることでコンテナ内のシェル`tcpdump.sh`を停止することができます。

ただし、現在のバージョンでは、稀に`tcpdump`が停止しないことがありますが、特段問題はありません。

取得したキャプチャは`/tmp`配下に格納されます。

```bash
$ resourcectl tcpdump stop
```

取得しキャプチャは`get`コマンドを使用することでmasterに転送することが出来ます。

転送したキャプチャはmasterの`/tmp`配下に格納されます。

```bash
$ resourcectl tcpdump get
```
