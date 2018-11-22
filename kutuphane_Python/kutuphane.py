from tkinter import *
import sqlite3 as sql
import tkinter
import datetime
from tkinter import simpledialog
from tkinter import messagebox

vt0 = sql.connect('odunc.sqlite')
imlec0 = vt0.cursor()

vt1=sql.connect("kitap.sqlite")
imlec1=vt1.cursor()

vt2=sql.connect("uye.sqlite")
imlec2=vt2.cursor()

pencere=Tk()

cerceve=Frame(pencere)
cerceve2=Frame(pencere)
cerceve3=Frame(pencere)

cerceve.pack()
pencere.title("Kütüphane Kitap Takip Programı")
pencere.geometry("1100x600")

sifre="12345"

#imlec0.execute("CREATE TABLE IF NOT EXISTS odunc_tablosu (odunc_id INTEGER PRIMARY KEY,value_uye,value_kitap,alis_tarihi,teslim_tarihi)")
def tikla_sec_uye_listesi(evt):
    global temp_value_uye
    global value_uye
    global kitap_id_uye
    temp_value_uye=uye_listesi.get(ANCHOR)
    value_uye=temp_value_uye[1]
    kitap_id_uye=temp_value_uye[0]
    secilen_uye_labeli.config(text=value_uye)

def tikla_sec_odunc_listesi(evt):
    global temp_value_odunc
    global value_odunc
    value_odunc=""
    temp_value_odunc=odunc_listesi.get(ANCHOR)
    if temp_value_odunc!="":
        value_odunc=temp_value_odunc[0]
    else:
        print("hata verme kardaş")
    secilen_odunc_labeli.config(text=value_odunc)

def odunc_teslim_al():
    id = str(value_odunc)
    silme_islemi="DELETE FROM odunc_tablosu WHERE odunc_id='"+id+"'"
    imlec0.execute(silme_islemi)
    vt0.commit()
    odunc_listele()
"""
    imlec0.execute("SELECT value_kitap FROM odunc_tablosu WHERE odunc_id='"+id+"'")
    kitap_teslim_temp=imlec0.fetchone()
    kitap_teslim=kitap_teslim_temp[0]
    print(kitap_teslim)

    #kitabı alan üyenin id sini bulma
    imlec2.execute("SELECT uye_id FROM uye_tablosu WHERE aldigi_kitap='"+ kitap_teslim +"'")
    uye_id_bulma_temp=imlec2.fetchone()
    uye_id_bulma=str(uye_id_bulma_temp[0])
    print("uye id : ",uye_id_bulma)
    

    #bulunan id ye göre uye listesinde aldigi kitap degerini silme
    aldigi_kitap_sil="DELETE aldigi_kitap FROM uye_tablosu WHERE uye_id= '" + uye_id_bulma + "'"
    imlec2.execute(aldigi_kitap_sil)
    imlec2.commit()    

    imlec0.execute("SELECT value_uye  FROM odunc_tablosu WHERE odunc_id='"+id+"'")
    uye_teslim_temp=imlec0.fetchall()
    uye_teslim=uye_teslim_temp[0]
    #print(uye_teslim)
"""
def tikla_sec_kitap_listesi(evt):
    global value_kitap
    global temp_value_kitap
    global kitap_id_kitap
    temp_value_kitap=kitap_listesi.get(ANCHOR)
    value_kitap=temp_value_kitap[1]
    kitap_id_kitap=temp_value_kitap[0]
    secilen_kitap_labeli.config(text=value_kitap)
    
def cerceve_kapat():
    sorgula()

def menuye_don():
    cerceve2.pack_forget()
    cerceve3.pack_forget()
    #cerceve.grid()
    cerceve.pack()
    uye_listele()
    kitap_listele()
    print("")

def ogrenci_islemleri_giris():
    sorgula_uye()
    
def envanter_listele():  #başlangıçta listenin dolu olmasını sağlıyor
    envanter_listesi.delete(0,END)
    imlec1.execute("SELECT kitap_id,kitap_ad FROM kitap_tablosu")
    kitaplar_tablosunun_listesi = []
    kitaplar_tablosunun_listesi += imlec1.fetchall()

    for i in kitaplar_tablosunun_listesi:
        envanter_listesi.insert(END,i)

