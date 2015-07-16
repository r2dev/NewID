from flask_oauthlib.client import OAuth, OAuthException
from flask import g, url_for, redirect, session, flash, request
from flask.ext.login import current_user, login_required
from .. import oauth, db
from . import social
#twitter module
twitter = oauth.remote_app(
    'twitter',
    consumer_key = 'eaiJAsQC6CBYzYMd2E4SVEopU',
    consumer_secret = 'tHo2SxWMVFiqZ3aj6hgjMRv8jnfAkb3bbfNY9gdbcCZj0IPJ02',
    base_url = 'https://api.twitter.com/1.1/',
    request_token_url = 'https://api.twitter.com/oauth/request_token',
    access_token_url = 'https://api.twitter.com/oauth/access_token',
    authorize_url = 'https://api.twitter.com/oauth/authenticate'
)

@twitter.tokengetter
def get_twitter_token():
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']
@social.route('/twitter/login')
@login_required
def twitter_login():
    callback_url = url_for('social.twitter_oauthorized', next=request.args.get('next'))
    return twitter.authorize(callback=callback_url or request.referer or None)

@social.route('/twitter/logout')
@login_required
def twitter_logout():
    session.pop('twitter_oauth', None)
    current_user.twitter = ""
    current_user.save()
    return redirect(url_for('main.index'))
@social.route('/twitter/oauthorized')
@login_required
def twitter_oauthorized():
    resp = twitter.authorized_response()
    if resp is None:
        flash('You denied the request to sign in')
    else:
        session['twitter_oauth'] = resp
        current_user.twitter = session['twitter_oauth'].get('screen_name')
        current_user.save()

    return redirect(url_for('main.index'))
#spotify module
spotify = oauth.remote_app(
    'spotify',
    consumer_key = '1028f73e68d4426abfd90934fda4996e',
    consumer_secret = 'a922e8feb46b4a78b32dcdd692bba5ae',
    base_url = 'https://accounts.spotify.com',
    request_token_params={'scope': 'user-read-email'},
    request_token_url = None,
    access_token_url = '/api/token',
    authorize_url = 'https://accounts.spotify.com/authorize'
)
@spotify.tokengetter
@login_required
def get_spotify_token():
    return session.get('spotify_oauth')
@social.route('/spotify/login')
@login_required
def spotify_login():
    callback_url = url_for('social.spotify_oauthorized', next=request.args.get('next'), _external=True)
    return spotify.authorize(callback=callback_url or request.referer or None)

@social.route('/spotify/oauthorized')
@login_required
def spotify_oauthorized():
    resp = spotify.authorized_response()
    if resp is None:
        flash('You denied the request to sign in')
    if isinstance(resp, OAuthException):
        flash('Something wrong')
        return redirect(url_for('main.index'))
    session['spotify_oauth'] = (resp['access_token'], '')
    me = spotify.get('https://api.spotify.com/v1/me')
    current_user.spotify = me.data['id']
    current_user.save()
    return redirect(url_for('main.index'))
@social.route('/spotify/logout')
@login_required
def spotify_logout():
    session.pop('spotify_oauth', None)
    current_user.spotify = ""
    current_user.save()
    return redirect(url_for('main.index'))

#instagram
instagram = oauth.remote_app(
    'instagram',
    consumer_key = 'eb6f325f500d4d439385ca0026929893',
    consumer_secret = '9cfe4bb29b9045809ca0895735caa928',
    base_url='https://api.instagram.com/',
    request_token_url=None,
    access_token_url='https://api.instagram.com/oauth/access_token',
    authorize_url='https://api.instagram.com/oauth/authorize'
)
@instagram.tokengetter
def get_instagram_token():
    return session.get('instagram_token')

@social.route('/instagram/login')
@login_required
def instagram_login():
    callback_url = url_for('social.instagram_oauthorized', next=request.args.get('next'), _external=True)
    return instagram.authorize(callback=callback_url or request.referer or None)

@social.route('/instagram/logout')
@login_required
def instagram_logout():
    session.pop('instagram_token', None)
    current_user.instagram = ""
    current_user.save()
    return redirect(url_for('main.index'))

@social.route('/instagram/oauthorized')
@login_required
def instagram_oauthorized():
    resp = instagram.authorized_response()
    if resp is None:
        flash('You denied the request to sign in')
    if isinstance(resp, OAuthException):
        flash('Something wrong')
    else:
        session['instagram_token'] = resp['access_token']
        print(session['instagram_token'])
        current_user.instagram = resp['user'].get('username')
        current_user.save()
    return redirect(url_for('main.index'))
