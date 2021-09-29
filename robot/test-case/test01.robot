*** Settings ***
Suite Teardown    わざと失敗とその後成功を入れ子

*** Variables ***
${hensuu}      Hello World

*** Test Cases ***
けーす1
    単純に実行が成功
    わざと失敗
    その後成功

けーす2
    単純に実行が成功
    わざと失敗

*** Keywords ***
単純に実行が成功
    Log    ${hensuu}

わざと失敗
    Should Be Equal    ${hensuu}    Hello Hello Hello

その後成功
    Should Be Equal    ${hensuu}    Hello World

わざと失敗とその後成功を入れ子
    わざと失敗
    その後成功
