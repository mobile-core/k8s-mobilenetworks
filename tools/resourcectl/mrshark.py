#!/usr/bin/env python3.6
# -*- coding: utf-8 -*

"""
    Script Name: mrshark.py
    Script Summary: kubectlコマンドを実行してpodsIp, serviceIpを取得し、
                Wireshark用hostsファイルを作成する
    Author: Moe Kobayashi
    Change History: 2021.09.06... 初版
                2021.09.07... 微修正
                2021.09.09... cmdlineOptionsにデフォルト引数を指定、
                    無効なオプション指定時の動作を追加
                2021.09.29... execKubectlCommandに、
                    リソースがない場合のエラー処理動作を追加
"""


# -------------------------------------------------- #
# 標準モジュール
# -------------------------------------------------- #

import subprocess
import os
import sys
import re


# -------------------------------------------------- #
# cmdlineOptions
# -------------------------------------------------- #
# ツール実行時のオプション一覧
# f5gc, open5gcどちらかを指定し、次の関数に渡す
# -------------------------------------------------- #

def cmdlineOptions(args = sys.argv):
    version = "1.3"

    # オプションがない場合は何もしない
    if len(args) == 1:
        return

    elif "-h" in args or "--help" in args:
        print("")
        print("Usage:")
        print("    python3 mrshark.py [--free5gc] [--open5gs] [--version] [--help]")
        print("")
        print("Optional arguments:")
        print("")
        print("    -f, --f5gc        set the variable 'namespaces' to the string 'f5gc'")
        print("    -o, --open5gs     set the variable 'namespaces' to the string 'open5gs'")
        print("    -v, --version     show version information and exit")
        print("    -h, --help        show this help message and exit")
        print("")
        print("Note:")
        print("No need to give any arguments if you have already defined the namespaces.")
        print("")
        sys.exit()

    elif "-v" in args or "--version" in args:
        print("This is Mr.Shark ver.{}".format(version))
        sys.exit()

    elif "-f" in args or "--f5gc" in args:
        os.environ["namespaces"] = "f5gc"
        print("Create hosts file with f5gc!")

    elif "-o" in args  or "--open5gs" in args:
        os.environ["namespaces"] = "open5gs"
        print("Create hosts file with open5gs!")

    # 無効なオプションが指定された場合はエラー出力
    else:
        print("This args is not exists!")
        sys.exit(0)


# -------------------------------------------------- #
# loadNameSpaces
# -------------------------------------------------- #
# Namespacesが設定されているかチェックする
# f5gc, open5gc以外の場合はプログラムを終了する
# -------------------------------------------------- #

def loadNameSpaces():
    # namespacesが設定されているかチェックし、未設定であれば終了
    if "namespaces" in os.environ:
        ns = os.environ["namespaces"]
    else:
        print("")
        print("You didn't define the namespaces.")
        print("Please run this script again with options or read variables with following commands:")
        print("")
        print("    if you want the file with f5gc -> $ source ~/.k8sfivegrc")
        print("    if you want the file with open5gs -> $ source ~/.k8sfourgrc")
        print("")
        sys.exit()

    if ns == "f5gc" or ns == "open5gs":
        return ns

    # f5gc, open5gs以外のnamespacesが設定されている場合はエラー出力
    else:
        print("This namespaces is unavailable!")
        sys.exit()


# -------------------------------------------------- #
# execKubectlCommand
# -------------------------------------------------- #
# kubectl get service/podsコマンドを実行する
# コマンド実行が失敗した場合はエラーを出力する
# -------------------------------------------------- #

def execKubectlCommand(ns, r):
    try:
        cmd_response = subprocess.check_output(["kubectl", "get", r, "-n", ns, "-o", "wide"], stderr=subprocess.STDOUT)
        
        if "No resources found in" in str(cmd_response):
            raise ValueError("ERROR! No resources found in " + ns + " namespaces.")

        return cmd_response
    
    except subprocess.CalledProcessError:
        print("kubectl failed!", file=sys.stderr)
        sys.exit(1)

    except ValueError as e:
        print(e)
        sys.exit(1)


