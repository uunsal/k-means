# UFUK REMZİ ÜNSAL  | KÜTÜPHANE KULLANMADAN K-MEAN ALGORİTMASI
# UFUK REMZİ ÜNSAL  |  K-MEAN ALGORITHM WITHOUT LIBRARY
from math import sqrt
import random


def data_read(file):
    satir = file.readline()
    columns = []
    for s in satir.split(","):
        if "\n" in s:
            columns.append(s.split("\n")[0])
        else:
            columns.append(s)

    data = []
    while(satir!=""):
        satir = file.readline()
        row = []
        ekle=True
        for i in satir.split(","):
            if(i!=""):
                if("\n" in i):
                    row.append(i.split("\n")[0])
                else:
                    row.append(i)
            else:
                ekle=False
        if ekle:
            data.append(row)
    file.close()
    DataFrame={}
    for c in columns:
        DataFrame[c] = []
    for d in range(0,len(data)):
        for c in range(0,len(columns)):
            DataFrame[columns[c]].append(data[d][c])
    values=data
    return DataFrame,values,columns


def merkezleri_hesapla(veriler, dagitilmis,values,idno,columns,K):
    #print(values)
    merkezler = {}
    for i in range(0,K):
        merkezler[i]=[]
        for p in range(0,len(columns)):
            merkez = 0
            Ekle = True
            for j in dagitilmis[str(i)]:
                if(p!=idno):
                    merkez+=float(values[j][p])/len(dagitilmis[str(i)])
                    Ekle = True
                else:
                    Ekle = False
            if Ekle:
                merkezler[i].append(merkez)
    #print(merkezler)
    return merkezler



def ortalama_hatalar_hesapla(veriler, dagitilmis, values, param, columns,merkezler):
    ortalama_hatalar = {}
    #print(dagitilmis)
    for d in range(0,len(list(dagitilmis.keys()))):
        ortalama_hatalar["e"+str(d)]=0
        ei = 0
        for j in dagitilmis[list(dagitilmis.keys())[d]]:
                for c in range (0,len(columns)):
                    if(c!=param): # param id kolonu
                        #print(float(values[j][c]),float(merkezler[d][c-1]))
                        ei+=(float(values[j][c])-float(merkezler[d][c-1]))**2
        #print(ei)
        ortalama_hatalar["e"+str(d)]=ei
    E = 0
    for o in ortalama_hatalar:
        E += ortalama_hatalar[o]
    #print(ortalama_hatalar)
    return ortalama_hatalar,E


def elemanları_merkeze_gore_kumele(values, dagitilmis, param, columns, merkezler):
    #print(merkezler)
    print()
    oklid_uzaklıkları = {}
    new_dagitilmis = {}
    for d in dagitilmis:
        new_dagitilmis[d] = []
    for i in range(0,len(values)):
        oklid_uzaklıkları[str(i)]={}
        for m in merkezler:
            oklid = 0
            Ekle=True
            for j in range (0,len(columns)):
                if(j!=param):
                    oklid+= (float(merkezler[m][j-1])-float(values[i][j]))**2
                    ekle=True
                else:
                    ekle = False
            if ekle :
                oklid_uzaklıkları[str(i)]["m-"+str(m)]=sqrt(oklid)
    #print(oklid_uzaklıkları)
    for i in oklid_uzaklıkları:
            index = (list(oklid_uzaklıkları[i].values()).index(min(list(oklid_uzaklıkları[i].values()))))
            #print(i,str(list(oklid_uzaklıkları[i].keys())[index]).split("-")[1])
            new_dagitilmis[str(list(oklid_uzaklıkları[i].keys())[index]).split("-")[1]].append(int(i))
    return new_dagitilmis

def hesap(veriler,dagitilmis,values,columns,E_temp,K):
    merkezler = merkezleri_hesapla(veriler, dagitilmis, values, 0, columns,K)
    ortalama_hatalar, E = ortalama_hatalar_hesapla(veriler, dagitilmis, values, 0, columns, merkezler)
    dagitilmis=elemanları_merkeze_gore_kumele(values, dagitilmis, 0, columns, merkezler)
    # print(ortalama_hatalar,E)
    # print(merkezler)
    # print(dagitilmis)
    # print(E,E_temp)
    return E_temp!=E,E,dagitilmis


def class_sutun_cikar(veriler, values, columns, cno):
    new_columns = []
    for c in range(0,len(columns)):
        if(c!=cno):
            new_columns.append(columns[c])
    new_values = []
    for v in values:
        val = []
        for c1 in  range(0,len(v)):
            if(c1!=cno):
                val.append(v[c1])
        new_values.append(val)

    return veriler,new_columns,new_values


def random_dagit(values, columns,K):
    random_dagitilmis = {}
    for i in range(0,K):
        random_dagitilmis[str(i)] = []
    for r in range(0,len(values)):
        random_dagitilmis[str(random.randint(0, K-1))].append(r)
    #print(random_dagitilmis)
    return random_dagitilmis


def main():
    print("-"*70,"K-Means Kümeleme Algoritması","-"*70,"\n")
    file = open("Iris.csv", "r")
    cno = int(input("class sutunno girin: "))
    idno = int(input("id no girin: "))
    K = int(input("k parametresini giriniz : "))
    veriler_new,values_new,columns_new = data_read(file)
    if(cno!=-1):
        #print("evet")
        veriler_new,columns_new,values_new= class_sutun_cikar(veriler_new,values_new,columns_new,cno)
    #cluster_label = [0,1]
    #dagitilmis = {"0":[0,1,3],"1":[2,4]}
    #print(values)
    dagitilmis = random_dagit(values_new,columns_new,K)

    devam, E_temp, dagitilmis = hesap(veriler_new,dagitilmis,values_new,columns_new,idno,K)
    devam = True

    while(devam):
         devam,E_temp,dagitilmis = hesap(veriler_new,dagitilmis,values_new,columns_new,E_temp,K)

    print(dagitilmis) # --> cluster labels



main()