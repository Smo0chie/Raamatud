# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SESSION_TYPE']  = 'filesystem'
# Selles kataloogis on nii üleslaetavad ribakoodifailid kui raamatukogu:
app.config['UPLOAD_FOLDER'] = '/home/reenakonn/upload_files/'
app.secret_key = 'jkfwoiel1324j9q8231oqw012asd001d'

@app.route('/', methods=['GET', 'POST'])
def pealeht():
    html = """
        <!DOCTYPE html>
        <html>
        <body>
    """

    if request.method == 'POST':
        html += '<b>Raamatu lisamine:</b> ' + uus_raamat()

    html += '<h1>Uue raamatu lisamine</h1>'
    html += '<h2>Lae ribakood:</h2>'
    html += faili_vorm()
    html += '<h2>Sisesta käsitsi:</h2>'
    html += kasitsi_vorm()

    html += '<h1>Raamatukogu</h1>'
    html += html_raamatute_tabel(db_loe_raamatud())

    html += """
        </body>
        </html>
    """
    return html

def faili_vorm():
    return """
        <form action="/" method="post" enctype = "multipart/form-data">
          <label for="file_upload">Ribakoodi pilt:</label>
          <input type="file" name="file" id="file_upload" />
          <input type="submit" />
        </form>
    """

def kasitsi_vorm():
    return """
        <form action="/" method="post" enctype = "multipart/form-data">
          <label for="autor">Autori nimi:</label>
          <input type="text" id="autor" name="autor" /></br>
          <label for="pealkiri">Pealkiri:</label>
          <input type="text" id="pealkiri" name="pealkiri" /></br>

          <input type="radio" id="loetud"   name="olek" value="loetud" />
          <label for="loetud">Loetud</label>
          <input type="radio" id="pooleli"  name="olek" value="pooleli" />
          <label for="pooleli">Pooleli</label>
          <input type="radio" id="lugemata" name="olek" value="lugemata" />
          <label for="lugemata">Lugemata</label></br>
          <input type="hidden" id="vormi_tyyp" name="vormi_tyyp"
           value="uus_raamat" />
          <input type="submit" />
        </form>
    """

def uus_raamat():
    import os

    if 'file' not in request.files:
        if request.form['vormi_tyyp'] == 'uus_raamat':
            db_lisa_raamat(
                request.form['autor'],
                request.form['pealkiri'],
                request.form['olek']
            )
            return 'Õnnestus!'
        else: # vormi_tyyp on 'oleku_muutus'
            raamatud = db_loe_raamatud()
            raamatud.loc[int(request.form['row_id']), 'Olek'] = request.form['olek']
            raamatud.to_csv(app.config['UPLOAD_FOLDER'] + 'raamatukogu.csv',
                    encoding='utf-8', index = False)
            return 'Muudetud!'
    file = request.files['file']
    if file.filename == '':
        return "Faili nime pole!"
    filename = os.path.join(app.config['UPLOAD_FOLDER'],
                            # secure_filename varjestab erisümbolid failinimes:
                            secure_filename(file.filename))
    file.save(filename)

    raamat = raamat_ribakoodist(filename)
    uue_raamatu_autor    = raamat['Autor']
    uue_raamatu_pealkiri = raamat['Pealkiri']
    uue_raamatu_olek     = 'lugemata'
    db_lisa_raamat(
        uue_raamatu_autor, uue_raamatu_pealkiri, uue_raamatu_olek)
    return 'Õnnestus!'

def html_raamatute_tabel(koik_raamatud):
    str = ''
    str += '<table>'
    str += '<tr>'
    for col in koik_raamatud.columns:
        str += '<th>' + col + '</th>'
    str += '</tr>'
    for i, row in koik_raamatud.iterrows():
        str += '<tr>'
        str += '<td>' + row['Autor'] + '</td>'
        str += '<td>' + row['Pealkiri'] + '</td>'
        str += '<td>'
        str += oleku_vorm(row['Olek'], i)
        str += '</td>'
        str += '</tr>'
    str += '</table>'

    return str

def oleku_vorm(olek, row_id):
    return """
        <form action="/" method="post" enctype = "multipart/form-data">
            <select id="olek" name="olek">
                <option value="loetud"   %s>Loetud</option>
                <option value="pooleli"  %s>Pooleli</option>
                <option value="lugemata" %s>Lugemata</option>
            </select>
            <input type="hidden" id="vormi_tyyp" name="vormi_tyyp"
             value="oleku_muutus" />
            <input type="hidden" id="row_id" name="row_id" value="%d" />
            <input type="submit" />
        </form>
    """ % (
        'selected' if olek == 'loetud'   else '',
        'selected' if olek == 'pooleli'  else '',
        'selected' if olek == 'lugemata' else '',
        row_id
    )


#andmebaasi kood, mis jääb muutumatuks sõltumata kasutajaliidesest
def db_loe_raamatud():
    import pandas as pd

    return pd.read_csv(app.config['UPLOAD_FOLDER'] + 'raamatukogu.csv',
                       encoding='UTF-8')

def db_lisa_raamat(autor, pealkiri, olek):
    raamatud = db_loe_raamatud()
    raamatud = raamatud.append({
        'Autor':    autor,
        'Pealkiri': pealkiri,
        'Olek':  olek
    }, ignore_index = True)
    raamatud.to_csv(app.config['UPLOAD_FOLDER'] + 'raamatukogu.csv',
                    encoding='utf-8', index = False)
    return raamatud

def raamat_ribakoodist(failinimi):
    import cv2
    import isbnlib
    from pyzbar.pyzbar import decode
    isbn = decode(cv2.imread(failinimi))[0].data.decode('ascii')
    meta = isbnlib.meta(isbn)
    return {
        'Autor':    meta['Authors'][0],
        'Pealkiri': meta['Title']
    }

