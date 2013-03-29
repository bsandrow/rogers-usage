
import requests

homepage_url = 'https://www.rogers.com'
login_submit_url = 'https://www.rogers.com/siteminderagent/forms/login.fcc'

class RogersSession(requests.Session):
    """
    A sub-class of requests.Session that automatically logs into the My
    Rogers account, setting up the session with access to the account info.
    """

    def __init__(self, username, password, **kwargs):
        requests.Session.__init__(self, **kwargs)
        self.headers.update({ 'User-Agent': 'rogers-usage/0.1' })
        self.username = username
        self.password = password
        self.login()

    def login(self):
        """ Login to account using :self.username: and :self.password: """
        login_data = {
            'TARGET'        : 'https://www.rogers.com/web/loginSuccess.jsp',
            'textPassword1' : 'Enter Password',
            'SMAUTHREASON'  : 0,
            'USER'          : self.username,
            'password'      : self.password,
        }
        self.get(homepage_url)
        self.post(login_submit_url, data=login_data)
