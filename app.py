import os
import io
import pyqrcode
import vobject
from uuid import uuid4
from flask import Flask, render_template, request, url_for, send_file

app = Flask(__name__)
app.config['QR_CODES'] = 'qr_codes'

if not os.path.exists(app.config['QR_CODES']):
    os.mkdir(app.config['QR_CODES'])

app.config['SECRET_KEY'] = 'secret_key'

@app.route('/download', methods=['POST'])
def download():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    full_name = (last_name + ' ' + first_name).rstrip()
    work_phone = request.form['work_phone']
    home_phone = request.form['home_phone']
    email = request.form['email']
    company = request.form['company']

    qr_code = vobject.vCard()
    # first name, last name (create object)
    param = qr_code.add('n')
    param.value = vobject.vcard.Name(family=last_name, given=first_name)
    # full name
    param = qr_code.add('fn')
    param.value = full_name
    # work phone
    param = qr_code.add('tel')
    param.value = work_phone
    param.type_param = 'work'
    # home phone
    param = qr_code.add('tel')
    param.value = home_phone
    param.type_param = 'home'
    # email
    param = qr_code.add('email')
    param.value = email
    #company
    param = qr_code.add('org')
    param.value = company

    qrcode_filename = os.path.join(app.config['QR_CODES'], f"{uuid4()}.png")

    qr_code = pyqrcode.create(qr_code.serialize())
    qr_code.png(qrcode_filename, scale=5)
    return send_file(qrcode_filename, as_attachment=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()