def envantere_kaydet():
    imlec1.execute("CREATE TABLE IF NOT EXISTS kitap_tablosu (kitap_id INTEGER PRIMARY KEY,kitap_ad)")
    kitap_girisi="INSERT INTO kitap_tablosu(kitap_ad) VALUES ('"+kitap_ad.get()+"')"
    imlec1.execute(kitap_girisi)
    vt1.commit()
    envanter_listele()

def envanter_guncelle():
    
    id = str(value_envanter)
    guncelleme_kodu="UPDATE kitap_tablosu SET kitap_ad='"+kitap_ad.get()+"' WHERE kitap_id = '"+id+"'"
    imlec1.execute(guncelleme_kodu)
    vt1.commit()
    envanter_listele()

def envanterden_sil():
    
    id = str(value_envanter)
    silme_islemi="DELETE FROM kitap_tablosu WHERE kitap_id='"+id+"'"
    imlec1.execute(silme_islemi)
    vt1.commit()
    envanter_listele()
    
odunc_listesi=Listbox(cerceve,width=80,height=15, font=("Helvetica", 10))
odunc_listesi.grid(row=6,column=2,padx=0)
odunc_listesi.bind('<<ListboxSelect>>',tikla_sec_odunc_listesi)

def odunc_listele():
    odunc_listesi.delete(0,END)
    imlec0.execute("SELECT odunc_id,value_uye,value_kitap,alis_tarihi,teslim_tarihi FROM odunc_tablosu")
    odunc_tablosunun_listesi = []
    odunc_tablosunun_listesi += imlec0.fetchall()

    for i in odunc_tablosunun_listesi:
        odunc_listesi.insert(END, i," ")

    search_term = search_var_odunc.get()
    odunc_listesi.delete(0, END)
         
    for item in odunc_tablosunun_listesi:
        if str(search_term).lower() in str(item).lower():
            odunc_listesi.insert(END, item)

search_var_odunc=StringVar()
search_var_odunc.trace("w", lambda name, index, mode: odunc_listele())
entry_odunc = Entry(cerceve,textvariable=search_var_odunc, width=38)
entry_odunc.grid(row=5, column=2, padx=10, pady=3)
	

    #print("__________________________________________________")

def ogrenci_kaydet():
    imlec2.execute("CREATE TABLE IF NOT EXISTS uye_tablosu (uye_id INTEGER PRIMARY KEY,uye_ad)")
    uye_girisi = "INSERT INTO uye_tablosu(uye_ad) VALUES ('" + ogrenci_adsoyad_textbox.get() + "')"

    imlec2.execute(uye_girisi)
    vt2.commit()
    liste_guncelle()

def tikla_sec_envanter_listesi(evt):
    global temp_value_envanter
    global value_envanter
    temp_value_envanter=envanter_listesi.get(ANCHOR)
    value_envanter=temp_value_envanter[0]
    kitap_id_labeli.config(text=value_envanter)

def tikla_sec_uye_listesi3(evt):
    global temp_value
    global value
    temp_value=uye_listesi3.get(ANCHOR)
    value=temp_value[0]
    ogrenci_isleri_bilgilendirme_labeli.config(text=temp_value[1])

def ogrenci_guncelle():
   
    id = str(value)
    guncelleme_kodu = "UPDATE uye_tablosu SET uye_ad='" + ogrenci_adsoyad_textbox.get() + "' WHERE uye_id = '" + id + "'"
    imlec2.execute(guncelleme_kodu)
    vt2.commit()
    liste_guncelle()

def ogrenci_sil():
    id = str(value)
    silme_islemi="DELETE FROM uye_tablosu WHERE uye_id='"+id+"'"
    imlec2.execute(silme_islemi)
    vt2.commit()
    liste_guncelle()

def liste_guncelle():
    uye_listesi3.delete(0,END)
    imlec2.execute("SELECT uye_id,uye_ad FROM uye_tablosu")
    uyeler_tablosunun_listesi = []
    uyeler_tablosunun_listesi += imlec2.fetchall()

    for i in uyeler_tablosunun_listesi:
        uye_listesi3.insert(END, i)

def uye_listele_ogrenciisleri():
    imlec2.execute("SELECT uye_id,uye_ad FROM uye_tablosu")
    uyeler_tablosunun_listesi = []
    uyeler_tablosunun_listesi += imlec2.fetchall()

    for i in uyeler_tablosunun_listesi:
        uye_listesi3.insert(END, i)

