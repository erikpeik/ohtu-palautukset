*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  uusikayttaja
    Set Password  salasana1
    Set Password Confirmation  salasana1
    Click Button  Register
    Welcome Page Should Be Open

Register With Too Short Username And Valid Password
    Set Username  us
    Set Password  salasana1
    Set Password Confirmation  salasana1
    Click Button  Register
    Register Page Should Be Open
    Page Should Contain  Username must be at least 3 characters long

Register With Valid Username And Too Short Password
    Set Username  uusikayttaja
    Set Password  sala
    Set Password Confirmation  sala
    Click Button  Register
    Register Page Should Be Open
    Page Should Contain  Password must be at least 8 characters long

Register With Valid Username And Invalid Password
    # salasana ei sisällä halutunlaisia merkkejä
    Set Username  uusikayttaja
    Set Password  salasana
    Set Password Confirmation  salasana
    Click Button  Register
    Register Page Should Be Open
    Page Should Contain  Password must contain at least one non-letter character

Register With Nonmatching Password And Password Confirmation
    Set Username  uusikayttaja
    Set Password  salasana1
    Set Password Confirmation  salasana2
    Click Button  Register
    Register Page Should Be Open
    Page Should Contain  Password and password confirmation do not match

Register With Username That Is Already In Use
    Create User  kalle  kalle123
    Set Username  kalle
    Set Password  salasana1
    Set Password Confirmation  salasana1
    Click Button  Register
    Register Page Should Be Open
    Page Should Contain  Username already exists

*** Keywords ***
Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password Confirmation
    [Arguments]  ${password_confirmation}
    Input Password  password_confirmation  ${password_confirmation}

Reset Application And Go To Register Page
    Reset Application
    Go To Register Page
