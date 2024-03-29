from flask import render_template, request, jsonify
from app import app
import datetime


def write_log(e):
    with open('logfile', 'a') as file:
        file.write("\n\n" + str(datetime.datetime.now().strftime("%d %b %Y - %H:%M")) + ' - ' + str(e))


def write_logmail(e, message, subject, to):
    with open('mail_logfile', 'a') as file:
        file.writelines("\n\n" + str(datetime.datetime.now().strftime("%d %b %Y - %H:%M")) + " - " + message + str(e))
        file.writelines('\nRecorda enviar email de ' + str(subject) + ' a: ' + str(to))


@app.errorhandler(404)
def page_not_found(e):
    print(e)
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    print(e)
    write_log(e)
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        # Responder con JSON
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    return render_template('500.html'), 500


@app.errorhandler(502)
def badgateway(e):
    print(e)
    write_log(e)
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'Bad Gateway'})
        response.status_code = 502
        return response
    return render_template('500.html'), 502


@app.errorhandler(Exception)
def generalException(e):
    print(e)
    write_log(e)
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'Unexpected error ' + str(e)})
        return response
    return render_template('500.html'), 500
