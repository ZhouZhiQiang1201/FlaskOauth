from flask import Flask, abort, url_for, jsonify
from flask_oauthlib.client import OAuth

app = Flask(__name__)


class Config(object):
    SECRET_KEY = "tlnl;ht90134ukgl;aeyopyuip]ghm"
    DEBUG = True


app.config.from_object(Config)

oauth = OAuth()

oauth.init_app(app)

github = oauth.remote_app(
    name="github",
    consumer_key="96b9929c35ab135576b5",
    consumer_secret="da052fb4eff92b69e8bfcbc43447a68ba7b87335",
    request_token_params={"scope": "user"},
    base_url="https://github.com/",
    request_token_url=None,
    access_token_method="POST",
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize"
)

providers = {
    "github": github
}

profile_endpoints = {
    "github": "user"
}


def get_social_profile(provider, access_token):
    profile_endpoint = profile_endpoints[provider.name]
    response = provider.get(profile_endpoint, token=access_token)

    username = response.data.get("name", "")
    website = response.data.get("blog", "")
    gb = response.dat.get("html_url", "")
    email = response.data.get("email", "")
    bio = response.data.get("bio", "")

    return username, website, gb, email, bio


@app.route("/login/<provider_name>")
def oauth_login(provider_name):
    if provider_name not in providers.keys():
        abort(404)
    callback = url_for(".oauth_callback", provider_name=provider_name, _external=True)
    return providers[provider_name].authorize(callback=callback)


@app.route("/callback/<provider_name>")
def oauth_callback(provider_name):
    print(provider_name)
    if provider_name not in providers.keys():
        abort(404)
    provider = providers[provider_name]
    response = provider.authorized_response()
    if response is not None:
        access_token = response.get("access_token")
    else:
        access_token = None
    if access_token is None:
        return jsonify(err_msg="NO")
    username, website, gb, email, bio = get_social_profile(provider, access_token)
    return jsonify(username=username, website=website, github=gb, email=email, bio=bio)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
