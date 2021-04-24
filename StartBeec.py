from Beec import app

if __name__ == '__main__':
    # d = app.run(host='127.0.0.1', port='5000', debug=True, threaded=True, ssl_context=('cert.pem', 'key.pem'))
    d = app.run(host='127.0.0.1', port='5001', debug=True, threaded=True)
