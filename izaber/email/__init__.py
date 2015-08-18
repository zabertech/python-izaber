import smtplib
from email.mime.text import MIMEText

from izaber import config, app_config
from izaber.startup import initializer
from izaber.paths import paths
from izaber.templates import parse

class Mailer(object):
    def load_config(self,**options):
        self.options = options

    def sendmail(self,*args,**kwargs):
        host = self.options.get('host',config.email.host)
        server = smtplib.SMTP(host)
        server.sendmail(*args,**kwargs)
        server.quit()

    def send_basic_email(
              self,
              from_addr,
              to_addrs,
              subject,
              body
          ):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['To'] = ", ".join(to_addrs)
        self.sendmail(from_addr,to_addrs,msg.as_string())

    def send_basic_templated(self,fpath,**kwargs):
        body = self.template_parse(fpath,**kwargs)
        msg = MIMEText(body)
        self.sendmail(from_addr,to_addrs,msg.as_string())

    def template_parse(self,fpath,**tags):
        body = parse(fpath,**tags)
        return body
        


mailer = Mailer()

@initializer('email')
def load_config(**options):
    mailer.load_config(**options)

