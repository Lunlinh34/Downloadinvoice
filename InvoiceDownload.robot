*** Settings ***
Library           SeleniumLibrary
Library           OperatingSystem
Library           auto_save_pdf.py

*** Variables ***
${URL}                 https://www.meinvoice.vn/tra-cuu
${INVOICE_CODE}        B1HEIRR8N0WP
${DOWNLOAD_DIR}        invoice.pdf
${PRINT_BUTTON_IMAGE}  images/print_button.png
${FILENAME}            invoice.pdf
${ADDRESS_BAR_X}       300
${ADDRESS_BAR_Y}       50

*** Keywords ***

Open Meinvoice Tra Cuu Page
    ${prefs}=    Create Dictionary
    ...    download.default_directory=${DOWNLOAD_DIR}
    ...    download.prompt_for_download=False
    ...    plugins.always_open_pdf_externally=True
    ${options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    Call Method    ${options}    add_experimental_option    prefs    ${prefs}
    Open Browser    ${URL}    chrome    options=${options}
    Maximize Browser Window
    Wait Until Page Contains Element    id=txtCode    timeout=15s

Input Invoice Code
    [Arguments]    ${code}
    Input Text    id=txtCode    ${code}

Click Search Button
    Click Button    id=btnSearchInvoice
    Sleep    3s

Check Invoice Found
    ${not_found}=    Run Keyword And Return Status    Page Should Contain    không tìm thấy hóa đơn
    Run Keyword If    ${not_found}    Log    Không tìm thấy hóa đơn với mã ${INVOICE_CODE}    WARN
    Run Keyword If    not ${not_found}    Log    Tìm thấy hóa đơn, chuẩn bị tải xuống    INFO
    RETURN    not ${not_found}

Remove Overlay If Present
    ${overlay_present}=    Run Keyword And Return Status    Element Should Be Visible    xpath=//div[contains(@class,'ui-widget-overlay')]
    Run Keyword If    ${overlay_present}    Execute JavaScript    document.querySelector('div.ui-widget-overlay').style.display='none'

Click Print Invoice Button
    Remove Overlay If Present
    Wait Until Element Is Visible    id=print-ticket    timeout=10s
    Click Element    id=print-ticket
    Sleep    2s    # Đợi popup Save As hiện ra
    Click Print Button With PyAutoGui    ${PRINT_BUTTON_IMAGE}    ${DOWNLOAD_DIR}    ${FILENAME}    ${ADDRESS_BAR_X}    ${ADDRESS_BAR_Y}

Click Print Button With PyAutoGui
    [Arguments]    ${image_path}    ${save_dir}    ${filename}    ${address_x}    ${address_y}
    Click Print Button    ${image_path}    save_dir=${save_dir}    filename=${filename}    address_bar_coords=(${address_x},${address_y})

Close Meinvoice Browser
    Close Browser

*** Test Cases ***
Tải Hóa Đơn Điện Tử
    Open Meinvoice Tra Cuu Page
    Input Invoice Code    ${INVOICE_CODE}
    Click Search Button
    ${found}=    Check Invoice Found
    Run Keyword If    ${found}    Click Print Invoice Button
    Close Meinvoice Browser
