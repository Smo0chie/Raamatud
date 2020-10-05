import pandas as pd

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

def loe_ribakood(failinimi):
    import cv2
    from pyzbar.pyzbar import decode
    return decode(cv2.imread(failinimi))[0].data
    

def kr_lisamine():
    uue_raamatu_autor    = input("Autori nimi: ")
    uue_raamatu_pealkiri = input("Raamatu pealkiri: ")
    uue_raamatu_staatus  = input("loetud/poolei/lugemata: ")
    
    koik_raamatud = db_lisa_raamat(uue_raamatu_autor, uue_raamatu_pealkiri, uue_raamatu_staatus)
    
    print(koik_raamatud)

kr_lisamine()
#print(db_loe_raamatud())
#print(loe_ribakood('ribakood.png'))




