#!/usr/bin/env python3.6
# -*- coding: utf-8 -*
# test

"""
    Script : mrshark.py



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
# f5gc, open5gcどちらかを指定し、次の関数に渡す。
# -------------------------------------------------- #

def cmdlineOptions():
    version = "1.0"
    args = sys.argv

    if "-h" in args or "-help" in args:
        print("")
        print("Usage:")
        print("    python3 mrbob.py [-free5gc] [-open5gs] [-version] [-help]")
        print("")
        print("Optional arguments:")
        print("")
        print("    -f, -f5gc        set the variable 'namespaces' to the string 'f5gc'")
        print("    -o, -open5gs     set the variable 'namespaces' to the string 'open5gs'")
        print("    -v, -version     show version information and exit")
        print("    -h, -help        show this help message and exit")
        print("")
        print("Note:")
        print("No need to give any arguments if you have already defined the 'namespaces.'")
        print("")
        sys.exit()

    elif "-v" in args or "-version" in args:
        print("This is Mr.Shark ver.{}".format(version))
        sys.exit()

    elif "-f" in args or "-f5gc" in args:
        os.environ["namespaces"] = "f5gc"
        print("Create hosts file with f5gc!")

        loadNameSpaces()

    elif "-o" in args  or "-open5gs" in args:
        os.environ["namespaces"] = "open5gs"
        print("Create hosts file with open5gs!")

        loadNameSpaces()


# -------------------------------------------------- #
# loadNameSpaces
# -------------------------------------------------- #
# rcファイルを読み込み、$namespacesを取得します。
# f5gc, open5gc以外の場合はプログラムを終了します。
# -------------------------------------------------- #

def loadNameSpaces():
    # namespacesが設定されているかチェックし、未設定であれば終了
    if "namespaces" in os.environ:
        ns = os.environ["namespaces"]
    else:
        print("")
        print("You didn't define the 'namespaces.'")
        print("Please run this script again with arguments or read variables with following commands:")
        print("")
        print("    if you want the file with f5gc -> $ source ~/.k8sfivegrc")
        print("    if you want the file with open5gs -> $ source ~/.k8sfourgrc")
        print("")
        sys.exit()
    # print(ns)
    # f5gc

    if ns == "f5gc":
        return ns
    elif ns == "open5gs":
        return ns
    else:
        sys.exit()


# -------------------------------------------------- #
# execKubectlServicesCommand
# -------------------------------------------------- #
# kubectl get servicesコマンドを実行します。
# コマンド実行が失敗した場合はエラーを出力します。
# -------------------------------------------------- #

def execKubectlServicesCommand(ns):
    try:
        cmd_service = subprocess.check_output(["kubectl", "get", "services", "-n", ns, "-o", "wide"], stderr=subprocess.STDOUT)
        # print(cmd_service.decode())
        return cmd_service
    except subprocess.CalledProcessError:
        print("kubectl failed!", file=sys.stderr)
        sys.exit(1)


# -------------------------------------------------- #
# execKubectlPodsCommand
# -------------------------------------------------- #
# kubectl get podsコマンドを実行します。
# コマンド実行が失敗した場合はエラーを出力します。
# -------------------------------------------------- #

def execKubectlPodsCommand(ns):
    try:
        cmd_pods = subprocess.check_output(["kubectl", "get", "pods", "-n", ns, "-o", "wide"], stderr=subprocess.STDOUT)
    # print(cmd_pods.decode())
        return cmd_pods
    except subprocess.CalledProcessError:
        print("kubectl failed!", file=sys.stderr)
        sys.exit(1)


# -------------------------------------------------- #
# parserCommandOutput
# -------------------------------------------------- #
# kubectlコマンドの取得結果をパースし、変数に格納します。
# -------------------------------------------------- #

def parserServiceIp(cmd_service):

    # 配列の14個目までを削除し、要素が7個ずつのリストに区切る
    # f5gc-amfはIPがないので飛ばす
    list = cmd_service.decode().split()
    lists = [list[i:i + 7] for i in range(14, len(list), 7)]

    # output serviceip list
    serviceip = []
    for i in lists:
        dict = {"address": i[2],
                    "name": i[0]+"-service"
                    }
        serviceip.append(dict)
    # print(serviceip)

    return serviceip


def parserPodsIp(cmd_pods):

    ## 配列の11個目までを削除し、要素が9個ずつのリストに区切る
    list = cmd_pods.decode().split()
    lists = [list[i:i + 9] for i in range(11, len(list), 9)]

    

    ## output podsIp list
    podsip = []
    for i in lists:
        dict = {"address": i[5],
                "name": str(re.search("f5gc-[a-z]*", i[0]).group())+"-pod"
                }
        podsip.append(dict)
    # print(podsIp)

    return podsip


# -------------------------------------------------- #
# nsBranching
# -------------------------------------------------- #
# 取得したNamespacesに該当するmultusIpを取得します。
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
# 変数に格納した各IPアドレスをhostsファイルに出力します。
# -------------------------------------------------- #

def makeHostsFile(ns, multusip, serviceip, podsip):
    
    with open("hosts", "w") as f:
        print("; multus ip", file=f)   
        for i in multusip:
            print(i["address"],"", i["name"], file=f)
        print("")
        print("; service ip", file=f)
        print("; kubectl get services -n ", ns, "-o wide", file=f)
        for i in serviceip:
            print(i["address"],"", i["name"], file=f)
        print("")
        print("; pod ip", file=f)
        print("; kubectl get pods -n", ns, "-o wide", file=f)
        for i in podsip:
            print(i["address"],"", i["name"], file=f)
        print("")
        

# -------------------------------------------------- #
# main
# -------------------------------------------------- #

def main():

    cmdlineOptions()
    
    # namespaces取得
    ns = loadNameSpaces()

    # kubectlコマンドを実行
    cmd_service = execKubectlServicesCommand(ns)
    cmd_pods = execKubectlPodsCommand(ns)

    # Parse
    serviceip = parserServiceIp(cmd_service)
    podsip = parserPodsIp(cmd_pods)

    # multusIp取得
    multusip = nsBranching(ns)

    # hostsファイルを出力
    makeHostsFile(ns, multusip, serviceip, podsip)


if __name__ == "__main__":
    main()


# -------------------------------------------------- #
# EOF
# -------------------------------------------------- #
