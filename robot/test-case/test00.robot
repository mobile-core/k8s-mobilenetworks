*** Settings ***
Library  String


*** Variables ***
${hensuu}      Hello World


*** Test Cases ***
Case1
    Logキーワードで変数hensuuをoutputに記録する
    変数hensuuに代入された文字がHello Worldかチェックする

Case2
    変数hensuuの文字を置き換えてoutputに記録する


*** Keywords ***
Logキーワードで変数hensuuをoutputに記録する
    Log    ${hensuu}

変数hensuuに代入された文字がHello Worldかチェックする
    Should Be Equal    ${hensuu}    Hello World

変数hensuuの文字を置き換えてoutputに記録する
    ${okikae}=    Replace String    ${hensuu}    Hello    Hi!
    Log    ${okikae}
