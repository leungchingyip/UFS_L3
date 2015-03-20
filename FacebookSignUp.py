from rauth import OAuth2Service
from flask import redirect, request

class FacebookSignUp():
	"""Pass the third party authorize info such as id, secret and url to 
	module OAuth2Service. Comunicate with the third party authorizor."""
	def __init__(self):
		self.service = OAuth2Service(
			name="facebook",
			# Name of the third party authorizor provider
			client_id="",
			client_secret="",
			# ID and secret provide by facebook.
			authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
			)

	def authorize(self):
		"""redirect to facebook authorize page and send callback page, scope, 
		response_type to facebook."""
		return redirect(self.service.get_authorize_url(
			scope='email',
			response_type='code',
			redirect_uri="http://localhost:5000/callback"
			# facebook will send the parameter to this page.
			)
		)

	def callback(self):
		"""Handle parameters facebook send back, return the user id and email"""
		if 'code' not in request.args:
			return None, None, None
		oauth_session = self.service.get_auth_session(
			data={'code': request.args['code'],
					'grant_type': 'authorization_code',
					'redirect_uri': "http://localhost:5000/callback"}
		)
		user = oauth_session.get('me').json()
		return (user['id'],	user['email'])
