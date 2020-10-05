import pandas as pd

#andmebaasi kood, mis jääb muutumatujs sõltumata kasutajaliidesest
def db_loe_raamatud():
    return pd.read_csv('raamatukogu.csv', encoding='UTF-8')

def db_lisa_raamat(autor, pealkiri, staatus):
    raamatud = db_loe_raamatud()
    raamatud = raamatud.append({
        'Autor':    autor,
        'Pealkiri': pealkiri,
        'Staatus':  staatus
    }, ignore_index = True)
    raamatud.to_csv('raamatukogu.csv', encoding='utf-8', index = False)
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
    
#kasutajaliidesega asendada
def kr_lisamine(ribakoodi_failinimi = None):
    if ribakoodi_failinimi:
        raamat = raamat_ribakoodist(ribakoodi_failinimi)
        uue_raamatu_autor    = raamat['Autor']
        uue_raamatu_pealkiri = raamat['Pealkiri']
        print('Autor: ',    raamat['Autor'])
        print('Pealkiri: ', raamat['Pealkiri'])
    else:
        uue_raamatu_autor    = input("Autori nimi: ")
        uue_raamatu_pealkiri = input("Raamatu pealkiri: ")
    uue_raamatu_staatus  = input("loetud/poolei/lugemata: ")
    koik_raamatud = db_lisa_raamat(uue_raamatu_autor, uue_raamatu_pealkiri, uue_raamatu_staatus)
    print(koik_raamatud)

while True:
    tegevus = input('Skanneeri(1), lisa raamat käsitsi(2), näita andmebaasi(3), lõpeta(4): ')
    if tegevus == '1':
        kr_lisamine(input('Sisesta pildi faili nimi: '))
    elif tegevus == '2':
        kr_lisamine()
    elif tegevus == '3':
        print(db_loe_raamatud())
    elif tegevus == '4':
        break
    else:
        print('Tundmatu valik.')
        




