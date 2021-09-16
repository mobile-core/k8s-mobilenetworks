#!/usr/bin/env python3.6
# -*- coding: utf-8 -*

"""
    Tests for the function of mrshark.py

    Change History: 2021.09.17... 作成
    
"""

import unittest
from unittest.mock import patch
import os
import sys
sys.path.append("../")
import mrshark


class TestMrshark(unittest.TestCase):

    def setUp(self):
        print("setUp")


    def tearDown(self):
        print(os.environ.pop("namespaces", "namespaces is cleared"))
        print("tearDown\n")


    def test_cmdline_options(self):
        # sys.exitで処理が終了になるオプションたち
        list1 = ["-h", "--help", "-v", "--version"]
        for i in list1:
            with self.assertRaises(SystemExit):
                mrshark.cmdlineOptions(i)

        # namespacesを指定するオプションたち
        os.environ["namespaces"] = "f5gc"
        self.assertEqual(mrshark.cmdlineOptions("-f"), os.environ["namespaces"])
        self.assertEqual(mrshark.cmdlineOptions("--f5gc"), os.environ["namespaces"])

        os.environ["namespaces"] = "open5gs"
        self.assertEqual(mrshark.cmdlineOptions("-o"), os.environ["namespaces"])
        self.assertEqual(mrshark.cmdlineOptions("--open5gs"), os.environ["namespaces"])

        # Error Case
        with self.assertRaises(SystemExit):
            mrshark.cmdlineOptions("-a")


    def test_load_namespaces(self):
        # Error Case1
        # namespacesが未定義
        with self.assertRaises(SystemExit):
            mrshark.loadNameSpaces()

        # Error Case2
        # namespacesが想定外の値
        os.environ["namespaces"] = "aaa"
        with self.assertRaises(SystemExit):
            mrshark.loadNameSpaces()

        # Normal Case
        os.environ["namespaces"] = "f5gc"
        ns = os.environ["namespaces"]
        self.assertEqual(mrshark.loadNameSpaces(), ns)

        os.environ["namespaces"] = "open5gs"
        ns = os.environ["namespaces"]
        self.assertEqual(mrshark.loadNameSpaces(), ns)


    def test_exec_kubectl_command(self):
        # たぶん違う
        self.assertTrue(mrshark.execKubectlCommand("f5gc", "service"))
        self.assertTrue(mrshark.execKubectlCommand("f5gc", "pods"))
        self.assertTrue(mrshark.execKubectlCommand("open5gs", "service"))
        self.assertTrue(mrshark.execKubectlCommand("open5gs", "pods"))

        # Error Case
        with self.assertRaises(SystemExit):
            mrshark.execKubectlCommand("f5gc", "aaa")
            mrshark.execKubectlCommand("open5gs", "aaa")


    def test_parser_serviceip(self):
        cmd_service = mrshark.execKubectlCommand("f5gc", "service")
        self.assertNotIn("None", mrshark.parserServiceIp(cmd_service))

        cmd_service = mrshark.execKubectlCommand("open5gs", "service")
        self.assertNotIn("None", mrshark.parserServiceIp(cmd_service))

        # Error Case
        # pods, service等のリソースがない場合
        with self.assertRaises(Exception) as context:
            mrshark.parserServiceIp("cmd_service")
        self.assertFalse("No resources found in" in str(context.exception))


    def test_parser_podsip(self):
        cmd_pods = mrshark.execKubectlCommand("f5gc", "pods")
        self.assertNotIn("None", mrshark.parserPodsIp(cmd_pods))

        cmd_pods = mrshark.execKubectlCommand("open5gs", "pods")
        self.assertNotIn("None", mrshark.parserPodsIp(cmd_pods))

        # Error Case
        # pods, service等のリソースがない場合
        with self.assertRaises(Exception) as context:
            mrshark.parserPodsIp("cmd_pods")
        self.assertFalse("No resources found in" in str(context.exception))


    def test_ns_branching(self):
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

        self.assertEqual(mrshark.nsBranching("f5gc"), multusip_f5gc)
        self.assertEqual(mrshark.nsBranching("open5gs"), multusip_open5gs)


    def test_make_hostsfile(self):
        cmd_service = mrshark.execKubectlCommand("f5gc", "service")
        cmd_pods = mrshark.execKubectlCommand("f5gc", "pods")
        multusip = mrshark.nsBranching("f5gc")
        serviceip = mrshark.parserServiceIp(cmd_service)
        podsip = mrshark.parserPodsIp(cmd_pods)
        self.assertTrue(mrshark.makeHostsFile("f5gc", multusip, serviceip, podsip))

        cmd_service = mrshark.execKubectlCommand("open5gs", "service")
        cmd_pods = mrshark.execKubectlCommand("open5gs", "pods")
        multusip = mrshark.nsBranching("open5gs")
        serviceip = mrshark.parserServiceIp(cmd_service)
        podsip = mrshark.parserPodsIp(cmd_pods)
        self.assertTrue(mrshark.makeHostsFile("open5gs", multusip, serviceip, podsip))

        # Error Case
#        os.chmod("./test", 0o644)
#        with self.assertRaises(PermissionError):
#            mrshark.makeHostsFile("f5gc", "multusip", "serviceip", "podsip")
#            mrshark.makeHostsFile("open5gs", "multusip", "serviceip", "podsip")
        
        # permission deniedになるので要修正
#        os.chdir("../")
#        os.chmod("./test", 0o755)
