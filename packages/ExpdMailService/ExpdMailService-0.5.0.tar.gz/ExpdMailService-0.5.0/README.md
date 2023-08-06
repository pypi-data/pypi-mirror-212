# ExpdFtpConn

Python wrapper library for upload & download file on Expeditros Ftp Server.


How to install:

    pip install ExpdMailService


How to use with download methods:

    from ExpdMailService.send_mail import SendingMail

    generate_mail = {
        "mail_server": "custapps.expeditors.com", 
        "sender": "greg.he@expeditors.com", 
        "to": "greg.he@expeditors.com", 
        "cc": "greg.he@expeditors.com",
        "subject": f"Event-Writer, File: {path.basename(file)} got response error", 
        "table": pd.DataFrame([]), 
        "branchcode": "SHA",
    }
    SendingMail(**generate_mail) 

    

