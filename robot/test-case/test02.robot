*** Settings ***
Library  SSHLibrary
Suite Teardown    テストケースが成功でもエラーでもSSHをクローズ

*** Variables ***
${user}         vagrant
${master-ip}    172.16.33.11
${key-path}     /tmp/id_rsa

*** Test Cases ***
masterにSSH接続してコマンドを実行
    masterに接続
    masterに秘密鍵を使ってログイン
    masterでechoコマンドを打って正常か判定
    Log VariablesキーワードでRobot Frameworkが保持している変数一覧を確認

*** Keywords ***
masterに接続
    Open Connection    ${master-ip}

masterに秘密鍵を使ってログイン
    Login With Public Key    ${user}    ${key-path}

masterでechoコマンドを打って正常か判定
    ${output1} =  Execute Command  echo "SSH to master is OK!"
    Should Be Equal  ${output1}  SSH to master is OK!

Log VariablesキーワードでRobot Frameworkが保持している変数一覧を確認
    ${output2} =  Execute Command  uname -a
    Log Variables

テストケースが成功でもエラーでもSSHをクローズ
    Close All Connections