def sorgula():
    
    cevap = simpledialog.askstring("Şifre Ekranı", "Yönetici Şifresini Giriniz",
                                parent=pencere)
    if sifre==cevap:
        
        cerceve.pack_forget()
        cerceve2.pack()

    else:
        messagebox.showwarning("Uyarı !","Girdiğiniz şifre yanlış")
        cerceve2.pack_forget()
        cerceve.pack()

def sorgula_uye():
    
    cevap = simpledialog.askstring("Şifre Ekranı", "Yönetici Şifresini Giriniz",
                                parent=pencere)
    if sifre==cevap:
        cerceve.pack_forget()
        cerceve3.pack()
    else:
        messagebox.showwarning("Uyarı !","Girdiğiniz şifre yanlış")
        cerceve3.pack_forget()
        cerceve.pack()

uye_listesi=Listbox(cerceve,width=25,height=15, font=("Helvetica", 12))
uye_listesi.grid(row=6,column=4,padx=5)
uye_listesi.bind('<<ListboxSelect>>',tikla_sec_uye_listesi)

def uye_listele():
    imlec2.execute("SELECT uye_id,uye_ad FROM uye_tablosu")
    uyeler_tablosunun_listesi = []
    uyeler_tablosunun_listesi += imlec2.fetchall()

    for i in uyeler_tablosunun_listesi:
        uye_listesi.insert(END, i," ")

    search_term = search_var_uye.get()
    uye_listesi.delete(0, END)
         
    for item in uyeler_tablosunun_listesi:
        if str(search_term).lower() in str(item).lower():
            uye_listesi.insert(END, item)

search_var_uye=StringVar()
search_var_uye.trace("w", lambda name, index, mode: uye_listele())
entry_uye = Entry(cerceve,textvariable=search_var_uye, width=38)
entry_uye.grid(row=5, column=4, padx=10, pady=3)

kitap_listesi=Listbox(cerceve,width=25,height=15, font=("Helvetica", 12))
kitap_listesi.grid(row=6,column=0,padx=5)
kitap_listesi.bind('<<ListboxSelect>>',tikla_sec_kitap_listesi)

def kitap_listele():
    kitap_listesi.delete(0, END)
    imlec1.execute("SELECT kitap_id,kitap_ad FROM kitap_tablosu")
    kitaplar_tablosunun_listesi = []
    kitaplar_tablosunun_listesi += imlec1.fetchall()

    for i in kitaplar_tablosunun_listesi:
        kitap_listesi.insert(END,i," ")
    
    search_term = search_var_kitap.get()
    kitap_listesi.delete(0, END)
         
    for item in kitaplar_tablosunun_listesi:
        if str(search_term).lower() in str(item).lower():
            kitap_listesi.insert(END, item)

search_var_kitap=StringVar()
search_var_kitap.trace("w", lambda name, index, mode: kitap_listele())
entry_kitap = Entry(cerceve,textvariable=search_var_kitap, width=38)
entry_kitap.grid(row=5, column=0, padx=10, pady=3)

