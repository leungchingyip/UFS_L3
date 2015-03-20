from flask.ext.login import LoginManager, UserMixin
from model import User
from rauth import OAuth1Service, OAuth2Service


lm = LoginManager(app)

class OAuthSignIn(object):
	def __init__ (self, provider_name):
		self.provider_name = provider_name
		credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
		self.consumer_id = credentials['id']
		self.consumer_secret = credentials['secret']

	def authorize(self):
		pass

	def callback(self):
		pass

	def get_callback_url(self):
		return url_for('oauth_callback', provider=self.provider_name, _external=True)

	@classmethod
	def get_provider(self, provider_name):
		if self.providers is None:
			self.providers = {}
			for provider_class in self.__subclasses__():
				provider = provieder_class()
				self.provider[provider.provider_name] = provider
		return self.providers[provider_name]

class FacebookSignIn(QAuthSignIn):
    def __init__(self):
    super(FacebookSignIn, self).__init__('facebook')
    self.service = OAuth2Service(
        name='facebook',
        client_id=self.consumer_id,
        client_secret=self.consumer_secret,
        authorize_url='https://graph.facebook.com/oauth/authorize',           
        access_token_url='https://graph.facebook.com/oauth/access_token',
        base_url='https://graph.facebook.com/'
    )

    def authorize(self):
    return redirect(self.service.get_authorize_url(
        scope='email',
        response_type='code',
        redirect_uri=self.get_callback_url())

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
	if not current_user.is_anonymous():
		return redirect("/")
	oauth = OAuthSignIn.get_pr5ovieder(provider)
	return oauther.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
	if not current_uer.is_anonymous():
		return redirect("/")
	oauth = OAuthSignIn.get_provider(provider)
	social_id, username, email = oauth.callback()


app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '',
        'secret': ''
    }
}