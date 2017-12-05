from email.mime.text import MIMEText
import smtplib
from email.header import Header


class MailSender(object):
    def __init__(self):
        self.my_name = ''
        self.from_address = ''
        self.password = ''
        self.to_address = ''
        self.smtp_server = ''
        self.smtp_server_port = ''

    def send(self, title: str, content: str, success_callback, failed_callback):
        msg = MIMEText(content, 'plain', 'utf-8')
        from_address = self.my_name + '<' + self.from_address + '>'
        msg['From'] = from_address
        msg['To'] = ", ".join(self.to_address)
        msg['Subject'] = Header(title, 'utf-8')

        server = smtplib.SMTP(self.smtp_server, self.smtp_server_port)
        server.set_debuglevel(1)
        try:
            server.login(self.from_address, self.password)
            server.sendmail(self.from_address, self.to_address, msg.as_string())
            success_callback()
        except Exception as e:
            print(e)
            failed_callback(str(e.args))
        finally:
            server.quit()
