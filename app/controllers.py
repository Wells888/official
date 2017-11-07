#coding=utf-8
from app import db
from sqlalchemy import desc
from werkzeug import secure_filename
from models import News, Catalogue, CatalogueItem, ProductImage, Product, ProductImageLink, Case, CaseImage, CaseImageLink, NewsImage
import os
import time

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#product image dir
PRODUCT_IMG_DIR = 'static/images/products'
#case image dir
CASE_IMG_DIR = 'static/images/cases'
#news image dir
NEWS_IMG_DIR = 'static/images/news'
#catalogue_list buffer
CATALOGUE_LIST = []
#catalogue_list changed flag: True for changed
CLG_HAS_CHANGED_FLAG = True

'''
ret data struct:
ret = [
   { 'id': <catalogue_id>, 'name': <catalogue_name>, 'items': [
          {'id': <item_id>, 'name': <item_name>}, ...
   ]}, ...
]

'''
def getCatalogueList():
    global  CATALOGUE_LIST
    if CLG_HAS_CHANGED_FLAG == False:
        return CATALOGUE_LIST
    #else:
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
    CATALOGUE_LIST = ret
    return ret


def addCatalogue(name_str):
    global CLG_HAS_CHANGED_FLAG
    c = Catalogue(name_str)
    db.session.add(c)
    try:
        db.session.commit()
        CLG_HAS_CHANGED_FLAG = True
        return 0
    except Exception,e:
        db.session.rollback()
        print e
        return -1

def addCatalogueItem(name_str, catalogue_id):
    global CLG_HAS_CHANGED_FLAG
    i = CatalogueItem(name_str, catalogue_id)
    db.session.add(i)
    try:
        db.session.commit()
        CLG_HAS_CHANGED_FLAG = True
        return 0
    except Exception,e:
        db.session.rollback()
        print e
        return -1

def delCatalogue(id):
    global CLG_HAS_CHANGED_FLAG
    c = db.session.query(Catalogue).filter(Catalogue.id == id).first()
    db.session.delete(c)
    try:
        db.session.commit()
        CLG_HAS_CHANGED_FLAG = True
        return 0
    except Exception,e:
        db.session.rollback()
        print e
        return -1

def delCatalogueItem(id):
    global CLG_HAS_CHANGED_FLAG
    c = db.session.query(CatalogueItem).filter(CatalogueItem.id == id).first()
    db.session.delete(c)
    try:
        db.session.commit()
        CLG_HAS_CHANGED_FLAG = True
        return 0
    except Exception,e:
        db.session.rollback()
        print e
        return -1

def getFullUrl(dir, name):
    base_url = os.path.join(BASE_DIR, dir)
    return os.path.join(base_url, name)

def getUrl(dir, name):
    return os.path.join(dir, name)

def getSecureName(raw_name):
    id = 'ID' + str(int(time.time())) + '_'
    id_file_name = id + raw_name
    return id_file_name

def addProductImage(image_file):
    raw_name = secure_filename(image_file.filename)
    name = getSecureName(raw_name)
    image = ProductImage(raw_name, name)
    db.session.add(image)
    try:
        db.session.commit()
        image_file.save(getFullUrl(PRODUCT_IMG_DIR, name))
        return 0
    except Exception, e:
        db.session.rollback()
        print e
        return -1

def addCaseImage(image_file):
    raw_name = secure_filename(image_file.filename)
    name = getSecureName(raw_name)
    image = CaseImage(raw_name, name)
    db.session.add(image)
    try:
        db.session.commit()
        image_file.save(getFullUrl(CASE_IMG_DIR, name))
        return 0
    except Exception, e:
        db.session.rollback()
        print e
        return -1


def addNewsImage(image_file):
    raw_name = secure_filename(image_file.filename)
    name = getSecureName(raw_name)
    image = NewsImage(raw_name, name)
    db.session.add(image)
    try:
        db.session.commit()
        image_file.save(getFullUrl(NEWS_IMG_DIR, name))
        return 0
    except Exception, e:
        db.session.rollback()
        print e
        return -1


'''
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


def uploadProductImage(file):
    try:
       file_name = secure_filename(file.filename)
       file_url = getUrlName(file_name)
       image = ProductImage(file_name, file_url)
       file.save(getFullPath(file_url))
       db.session.add(image)
       db.session.commit()
       return 0
    except Exception, e:
        print e
        return -1
'''

def getProductImages():
    images = db.session.query(ProductImage).order_by(desc(ProductImage.id)).all()
    ret = []
    for image in images:
        item = {}
        item['id'] = image.id
        item['name'] = image.raw_name
        item['url'] = getUrl(PRODUCT_IMG_DIR, image.name)
        ret.append(item)
    return ret


def getCaseImages():
    images = db.session.query(CaseImage).order_by(desc(CaseImage.id)).all()
    ret = []
    for image in images:
        item = {}
        item['id'] = image.id
        item['name'] = image.raw_name
        item['url'] = getUrl(CASE_IMG_DIR, image.name)
        ret.append(item)
    return ret


def getNewsImages():
    images = db.session.query(NewsImage).order_by(desc(NewsImage.id)).all()
    ret = []
    for image in images:
        item = {}
        item['id'] = image.id
        item['name'] = image.raw_name
        item['url'] = getUrl(NEWS_IMG_DIR, image.name)
        ret.append(item)
    return ret

def addProduct(date_str, title_str, keywords_str, partno_str, power_str, voltage_str, introduction_str, description_str, catalogue_item_id, image_ids):
    p = Product(date_str, title_str, keywords_str, partno_str, power_str, voltage_str,introduction_str, description_str, catalogue_item_id)
    db.session.add(p)
    try:
        db.session.commit()
    except Exception, e:
        db.session.rollback()
        return -1
    for image_id in image_ids:
        i = ProductImageLink(p.id, image_id)
        db.session.add(i)
    try:
        db.session.commit()
        return 0
    except Exception, e:
        db.session.rollback()
        print e
        return -1

