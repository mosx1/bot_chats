import pandas as pd

excel_data = pd.read_excel('4k.xlsx')
data = pd.DataFrame(excel_data, columns=['№ квартиры', 'Имя', 'Ссылка на чат'])

f = 6       #квартир на этаже
lim = 72    #номер последней квартиры
start = 1   #номер вервой квартиры
a = 0


while start <= lim:
    a = 0
    while a <= f:
        if data['№ квартиры'][a] == a:
            print(data['Имя'][a])
        a+=1
    start+= a