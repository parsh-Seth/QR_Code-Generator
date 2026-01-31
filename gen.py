import base64

import qrcode
import io
from flask import Flask, jsonify, send_file, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('qrindex.html')

def make_qr(data):
    qr = qrcode.QRCode()
    qr.add_data(data)
    return qr

#force download
@app.route("/gen", methods=['POST'])
def generate():
    data = request.form["linkStr"]

    if data is None:
        return jsonify({'error': 'No data'}), 400
    elif len(data) > 255:
        return jsonify({'error': 'Too long'}) , 400

    qr = make_qr(data)
    img = qr.make_image()

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png', as_attachment=True, download_name=f"qrcode_{data}.png"), 200

@app.route('/show', methods=['POST'])
def show():
    data = request.form["linkStr"]

    if data is None:
        return jsonify({'error': 'No data'}), 400
    elif len(data) > 255:
        return jsonify({'error': 'Too long'}), 400

    qr = make_qr(data)
    img = qr.make_image()
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return render_template("qrindex.html", qr_data=img_b64, value=data)

if __name__ == "__main__":
    app.run(debug=True)

