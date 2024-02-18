import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Soru 1: Gezinomi veri setini okutunuz.
df = pd.read_excel("datasets/gezinomi.xlsx")
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
df.head()
df.shape
df.info()

# Soru 2:Kaç unique şehir vardır? Frekansları nedir?
df["SaleCityName"].nunique()

#  Soru 3: Kaç unique Concept vardır?
df["ConceptName"].nunique()

# Soru 4: Hangi Concept’den kaçar tane satış gerçekleşmiş?
df["ConceptName"].value_counts()

# Soru 5:Şehirlere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("SaleCityName").agg({"Price": "sum"})

# Soru 6: Concept türlerine göre göre ne kadar kazanılmış?
df.groupby("ConceptName").agg({"Price": "sum"})

# Soru 7: Şehirlere göre PRICE ortalamaları nedir?
df.groupby("SaleCityName").agg({"Price": "mean"})

# Soru 8: Conceptlere göre PRICE ortalamaları nedir?
df.groupby("ConceptName").agg({"Price": "mean"})

# Soru 9: Şehir-Concept kırılımında PRICE ortalamaları nedir?
df.groupby(["SaleCityName", "ConceptName"]).agg({"Price": "mean"})


# Görev 2: SaleCheckInDayDiff değişkenini kategorik bir değişkene çeviriniz.
categories = ["Last Minuters", "Potential Planners", "Planners", "Early Bookers"]
EB_Score = pd.cut(df["SaleCheckInDayDiff"], [-1, 7, 30, 90, df["SaleCheckInDayDiff"].max()], labels=categories)  # max'ı 99999 olarak yapmıştım
df["EB_Score"] = EB_Score


# Görev 3: Şehir-Concept-EB Score, Şehir-Concept- Sezon, Şehir-Concept-CInDay kırılımında ortalama ödenen ücret ve yapılan işlem sayısı cinsinden inceleyiniz?
df.groupby(["SaleCityName", "ConceptName", "EB_Score"]).agg({"Price": ["mean", "count"]})


# Görev 4: City-Concept-Season kırılımının çıktısını PRICE'a göre sıralayınız.
agg_df = df.groupby(["SaleCityName", "ConceptName", "Seasons"]).agg({"Price": "mean"}).sort_values("Price", ascending=False)
# .sort_values("Price", ascending=False) -> price'a göre sırala


# Görev 5: Indekste yer alan isimleri değişken ismine çeviriniz.
agg_df.reset_index(inplace=True)  # price ve diğer değişkenler aynı yatay hizaya geldi


# Görev 6: Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
agg_df["sales_level_based"] = agg_df[["SaleCityName", "ConceptName", "Seasons"]].apply(lambda x: "_".join(x).upper(), axis=1)  # !!


# Görev 7: Yeni müşterileri (personaları) segmentlere ayırınız.
agg_df["SEGMENT"] = pd.qcut(agg_df["Price"], 4, labels=["D", "C", "B", "A"])

# Segmentleri betimleyiniz (Segmentlere göre group by yapıp price mean, max, sum’larını alınız).
agg_df.groupby(["SEGMENT"]).agg({"Price": ["mean", "max", "sum"]})


# Görev 8: Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz.
agg_df.sort_values(by="Price")

new_user = "ANTALYA_HERŞEY DAHIL_HIGH"
agg_df[agg_df["sales_level_based"] == new_user]

