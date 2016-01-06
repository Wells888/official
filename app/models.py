#coding=utf-8
from app import db
from datetime import datetime

CONTENT_TYPE_NEWS = 0
CONTENT_TYPE_PRODUCT =1
CONTENT_TYPE_CASE =2


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.INTEGER, primary_key=True)
    date = db.Column(db.DATE, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    keywords = db.Column(db.String(256), nullable=False)
    content = db.Column(db.TEXT, nullable=False)

    def __init__(self, date_str, title_str, keywords_str, content_str):
        self.date = date_str
        self.title = title_str
        self.keywords = keywords_str
        self.content = content_str

    def __repr__(self):
        return '<News(id=%r, date=%r, title=%r, keywords=%r)>' % (self.id, self.date, self.title, self.keywords)


class Catalogue(db.Model):
    __tablename__ = 'catalogue'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    items = db.relationship('CatalogueItem', backref='catalogue', lazy='dynamic')

    def __init__(self, name_str):
        self.name = name_str

    def __repr__(self):
        return '<Catalogue(id=%r, name=%r)>' % (self.id, self.name)


class CatalogueItem(db.Model):
    __tablename__ = 'catalogueitem'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    catalogue_id = db.Column(db.INTEGER, db.ForeignKey('catalogue.id'))
    products = db.relationship('Product', backref='catalogueitem', lazy='dynamic')

    def __init__(self, name_str, catalogue_id):
        self.name = name_str
        self.catalogue_id = catalogue_id

    def __repr__(self):
        return '<CatalogueItem(id=%r, name=%r, catalogue_id=%r)>' % (self.id, self.name, self.catalogue_id)



class Image(db.Model):
    __tablename__ = 'image'
    id = db.Column(db.INTEGER, primary_key=True)
    url = db.Column(db.String(96), nullable=False)
    file_name = db.Column(db.String(64), nullable=False)
    imagelinks = db.relationship('ProductImage', backref='image', lazy='dynamic')

    def __init__(self, file_name_str, url_str):
        self.file_name = file_name_str
        self.url = url_str

    def __repr__(self):
        return '<Image(id=%r, file_name=%r, url=%r)>' % (self.id, self.file_name, self.url)


class ImageLink(db.Model):
    __tablename__ = 'imagelink'
    id = db.Column(db.INTEGER, primary_key=True)
    content_id = db.Column(db.INTEGER, db.ForeignKey('content.id'))
    image_id = db.Column(db.INTEGER, db.ForeignKey('image.id'))

    def __init__(self, content_id, image_id):
        self.content_id = content_id
        self.image_id =image_id

    def __repr__(self):
        return '<ImageLink(id=%r, content_id=%r, image_id=%r)>' % (self.id, self.content_id, self.image_id)


class Content(db.Model):
    __tablename__ = 'content'
    id = db.Column(db.INTEGER, primary_key=True)
    date = db.Column(db.DATE, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    keywords = db.Column(db.String(256), nullable=False)
    introduction = db.Column(db.TEXT, nullable=False)
    description = db.Column(db.TEXT, nullable=False)
    imagelinks = db.relationship('ImageLink', backref='content', lazy='dynamic')

    def __init__(self, date_str, title_str, keywords_str, introduction_str, description_str):
        self.date = date_str
        self.title = title_str
        self.keywords = keywords_str
        self.introduction = introduction_str
        self.description = description_str

    def __repr__(self):
        return '<Content(id=%r, date=%r, title=%r, type=%r, keywords=%r)>' % (self.id, self.date, self.title, self.type, self.keywords)


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.INTEGER, primary_key=True)
    date = db.Column(db.DATE, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    keywords = db.Column(db.String(256), nullable=False)
    partno = db.Column(db.String(32), nullable=False)
    power = db.Column(db.String(32), nullable=False)
    voltage = db.Column(db.String(32), nullable=False)
    introduction = db.Column(db.TEXT, nullable=False)
    description = db.Column(db.TEXT, nullable=False)
    catalogue_item_id =  db.Column(db.INTEGER, db.ForeignKey('catalogueitem.id'))
    images = db.relationship('ProductImage', backref='product', lazy='dynamic')


    def __init__(self, date_str, title_str, keywords_str, partno_str, power_str, voltage_str, introduction_str, description_str, catalogue_item_id):
        self.date = datetime.strptime(date_str, '%Y-%m-%d')
        self.title = title_str
        self.keywords = keywords_str
        self.partno = partno_str
        self.power = power_str
        self.voltage = voltage_str
        self.introduction = introduction_str
        self.description = description_str
        self.catalogue_item_id = catalogue_item_id

    def __repr__(self):
        return '<Product(id=%r, date=%r, title=%r, keywords=%r, partno=%r, power=%r, voltage=%r, introduction=%r, catalogue_item_id=%r)>' % (self.id, self.date, self.title, self.keywords, self.partno, self.power, self.voltage, self.introduction, self.catalogue_item_id)



class ProductImage(db.Model):
    __tablename__ = 'productimage'
    id = db.Column(db.INTEGER, primary_key=True)
    product_id = db.Column(db.INTEGER, db.ForeignKey('product.id'))
    image_id = db.Column(db.INTEGER, db.ForeignKey('image.id'))

    def __init__(self, product_id, image_id):
        self.product_id = product_id
        self.image_id = image_id

    def __repr__(self):
        return '<ProductImage(id=%r, product_id=%r, image_id=%r)>' % (self.id, self.product_id, self.image_id)



class Case(db.Model):
    __tablename__ = 'case'
    id = db.Column(db.INTEGER, primary_key=True)
    date = db.Column(db.DATE, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    keywords = db.Column(db.String(256), nullable=False)
    introduction = db.Column(db.TEXT, nullable=False)
    description = db.Column(db.TEXT, nullable=False)
    imagelinks = db.relationship('CaseImageLink', backref='case', lazy='dynamic')

    def __init__(self, date_str, title_str, keywords_str, introduction_str, description_str):
        self.date = datetime.strptime(date_str, '%Y-%m-%d')
        self.title = title_str
        self.keywords = keywords_str
        self.introduction = introduction_str
        self.description = description_str

    def __repr__(self):
        return '<Case(id=%r, date=%r, title=%r, keywords=%r, introduction=%r)>' % (self.id, self.date, self.title, self.keywords, self.introduction)


class CaseImageLink(db.Model):
    __tablename__ = 'caseimagelink'
    id = db.Column(db.INTEGER, primary_key=True)
    case_id = db.Column(db.INTEGER, db.ForeignKey('case.id'))
    image_id = db.Column(db.INTEGER, db.ForeignKey('caseimage.id'))

    def __init__(self, case_id, image_id):
        self.case_id = case_id
        self.image_id = image_id

    def __repr__(self):
        return '<CaseImageLink(id=%r, case_id=%r, image_id=%r)>' % (self.id, self.case_id, self.image_id)


class CaseImage(db.Model):
    __tablename__ = 'caseimage'
    id = db.Column(db.INTEGER, primary_key=True)
    url = db.Column(db.String(96), nullable=False)
    file_name = db.Column(db.String(64), nullable=False)
    caseimagelinks = db.relationship('CaseImageLink', backref='caseimage', lazy='dynamic')

    def __init__(self, file_name_str, url_str):
        self.file_name = file_name_str
        self.url = url_str

    def __repr__(self):
        return '<CaseImage(id=%r, file_name=%r, url=%r)>' % (self.id, self.file_name, self.url)