def odunc_al(kitap_id, uye_id):
    imlec1.execute("SELECT kitap_id,kitap_ad FROM kitap_tablosu")

    kitaplar_tablosunun_listesi = []
    kitaplar_tablosunun_listesi += imlec1.fetchall()

    for i in kitaplar_tablosunun_listesi:
        if kitap_id == i[0]:
            #print("bulduk", i[0])
            kitap_ismi = i[1]
            #print(kitap_ismi)

    imlec2.execute("SELECT uye_id,uye_ad FROM uye_tablosu")

    uyeler_tablosunun_listesi = []
    uyeler_tablosunun_listesi += imlec2.fetchall()

    for i in uyeler_tablosunun_listesi:
        if uye_id == i[0]:
            #print("bulduk", i[0])
            uye_ismi = i[1]
            #print(uye_ismi)
    
    guncelleme_kodu_kitap = "UPDATE kitap_tablosu SET kitap_id='" + str(
        kitap_id) + "', suan_kimde='" + uye_ismi + "' WHERE kitap_id = '" + str(kitap_id) + "'"
    guncelleme_kodu_uye = "UPDATE uye_tablosu SET uye_id='" + str(
        uye_id) + "', aldigi_kitap='" + kitap_ismi + "' WHERE uye_id = '" + str(uye_id) + "'"

    alis_tarihi=datetime.datetime.now().strftime ("%d/%m/20%y")
    alis_gunu=datetime.datetime.now().strftime("%d")
    alis_ay=int(datetime.datetime.now().strftime ("%m"))
    alis_yil=int(datetime.datetime.now().strftime ("20%y"))

    teslim_gunu=int(alis_gunu)+15
    teslim_tarihi="1"
    if teslim_gunu>30:
        teslim_gunu-=30
        alis_ay+=1
        if alis_ay >12:
            alis_ay-=12
            alis_yil+=1
            teslim_tarihi=str(teslim_gunu) + "/" + str(alis_ay)+ "/" +str(alis_yil)
            
        else:
            teslim_tarihi=str(teslim_gunu) + "/" + str(alis_ay)+ "/" +str(alis_yil)
            
            

    elif teslim_gunu<30:
        teslim_tarihi=str(teslim_gunu) + "/" + str(alis_ay)+ "/" +str(alis_yil)
        

    imlec0.execute("CREATE TABLE IF NOT EXISTS odunc_tablosu (odunc_id INTEGER PRIMARY KEY,value_uye,value_kitap,alis_tarihi,teslim_tarihi)")
    odunc_girisi="INSERT INTO odunc_tablosu(value_uye,value_kitap,alis_tarihi,teslim_tarihi) VALUES ('"+value_uye+"','"+value_kitap +"  "+"','"+str(alis_tarihi)+"','"+str(teslim_tarihi) +"')"
    
    imlec0.execute(odunc_girisi)
    imlec1.execute(guncelleme_kodu_kitap)
    imlec2.execute(guncelleme_kodu_uye)

    vt0.commit()
    vt1.commit()
    vt2.commit()
    odunc_listele()

def uye_veritabanina_kaydet():
    imlec2.execute("CREATE TABLE IF NOT EXISTS uye_tablosu (uye_id INTEGER PRIMARY KEY,uye_ad)")



    file2=open("uyeler.txt","r")
    uye_listesi=[]

    uye_listesi += file2.readlines()

    for i in range(len(uye_listesi)):

        uye_girisi = "INSERT INTO uye_tablosu(uye_ad) VALUES ('" + uye_listesi[i] + "')"
        print(i+1," ",uye_listesi[i])
        imlec2.execute(uye_girisi)
        vt2.commit()
    file2.close()

def kitap_veritabanina_kaydet():
    imlec1.execute("CREATE TABLE IF NOT EXISTS kitap_tablosu (kitap_id INTEGER PRIMARY KEY,kitap_ad)")



    file=open("kitaplar.txt","r")
    kitap_listesi=[]

    kitap_listesi += file.readlines()

    for i in range(len(kitap_listesi)):

        kitap_girisi = "INSERT INTO kitap_tablosu(kitap_ad) VALUES ('" + kitap_listesi[i] + "')"
        print(i+1," ",kitap_listesi[i])
        imlec1.execute(kitap_girisi)
        vt1.commit()
    file.close()
#cerceve    ->

karsilama_labeli=Label(cerceve,text="KÜTÜPHANE KAYIT TAKİP PROGRAMI",font=30)
karsilama_labeli.grid(row=1,column=2,pady=20)

kitap_listesi_labeli=Label(cerceve,text="   Kitap Listesi  ",font=15)
kitap_listesi_labeli.grid(row=4,column=0)

odunc_listesi_labeli=Label(cerceve,text="   Ödünç Listesi  ",font=15)
odunc_listesi_labeli.grid(row=4,column=2)



uye_listesi_labeli=Label(cerceve,text="   Üye Listesi  ",font=15)
uye_listesi_labeli.grid(row=4,column=4)

secilen_kitap_labeli=Label(cerceve,text="")
secilen_kitap_labeli.grid(row=7,column=0)

secilen_uye_labeli=Label(cerceve,text="")
secilen_uye_labeli.grid(row=7,column=4)

secilen_odunc_labeli=Label(cerceve,text="")
secilen_odunc_labeli.grid(row=7,column=2)

envanter_tamam_butonu=Button(cerceve,width=16,text="Kitap Kayıt İşlemleri",command=cerceve_kapat)
envanter_tamam_butonu.grid(row=8,column=0,pady=10)

uye_islemleri_butonu=Button(cerceve,width=18,text="Öğrenci Kayıt İşlemleri",command=ogrenci_islemleri_giris)
uye_islemleri_butonu.grid(row=9,column=0,pady=10)

created_by=Label(cerceve,text="created_by Muhammet Tan")
created_by.grid(row=10,column=0)

