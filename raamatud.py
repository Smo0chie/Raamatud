import pandas as pd

raamatute_seeria = pd.Series({'G. Orwell "1984"': 'loetud',
                              'V. Aveyard "Red Queen"': 'pooleli',
                              'J Niven "All the Brigth Places"': 'lugemata'})
print(raamatute_seeria)

def lisamine():
    raamatute_seeria = pd.Series({})
    uue_raamatu_autor = input("Autori nimi: ")
    uue_raamatu_pealkiri = input("Raamatu pealkiri jutumärkide sisse:")
    uue_raamatu_staatus = input("loetud/poolei/lugemata: ")
    lisa_raamat_seeriasse = pd.Series({uue_raamatu_autor + " " + uue_raamatu_pealkiri: uue_raamatu_staatus})
    raamatute_seeria = raamatute_seeria.append(lisa_raamat_seeriasse)
    print(raamatute_seeria)
lisamine()

print(raamatute_seeria)