def addCase(date_str, title_str, keywords_str, introduction_str, description_str, image_ids):
    c = Case(date_str, title_str, keywords_str, introduction_str, description_str)
    db.session.add(c)
    try:
        db.session.commit()
    except Exception, e:
        db.session.rollback()
        return -1
    for image_id in image_ids:
        i = CaseImageLink(c.id, image_id)
        db.session.add(i)
    try:
        db.session.commit()
        return 0
    except Exception, e:
        db.session.rollback()
        print e
        return -1


def addNews(date_str, title_str, keywords_str, introduction_str, description_str):
    n = News(date_str, title_str, keywords_str, introduction_str, description_str)
    db.session.add(n)
    try:
        db.session.commit()
        return 0
    except Exception, e:
        db.session.rollback()
        return -1

#curCatalogue: current catalogue, current position in other words.
def curCatalogueRet(catalogue_id, catalogue_name, item_id, item_name):
    return {'catalogue_id': catalogue_id, 'catalogue_name': catalogue_name, 'item_id': item_id, 'item_name': item_name}

def getCurCatalogue(catalogue_id, item_id):
    catalogue_list = getCatalogueList()
    if item_id != -1 and catalogue_id !=-1:
        for catalogue in catalogue_list:
            if catalogue_id == catalogue['id']:
                # has found catalogue by catalogue_id
                for item in catalogue['items']:
                    if item['id'] == item_id:
                        # has found catalogue_item by item_id
                        #return {'catalogue_id': catalogue['id'], 'catalogue_name': catalogue['name'], 'item_id': item['id'], 'item_name': item['name']}
                        return curCatalogueRet(catalogue['id'], catalogue['name'], item['id'], item['name'] )
                # has found catalogue by catalogue_id but hasn't found catalogue_item with that catalogue
                #return  {'catalogue_id': catalogue_id, 'catalogue_name': catalogue['name'], 'item_id': -1, 'item_name': ''}
                return curCatalogueRet(catalogue_id, catalogue['name'], -1, '')
    elif catalogue_id == -1 and item_id == -1:
        for catalogue in catalogue_list:
            for item in catalogue['items']:
                #catalogue and item exists, so return the first item
                #return {'catalogue_id': catalogue['id'], 'catalogue_name': catalogue['name'], 'item_id': item['id'], 'item_name': item['name']}
                return curCatalogueRet(catalogue['id'], catalogue['name'], item['id'], item['name'])
    elif catalogue_id != -1 and item_id == -1:
        #assign the catalogue id but don't assign item id
        #so return the first item
        for catalogue in catalogue_list:
            if catalogue['id'] == catalogue_id:
                for item in catalogue['items']:
                    #return {'catalogue_id': catalogue['id'], 'catalogue_name': catalogue['name'], 'item_id': item['id'], 'item_name': item['name']}
                    return curCatalogueRet(catalogue['id'], catalogue['name'], item['id'], item['name'] )
                #no first item, so return -1
                #return {'catalogue_id': catalogue_id, 'catalogue_name': catalogue['name'], 'item_id': -1, 'item_name': ''}
                return curCatalogueRet(catalogue_id, catalogue['name'], -1, '')
    #not found catalogue and item, so return -1 and ''
    #return {'catalogue_id': -1, 'catalogue_name': '', 'item_id': -1, 'item_name': ''}
    return curCatalogueRet(-1, '', -1, '')

'''
#
#deprecated
#
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
'''

def getProductsSize(cid):
    products = db.session.query(Product).filter(Product.catalogue_item_id == cid).all()
    return len(products)

def getCasesSize():
    cases = db.session.query(Case).all()
    return len(cases)


def getNewesSize():
    news = db.session.query(News).all()
    return len(news)


'''
index: from 0
'''
def getProducts(item_id, index, num):
    if item_id == -1:
        return []
    products = db.session.query(Product).filter(Product.catalogue_item_id == item_id).all()
    data = []
    size = len(products)
    if size > 0:
        for i in range(0, num):
            if(index+i >= size):
                break
            else:
                data.append(products[index+i])
    return data


'''
index: from 0
'''
def getCases(index, num):
    cases = db.session.query(Case).all()
    data = []
    size = len(cases)
    if size > 0:
        for i in range(0, num):
            if(index+i >= size):
                break
            else:
                data.append(cases[index+i])
    return data


'''
index: from 0
'''
def getNewses(index, num):
    newses = db.session.query(News).order_by(desc(News.id)).all()
    data = []
    size = len(newses)
    if size > 0:
        for i in range(0, num):
            if(index+i >= size):
                break
            else:
                data.append(newses[index+i])
    return data


def getProductById(pid):
    if pid == -1:
        return None
    product = db.session.query(Product).filter(Product.id == pid).first()
    return product



def delProductById(pid):
    if pid == -1:
        return -1
    product = db.session.query(Product).filter(Product.id == pid).first()
    db.session.query(ProductImageLink).filter(ProductImageLink.product_id == product.id).delete()
    db.session.delete(product)
    try:
        db.session.commit()
    except Exception, e:
        db.session.rollback()
    return 0


def getCaseById(cid):
    if cid == -1:
        return None
    case = db.session.query(Case).filter(Case.id == cid).first()
    return case


def getNewsById(nid):
    if nid == -1:
        return None
    news = db.session.query(News).filter(News.id == nid).first()
    return news







