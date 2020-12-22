# Kubernetes環境構築手順

## 概要

* vagrant, virtual boxを利用して構築
* HLD(Teams内の資料を参照)
* Virtual Box ver. 6.1.16 (2020/12/9)
* Vagrant  ver. 2.2.14 (2020/12/9)
* VMベースイメージ centos7

## 構築の概要、下準備
次の2段階で構築
* kubernetes環境のベースとなるVM(vagrant BOX)を作成し、vagrant環境にBOXとして登録
* 1.のBOXを利用し、Master Node x1, Worker Node x2 を作成

## 下準備
各自PCの適当な場所に保存、解凍。
`git clone https://github.com/mobile-core/k8s-mobilenetworks.git/k8s-vagrant`


k8s-vagrantフォルダ内
* "k8s-base" フォルダ： 上記 "構築の概要" 1. ... 用
* "k8s" フォルダ：上記 "構築の概要" 2.  ... 用

以下の手順はPowerShellで説明
## 1. kubernetes環境のベースとなるVM(vagrant BOX)を作成し、vagrant環境にBOXとして登録
PowerShell起動。解凍、設置したVagrantフォルダ > k8s-baseフォルダ へ移動
`cd (設置したフォルダ)\k8s-vagrant\k8s-base`

vagrant up。VM起動、自動設定。

`vagrant up`

VM起動、自動設定が完了したら、Virtual box Guest Additionをインストールするため、一旦VMシャットダウン。

`vagrant halt`

Guest Addition CD イメージの挿入とマウント

GUI > 設定



ストレージ > コントローラー: IDE "左側のアイコン"
"光学ドライブの追加"



「追加」ボタンでisoファイルを選択する。



VirtualBoxをデフォルトでインストールしている場合、
「C:\Program Files\Oracle\VirtualBox」
に"VBoxGuestAdditions.iso"がある。




VBoxGuestAdditions.isoを選択 > あとはOK




再度、設置したVagrantフォルダ > k8s-baseフォルダ から作業

`cd (設置したフォルダ)\k8s-vagrant\k8s-base`

vagrant up。VM起動。2回目は自動設定がスキップされる。

`vagrant up`

VM起動したら、vagrant sshコマンドでVMへ入る。

`vagrant ssh`


管理者権限になって、CDマウントして、Guest Additionのインストール
```
sudo -i
mkdir /mnt/cdrom
mount /dev/sr0 /mnt/cdrom
/mnt/cdrom/VBoxLinuxAdditions.run
```

最後エラーっぽい表示が出力されるが、centosにGUI環境が無い為のエラー(警告)らしい。気にしない。
後かたずけ
```
umount /mnt/cdrom
exit
exit
```

VMからログアウトしたら、VMシャットダウン。

`vagrant halt`

VMのCDアタッチを外す

GUI > 設定



割り当てた光学ドライブを除去しておく




再度、設置したVagrantフォルダ > k8s-baseフォルダ から作業

`cd (設置したフォルダ)\k8s-vagrant\k8s-base`

Boxファイルの生成。k8s-baseフォルダ内に"package.box"が生成される。

`vagrant package`

package.boxをBoxとしてvagrant環境に登録。Box名は"k8s-base"として、後でvagrantfileから参照される。
```
vagrant box list
vagrant box add k8s-base package.box
```

## 2. 1.のBOXを利用し、Master Node x1, Worker Node x2 を作成
解凍、設置したVagrantフォルダ > k8sフォルダ へ移動

`cd (設置したフォルダ)\k8s-vagrant\k8s`

vagrant up。1.で作成したBox "k8s-base"が参照されVM起動、自動設定。

`vagrant up`

VM起動、自動設定が完了したら、Master x1, Worker x2 が存在するか確認

`vagrant status`

各々のノードの名前を確認したら、Masterへsshしてみる。

`vagrant ssh master`

## kubernetes関連コマンド
ノード確認

`kubectl get nodes`

nginx web server POD起動してみる (nginxコンテナイメージをインターネットから取得できるか)

`kubectl run nginx --image=inx`

PODの状態確認

`kubectl get pods`

nginx PODの削除

`kubectl delete pod nginx`
 