# -------------------------------------------------- #
# parserCommandOutput
# -------------------------------------------------- #
# kubectlコマンドの取得結果をパースし、変数に格納する
# -------------------------------------------------- #

def parserServiceIp(cmd_service):

    # 配列の7個目までを削除し、要素が7個ずつのリストに区切る
    list = cmd_service.decode().split()
    lists = [list[i:i + 7] for i in range(7, len(list), 7)]

    # output serviceip list
    serviceip = []
    for i in lists:
        #IPがない場合はSkip (e.g. f5gc-amf)
        if i[2] == "None":
            continue

        dict = {
                "address": i[2],
                "name": i[0]+"-service"
        }
        serviceip.append(dict)

    return serviceip


def parserPodsIp(cmd_pods):

    # 配列の11個目までを削除し、要素が9個ずつのリストに区切る
    list = cmd_pods.decode().split()
    lists = [list[i:i + 9] for i in range(11, len(list), 9)]
    
    # output podsip list
    podsip = []
    for i in lists:
        dict = {
                "address": i[5],
                "name": str(re.search("f5gc-[a-z]*", i[0]).group())+"-pod"
        }
        podsip.append(dict)

    return podsip


# -------------------------------------------------- #
# nsBranching
# -------------------------------------------------- #
# 取得したNamespacesに該当するmultusIpを取得する
# -------------------------------------------------- #

def nsBranching(ns):
    if ns == "f5gc":
        multusip = [
            {
                "address": "172.16.10.11",
                "name": "f5gc-ue-multus-n1n2"
            },
            {
                "address": "172.16.10.10",
                "name": "f5gc-gnb-multus-n1n2"
            },
            {
                "address": "192.168.10.10",
                "name": "f5gc-gnb-multus-n3"
            },
            {
                "address": "172.16.10.20",
                "name": "f5gc-amf-multus-n1n2"
            },
            {
                "address": "172.16.30.20",
                "name": "f5gc-smf-multus-n4"
            },
            {
                "address": "192.168.10.20",   
                "name": "f5gc-upf-multus-n3"
            },
            {
                "address": "172.16.30.30",
                "name": "f5gc-upf-multus-n4"
            },
            {
                "address": "192.168.30.31",
                "name": "f5gc-upf-multus-n9"
            },
            {
                "address": "10.96.0.10",
                "name": "kube-system-coredns"
            }
        ]
        return multusip
    else:
        multusip = []
        # open5gs multusip 
        return multusip


# -------------------------------------------------- #
# makeHostsFile
# -------------------------------------------------- #
# 変数に格納した各IPアドレスをhostsファイルに出力する
# -------------------------------------------------- #

def makeHostsFile(ns, multusip, serviceip, podsip):
    
    with open("hosts", "w") as f:
        print("; multus ip", file=f)   
        for i in multusip:
            print(i["address"],"", i["name"], file=f)
        print("", file=f)
        print("; service ip", file=f)
        print("; kubectl get services -n ", ns, "-o wide", file=f)
        for i in serviceip:
            print(i["address"],"", i["name"], file=f)
        print("", file=f)
        print("; pod ip", file=f)
        print("; kubectl get pods -n", ns, "-o wide", file=f)
        for i in podsip:
            print(i["address"],"", i["name"], file=f)
        print("", file=f)
        

# -------------------------------------------------- #
# main
# -------------------------------------------------- #

def main():

    cmdlineOptions()
    
    # namespacesを取得
    ns = loadNameSpaces()

    # kubectlコマンドを実行
    cmd_service = execKubectlCommand(ns, "service")
    cmd_pods = execKubectlCommand(ns, "pods")

    # Parse
    serviceip = parserServiceIp(cmd_service)
    podsip = parserPodsIp(cmd_pods)

    # multusIpを取得
    multusip = nsBranching(ns)

    # hostsファイルを出力
    makeHostsFile(ns, multusip, serviceip, podsip)


if __name__ == "__main__":
    main()


# -------------------------------------------------- #
# EOF
# -------------------------------------------------- #
