import os
import pyqrcode
import vobject
# from cloud_api import *
from uuid import uuid4
from flask import Flask, render_template, request, url_for, send_file
# from google.cloud import storage
# from google.oauth2 import service_account

app = Flask(__name__)
app.config['QR_CODES'] = 'qr_codes'
# app.config['BUCKET_NAME'] = 'qrcontact-qrcodes'

# storage_client = storage.Client(credentials=get_credentials())
# bucket = storage_client.bucket(app.config['BUCKET_NAME'])

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

    qrcode_filename = f"{uuid4()}.png"

    qrcode_path = qrcode_filename
    # qrcode_path = os.path.join(app.config['QR_CODES'], qrcode_filename)

    qr_code = pyqrcode.create(qr_code.serialize())
    qr_code.png(qrcode_path, scale=5)
    return send_file(qrcode_path, as_attachment=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

# 
# destination_blob_name = 'f97d354d-36f5-4b88-9f18-a599acb88c66.png'
# source_file_name = 'qr_codes/f97d354d-36f5-4b88-9f18-a599acb88c66.png'
# credentials = service_account.Credentials.from_service_account_file('qrcontact-358817-357b39193389.json')
# storage_client = storage.Client(credentials=credentials)
# bucket = storage_client.bucket(bucket_name)
# blob = bucket.blob(destination_blob_name)

# blob.upload_from_filename(source_file_name)

# print(
#     f"File {source_file_name} uploaded to {destination_blob_name}."
# )