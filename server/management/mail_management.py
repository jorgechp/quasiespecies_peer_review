import smtplib, ssl


class MailManagement(object):
    def __init__(self, port, password, smtp_server, mail_account) -> None:
        self.__port = port
        self.__smtp_server = smtp_server
        self.__password = password
        self.__mail_account = mail_account

    def send_mail(self, target_mail, text):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.__smtp_server, self.__port, context=context) as server:
            server.login(self.__mail_account, self.__password)
            server.sendmail(self.__mail_account, target_mail, text)

    def send_recovery_mail(self, target_mail, token):
        text = """\
Subject: [QuasiSpecies Peer Review] Recovery password

Hello, it seems that you have request a new password, you would need the following token:
 
{}

If you have not requested a new password, please forget this mail and remove it. Your password is not
going to be changed.

Thanks!

.""".format(token)
        self.send_mail(target_mail, text)


