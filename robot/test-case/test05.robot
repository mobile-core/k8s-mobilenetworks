*** Settings ***
Library  SSHLibrary
Suite Teardown    クリーンアップ処理

*** Variables ***
${user}                     vagrant
${master-ip}                172.16.33.11
${key-path}                 /tmp/id_rsa
${vmSide-manifest}          ./manifest/dep-python.yaml
${continerSide-manifest}    /tmp/dep-python.yaml

*** Test Cases ***
テストケース
    masterに接続して秘密鍵を使ってログイン
    masterにk8sマニフェストファイルを転送する
    kubectl applyコマンドでk8s deploymentを生成する
    k8s deploymentが3つPODを生成してRunning状態になるまで10秒x18回待つ
    
    sedコマンドでマニフェストファイル内のreplicas:3を5に書き換える
    
    kubectl applyコマンドでk8s deploymentを生成する
    k8s deploymentが5つPODを生成してRunning状態になるまで10秒x18回待つ

*** Keywords ***
masterに接続して秘密鍵を使ってログイン
    Open Connection    ${master-ip}
    Login With Public Key    ${user}    ${key-path}

masterにk8sマニフェストファイルを転送する
    Put File    ${vmSide-manifest}    ${continerSide-manifest}

kubectl applyコマンドでk8s deploymentを生成する
    ${stdout}   ${stderr}   ${rc}=   Execute Command   kubectl apply -f ${continerSide-manifest}    return_stderr=True    return_rc=True
    Should Be Equal As Integers    ${rc}    0

k8s deploymentが3つPODを生成してRunning状態になるまで10秒x18回待つ
    Wait Until Keyword Succeeds    18x    10s    kubectl get podでRunningが3つ含まれていること

kubectl get podでRunningが3つ含まれていること
    ${stdout}   ${stderr}   ${rc}=   Execute Command   kubectl get pods | grep deploy-python    return_stderr=True    return_rc=True
    Should Be Equal As Integers    ${rc}    0
    Should Contain X Times    ${stdout}    Running    3

sedコマンドでマニフェストファイル内のreplicas:3を5に書き換える
    ${stdout}   ${stderr}   ${rc}=   Execute Command   
    ...    sed -i 's/replicas: 3/replicas: 5/' ${continerSide-manifest}    return_stderr=True    return_rc=True
    Should Be Equal As Integers    ${rc}    0

k8s deploymentが5つPODを生成してRunning状態になるまで10秒x18回待つ
    Wait Until Keyword Succeeds    18x    10s    kubectl get podでRunningが5つ含まれていること

kubectl get podでRunningが5つ含まれていること
    ${stdout}   ${stderr}   ${rc}=   Execute Command   kubectl get pods | grep deploy-python    return_stderr=True    return_rc=True
    Should Be Equal As Integers    ${rc}    0
    Should Contain X Times    ${stdout}    Running    5

クリーンアップ処理
    ${stdout}   ${stderr}   ${rc}=   Execute Command   kubectl delete -f ${continerSide-manifest}    return_stderr=True    return_rc=True
    ${stdout}   ${stderr}   ${rc}=   Execute Command   rm -fr ${continerSide-manifest}    return_stderr=True    return_rc=True
    Close All Connections
