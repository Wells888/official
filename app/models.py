#coding=utf-8
from app import db
from datetime import datetime

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



class ProductImage(db.Model):
    __tablename__ = 'productimage'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(96), nullable=False)
    raw_name = db.Column(db.String(64), nullable=False)
    imagelinks = db.relationship('ProductImageLink', backref='productimage', lazy='dynamic')

    def __init__(self, raw_name_str, name_str):
        self.raw_name = raw_name_str
        self.name = name_str

    def __repr__(self):
        return '<ProductImage(id=%r, raw_name=%r, name=%r)>' % (self.id, self.raw_name, self.name)


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
    imagelinks = db.relationship('ProductImageLink', backref='product', lazy='dynamic')


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



class ProductImageLink(db.Model):
    __tablename__ = 'productimagelink'
    id = db.Column(db.INTEGER, primary_key=True)
    product_id = db.Column(db.INTEGER, db.ForeignKey('product.id'))
    image_id = db.Column(db.INTEGER, db.ForeignKey('productimage.id'))

    def __init__(self, product_id, image_id):
        self.product_id = product_id
        self.image_id = image_id

    def __repr__(self):
        return '<ProductImageLink(id=%r, product_id=%r, image_id=%r)>' % (self.id, self.product_id, self.image_id)



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
    name = db.Column(db.String(64), nullable=False)
    raw_name = db.Column(db.String(64), nullable=False)
    imagelinks = db.relationship('CaseImageLink', backref='caseimage', lazy='dynamic')

    def __init__(self, raw_name_str, name_str):
        self.raw_name = raw_name_str
        self.name = name_str

    def __repr__(self):
        return '<CaseImage(id=%r, raw_name=%r, name=%r)>' % (self.id, self.raw_name, self.name)



class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.INTEGER, primary_key=True)
    date = db.Column(db.DATE, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    keywords = db.Column(db.String(256), nullable=False)
    introduction = db.Column(db.TEXT, nullable=False)
    description = db.Column(db.TEXT, nullable=False)
    imagelinks = db.relationship('NewsImageLink', backref='news', lazy='dynamic')

    def __init__(self, date_str, title_str, keywords_str, introduction_str, description_str):
        self.date = datetime.strptime(date_str, '%Y-%m-%d')
        self.title = title_str
        self.keywords = keywords_str
        self.introduction = introduction_str
        self.description = description_str

    def __repr__(self):
        return '<News(id=%r, date=%r, title=%r, keywords=%r, introduction=%r)>' % (self.id, self.date, self.title, self.keywords, self.introduction)


class NewsImageLink(db.Model):
    __tablename__ = 'newsimagelink'
    id = db.Column(db.INTEGER, primary_key=True)
    news_id = db.Column(db.INTEGER, db.ForeignKey('news.id'))
    image_id = db.Column(db.INTEGER, db.ForeignKey('newsimage.id'))

    def __init__(self, news_id, image_id):
        self.news_id = news_id
        self.image_id = image_id

    def __repr__(self):
        return '<NewsImageLink(id=%r, news_id=%r, image_id=%r)>' % (self.id, self.news_id, self.image_id)


class NewsImage(db.Model):
    __tablename__ = 'newsimage'
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    raw_name = db.Column(db.String(64), nullable=False)
    imagelinks = db.relationship('NewsImageLink', backref='newsimage', lazy='dynamic')

    def __init__(self, raw_name_str, name_str):
        self.raw_name = raw_name_str
        self.name = name_str

    def __repr__(self):
        return '<NewsImage(id=%r, raw_name=%r, name=%r)>' % (self.id, self.raw_name, self.name)