onayla_butonu=Button(cerceve,width=15,text="Ödünç Al",command=lambda : odunc_al(kitap_id_kitap,kitap_id_uye))
onayla_butonu.grid(row=8,column=2)

teslim_al_butonu=Button(cerceve,width=15,text="Teslim Al",command=odunc_teslim_al)
teslim_al_butonu.grid(row=8,column=4)

#print("-------------------------------------------------")
#cerceve2 ->
tamam_butonu=Button(cerceve2,text="    Ekle     ",command=envantere_kaydet)
tamam_butonu.grid(row=5,column=0,pady=10)

sil_butonu=Button(cerceve2,text="    Sil   ",command=envanterden_sil)
sil_butonu.grid(row=5,column=1,pady=10)

guncelle_butonu=Button(cerceve2,text="Kayıt Güncelle",command=envanter_guncelle)
guncelle_butonu.grid(row=5,column=3,pady=10)

menuye_don_butonu=Button(cerceve2,text="Geri Dön",command=menuye_don)
menuye_don_butonu.grid(row=5,column=4,pady=10)

#print("-------------------------------------------------")
kitap_ad=Entry(cerceve2)
ad=kitap_ad.get()
kitap_ad.grid(row=0,column=2,pady=10)

yazar_ad=Entry(cerceve2)
y=yazar_ad.get()
yazar_ad.grid(row=1,column=2,pady=10)

#print("-------------------------------------------------")

kitap_id_labeli=Label(cerceve2,text="kitap sıra no")
kitap_id_labeli.grid(row=3,column=2)



mevcut_sonuc=Label(cerceve2,text="")
mevcut_sonuc.grid(row=4,column=2)

kitap_ad_labeli=Label(cerceve2,text="Kitap        : ")
kitap_ad_labeli.grid(row=0,column=0)



envanter_listesi_labeli=Label(cerceve2,text="    Envanter Listesi     ")
envanter_listesi_labeli.grid(row=4,column=2)

envanter_listesi=Listbox(cerceve2,width=40,height=25,font=12)
envanter_listesi.grid(row=7,column=2,padx=0)
envanter_listesi.bind('<<ListboxSelect>>',tikla_sec_envanter_listesi)

#print("-----------------------------------------------------------------------------------------")
#cerceve3
ogrenci_isleri_karsilama_labeli=Label(cerceve3,text="Öğrenci Kayıt İşlemleri Ekranına Hoş Geldiniz")
ogrenci_isleri_karsilama_labeli.grid(row=0,column=0,pady=20)

ogrenci_isleri_bilgilendirme_labeli=Label(cerceve3,text="")
ogrenci_isleri_bilgilendirme_labeli.grid(row=2,column=1)

ogrenci_id_text=Entry(cerceve3)

ogrenci_isleri_adsoyad_labeli=Label(cerceve3,text="Ad Soyad")
ogrenci_isleri_adsoyad_labeli.grid(row=1,column=0,padx=5)

ogrenci_adsoyad_textbox=Entry(cerceve3)
ogrenci_adsoyad_textbox.grid(row=1,column=1)

menuye_don_butonu=Button(cerceve3,text="Geri Dön",command=menuye_don)
menuye_don_butonu.grid(row=2,column=5,pady=4)

ogrenci_kaydet_butonu=Button(cerceve3,text="Ekle",command=ogrenci_kaydet)
ogrenci_kaydet_butonu.grid(row=2,column=0)

ogrenci_guncelle_butonu=Button(cerceve3,text="Güncelle",command=ogrenci_guncelle)
ogrenci_guncelle_butonu.grid(row=2,column=3)

ogrenci_sil_butonu=Button(cerceve3,text="   Sil    ",command=ogrenci_sil)
ogrenci_sil_butonu.grid(row=2,column=2)

uye_listesi_labeli=Label(cerceve3,text="   Üye Listesi  ")
uye_listesi_labeli.grid(row=4,column=1)

uye_listesi3=Listbox(cerceve3,width=40,height=25, font=("Helvetica", 11))
uye_listesi3.grid(row=5,column=1,pady=5)
uye_listesi3.bind('<<ListboxSelect>>',tikla_sec_uye_listesi3)

#kitap_veritabanina_kaydet()
#uye_veritabanina_kaydet()
odunc_listele()
kitap_listele()
uye_listele_ogrenciisleri()
envanter_listele()
uye_listele()
pencere.mainloop()

