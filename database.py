from deta import Deta

deta_key = "b0ihc9w1kgk_h2piYahYtYynJ3e44uP5xLqNS3Tvy9oE"

deta = Deta(deta_key)
db = deta.Base("your_form")

def save_data(name, keywords, img, rest):
    return db.put({"key":name,"keywords":keywords, "image":img, "other details":rest})

def fetch_all():
    res = db.fetch()
    return res.items

def get_product(product_key):
    return db.get(product_key)
