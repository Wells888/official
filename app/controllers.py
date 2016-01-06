#coding=utf-8
from app import db
from werkzeug import secure_filename
from models import News, Catalogue, CatalogueItem, Image, Product, ProductImage
import os
import time

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
IMG_DIR = 'static/images'


def getCatalogueList():
    ret = []
    result_list = db.session.query(Catalogue).all()
    for r in result_list:
        catalogue_dict = {}
        catalogue_dict['id'] = r.id
        catalogue_dict['name'] = r.name
        catalogue_dict['items'] = []
        for i in r.items:
            item_dict = {}
            item_dict['id'] = i.id
            item_dict['name'] = i.name
            catalogue_dict['items'].append(item_dict)
        ret.append(catalogue_dict)
    return ret




def addCatalogue(name_str):
    try:
        c = Catalogue(name_str)
        db.session.add(c)
        db.session.commit()
        return 0
    except Exception,e:
        print e
        return -1


def addCatalogueItem(name_str, catalogue_id):
    try:
        i = CatalogueItem(name_str, catalogue_id)
        db.session.add(i)
        db.session.commit()
        return 0
    except Exception,e:
        print e
        return -1


def delCatalogue(id):
    try:
        c = db.session.query(Catalogue).filter(Catalogue.id == id).first()
        db.session.delete(c)
        db.session.commit()
        return 0
    except Exception,e:
        print e
        return -1


def delCatalogueItem(id):
    try:
        c = db.session.query(CatalogueItem).filter(CatalogueItem.id == id).first()
        db.session.delete(c)
        db.session.commit()
        return 0
    except Exception,e:
        print e
        return -1


def getFullPath(url):
    path = os.path.join(BASE_DIR, IMG_DIR)
    #if os.path.exists(path) == False:
    #   os.makedirs(path)
    return os.path.join(path, url)

def getUrl(url):
    return os.path.join(IMG_DIR, url)

def getUrlName(file_name):
    id = 'ID' + str(int(time.time())) + '_'
    id_file_name = id + file_name
    return id_file_name


def uploadImage(file):
    try:
       file_name = secure_filename(file.filename)
       file_url = getUrlName(file_name)
       image = Image(file_name, file_url)
       file.save(getFullPath(file_url))
       db.session.add(image)
       db.session.commit()
       return 0
    except Exception, e:
        print e
        return -1


def getImages():
    images = db.session.query(Image).all()
    ret = []
    for image in images:
        item = {}
        item['id'] = image.id
        item['name'] = image.file_name
        item['url'] = getUrl(image.url)
        ret.append(item)
    return ret

def addProduct(date_str, title_str, keywords_str, partno_str, power_str, voltage_str, introduction_str, description_str, catalogue_item_id, image_ids):
    try:
        p = Product(date_str, title_str, keywords_str, partno_str, power_str, voltage_str,introduction_str, description_str, catalogue_item_id)
        db.session.add(p)
        db.session.commit()
        for image_id in image_ids:
            i = ProductImage(p.id, image_id)
            db.session.add(i)
        db.session.commit()
        return 0
    except Exception, e:
        print e
        return -1



def getCurCatalogue(catalogue_id, item_id):
    CATALOGUES = getCatalogueList()
    if item_id != -1 and catalogue_id !=-1:
        for catalogue in CATALOGUES:
            if catalogue_id == catalogue['id']:
                for item in catalogue['items']:
                    if item['id'] == item_id:
                        return {'catalogue_id': catalogue['id'], 'catalogue_name': catalogue['name'], 'item_id': item['id'], 'item_name': item['name']}
                return  {'catalogue_id': -1, 'catalogue_name': '', 'item_id': -1, 'item_name': ''}
    elif catalogue_id == -1 and item_id == -1:
        for catalogue in CATALOGUES:
            for item in catalogue['items']:
                return {'catalogue_id': catalogue['id'], 'catalogue_name': catalogue['name'], 'item_id': item['id'], 'item_name': item['name']}
    elif catalogue_id != -1 and item_id == -1:
        for catalogue in CATALOGUES:
            if catalogue['id'] == catalogue_id:
                for item in catalogue['items']:
                    return {'catalogue_id': catalogue['id'], 'catalogue_name': catalogue['name'], 'item_id': item['id'], 'item_name': item['name']}
                return {'catalogue_id': catalogue_id, 'catalogue_name': catalogue['name'], 'item_id': -1, 'item_name': ''}
    return {'catalogue_id': -1, 'catalogue_name': '', 'item_id': -1, 'item_name': ''}


def validateCatalogueId(catalogue_id, item_id):
    if catalogue_id == -1 and item_id == -1:
        return False
    CATALOGUES = getCatalogueList()
    for catalogue in CATALOGUES:
        if catalogue['id'] == catalogue_id:
            if item_id == -1:
                return True
            for item in catalogue['items']:
                if item['id'] == item_id:
                    return True
            return False
    return False

def getProductsSize(cid):
    products = db.session.query(Product).filter(Product.catalogue_item_id == cid).all()
    return len(products)

'''
index: from 0
'''
def getProducts(item_id, index, num):
    if item_id == -1:
        return []
    products = db.session.query(Product).filter(Product.catalogue_item_id == item_id).all()
    data = []
    size = len(products)
    for i in range(0, num):
        if(index+i >= size):
            break
        else:
            data.append(products[index+i])
    return data

def getProductById(pid):
    if pid == -1:
        return None
    product = db.session.query(Product).filter(Product.id == pid).first()
    return product






