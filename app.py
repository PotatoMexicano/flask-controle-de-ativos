from app import app
from flask import redirect, url_for

@app.errorhandler(404)
def handler_404(_):
    return redirect(url_for('homepage.homepage'))
@app.errorhandler(401)
def handler_401(_):
    return redirect(url_for('auth.auth_user'))
@app.errorhandler(403)
def handler_403(_):
    return redirect(url_for('auth.auth_user'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)