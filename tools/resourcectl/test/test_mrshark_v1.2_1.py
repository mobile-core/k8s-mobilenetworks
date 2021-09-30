#!/usr/bin/env python3.6
# -*- coding: utf-8 -*


import unittest
import difflib
import os
import sys
import mrshark


global_cmd_service = "\
NAME           TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                AGE   SELECTOR \
f5gc-amf       ClusterIP   None             <none>        29518/TCP,38412/SCTP   56d   app=f5gc-amf \
f5gc-gnb       ClusterIP   10.107.248.30    <none>        38412/SCTP,2152/UDP    56d   app=f5gc-gnb \
".encode("utf-8")

global_cmd_pods = "\
NAME                          READY   STATUS    RESTARTS   AGE   IP               NODE    NOMINATED NODE   READINESS GATES \
f5gc-amf-67c4cdbbb7-6vt8g     2/2     Running   20         12d   10.244.104.49    node2   <none>           <none> \
f5gc-gnb-7cdb85bf67-v2x5q     2/2     Running   20         12d   10.244.104.47    node2   <none>           <none> \
".encode("utf-8")


class TestMrshark(unittest.TestCase):

    #sample values
    sample_cmd_service = "NAME           TYPE        CLUSTER-IP       EXTERNAL-IP   \
            PORT(S)                AGE   SELECTOR f5gc-amf       ClusterIP   \
            None             <none>        29518/TCP,38412/SCTP   56d   app=f5gc-amf \
            f5gc-gnb       ClusterIP   10.107.248.30    <none>        \
            38412/SCTP,2152/UDP    56d   app=f5gc-gnb"\
            .encode("utf-8")

    sample_cmd_pods = "NAME                          READY   STATUS    RESTARTS   AGE   \
            IP               NODE    NOMINATED NODE   READINESS GATES \
            f5gc-amf-67c4cdbbb7-6vt8g     2/2     Running   20         12d   \
            10.244.104.49    node2   <none>           <none> f5gc-gnb-7cdb85bf67-v2x5q     \
            2/2     Running   20         12d   10.244.104.47    node2   <none>           <none>"\
            .encode("utf-8")

    sample_serviceip = [
        {
            "address": "10.107.248.30", 
            "name": "f5gc-gnb-service"
        }
    ]

    sample_podsip = [
        {
            "address": "10.244.104.49",
            "name": "f5gc-amf-pod"
        },
        {
            "address": "10.244.104.47",
            "name": "f5gc-gnb-pod"
        }
    ]

    multusip_f5gc = [
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

    multusip_open5gs = []

    ns = ["f5gc", "open5gs", "aaa"]


    def setUp(self):
        print("setUp")


    def tearDown(self):
        print(os.environ.pop("namespaces", "namespaces is cleared"))
        print("tearDown\n")
        self.separator()


    # テスト実行結果の表示用区切り線
    def separator(self):
        print("----------"*6)


    def test_cmdline_options(self):
        # sys.exitで処理が終了になるオプションたち
        list = ["-h", "--help", "-v", "--version"]
        for i in list:
            with self.assertRaises(SystemExit):
                mrshark.cmdlineOptions(i)
        self.separator()

        # namespacesを指定するオプションたち
        dict = {
                    "-f": "f5gc",
                    "--f5gc": "f5gc",
                    "-o": "open5gs",
                    "--open5gs": "open5gs"
                }
        for key, val in dict.items():
            result = mrshark.cmdlineOptions(key)
            # if result is None:
                # return val
            self.assertEqual(val, os.environ["namespaces"])
        self.separator()
                
        # Error Case
        with self.assertRaises(SystemExit):
            mrshark.cmdlineOptions("-a")


    def test_load_namespaces(self):
        # Error Case1
        # namespacesが未定義
        with self.assertRaises(SystemExit):
            mrshark.loadNameSpaces()

        #Normal Case, Error Case2
        #namespacesがf5gc, open5gs, 想定外の値
        for j, name in enumerate(self.ns):
            os.environ["namespaces"] = name
            try:
                self.assertEqual(mrshark.loadNameSpaces(), name)
                # print(mrshark.loadNameSpaces())
            except:
                with self.assertRaises(SystemExit):
                    mrshark.loadNameSpaces()


    def test_exec_kubectl_command(self):
        self.assertEqual(type(mrshark.execKubectlCommand(self.ns[0], "service")), bytes)
        self.assertEqual(type(mrshark.execKubectlCommand(self.ns[0], "pods")), bytes)
        self.assertEqual(type(mrshark.execKubectlCommand(self.ns[1], "service")), bytes)
        self.assertEqual(type(mrshark.execKubectlCommand(self.ns[1], "pods")), bytes)

        # Error Case
        with self.assertRaises(SystemExit):
            mrshark.execKubectlCommand(self.ns[0], "aaa")
            mrshark.execKubectlCommand(self.ns[1], "aaa")


    def test_parser_serviceip(self):
        result = mrshark.parserServiceIp(self.sample_cmd_service)
        self.assertEqual(result, self.sample_serviceip)

        # Error Case
        # pods, service等のリソースがない場合
        with self.assertRaises(Exception) as context:
            mrshark.parserServiceIp("cmd_service")
        self.assertFalse("No resources found in" in str(context.exception))


    def test_parser_podsip(self):
        result = mrshark.parserPodsIp(self.sample_cmd_pods)
        self.assertEqual(result, self.sample_podsip)

        # Error Case
        # pods, service等のリソースがない場合
        with self.assertRaises(Exception) as context:
            mrshark.parserPodsIp("cmd_pods")
        self.assertFalse("No resources found in" in str(context.exception))


    def test_ns_branching(self):
        self.assertEqual(mrshark.nsBranching("f5gc"), self.multusip_f5gc)
        self.assertEqual(mrshark.nsBranching("open5gs"), self.multusip_open5gs)


    def test_make_hostsfile(self):
        # Error Case
        # 書き込み権限がないので作成不可
        os.chmod("./", 0o555)
        with self.assertRaises(PermissionError):
            mrshark.makeHostsFile("f5gc", self.multusip_f5gc, self.sample_serviceip, self.sample_podsip)
        
        os.chmod("./", 0o755)

        # Normal Case
        mrshark.makeHostsFile("f5gc", self.multusip_f5gc, self.sample_serviceip, self.sample_podsip)
        
        #作成済みのhostsdiffと差分比較
        with open("./hosts", mode="r") as hosts, \
            open("./hostsdiff", mode="r") as hostsdiff:
            
            content1 = hosts.readlines()
            content2 = hostsdiff.readlines()
            self.assertEqual(content1, content2)

            # 削除しないと、Error Case実行時にエラーが発生してしまう為
            os.remove('./hosts')

            # 差分表示用
            # diff = difflib.Differ().compare(hosts.readlines(), hostsdiff.readlines())
            # print(diff)


    def test_total(self):
        cmd_service = mrshark.execKubectlCommand("f5gc", "service")
        cmd_pods = mrshark.execKubectlCommand("f5gc", "pods")
        serviceip = mrshark.parserServiceIp(cmd_service)
        podsip = mrshark.parserPodsIp(cmd_pods)
        multusip = mrshark.nsBranching("f5gc")
        self.assertIsNone(mrshark.makeHostsFile("f5gc", multusip, serviceip, podsip))

        # 削除しないと、Error Case実行時にエラーが発生してしまう為
        os.remove('./hosts')
