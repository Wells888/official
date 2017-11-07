from app import app
from flask import render_template, request, jsonify, abort, redirect
import controllers
import math

#list size per page
PAGE_LIST_SIZE = 4


#index from 1
def getItemActives(index):
    actives = ['','','','','','','']
    actives[index-1] =  'item-active'
    return actives

@app.route('/')
def do_home_page():
    actives = getItemActives(1)
    newses = controllers.getNewses(0, 4)
    catalogues = controllers.getCatalogueList()
    return render_template('home.html', item_actives = actives, catalogues = catalogues, newses = newses)


@app.route('/service')
def do_service_page():
    actives = getItemActives(6)
    catalogues = controllers.getCatalogueList()
    return render_template('service.html', item_actives = actives, catalogues = catalogues)

@app.route('/contact')
def do_contact_page():
    actives = getItemActives(7)
    catalogues = controllers.getCatalogueList()
    return render_template('contact.html', item_actives = actives, catalogues = catalogues)

@app.route('/about')
def do_about_page():
    actives = getItemActives(2)
    catalogues = controllers.getCatalogueList()
    return render_template('about.html', item_actives = actives, catalogues = catalogues)

@app.route('/product', methods=['GET'])
def product():
    catalogue = {}
    catalogue['item'] = {}
    try:
        catalogue['id'] = int(request.args.get('cid', -1))
        catalogue['item']['id'] = int(request.args.get('itemid', -1))
        page = int(request.args.get('page', 1))
    except ValueError:
        abort(404)
    else:
        data = controllers.getCurCatalogue(catalogue['id'], catalogue['item']['id'])
        catalogue['id'] = data['catalogue_id']
        catalogue['name'] = data['catalogue_name']
        catalogue['item']['id'] = data['item_id']
        catalogue['item']['name'] = data['item_name']
        catalogues = controllers.getCatalogueList()
        products_size = controllers.getProductsSize(catalogue['item']['id'])
        page_size = int(math.ceil(float(products_size)/float(PAGE_LIST_SIZE)))
        if page > page_size:
            page = page_size
        elif page < 1:
            page = 1
        products = controllers.getProducts(catalogue['item']['id'], (page-1)*PAGE_LIST_SIZE, PAGE_LIST_SIZE)
        actives = getItemActives(4)
        return render_template('product.html', item_actives = actives, catalogues = catalogues, cur_catalogue = catalogue, products = products, page = page, page_size = page_size)


@app.route('/case', methods=['GET'])
def case():
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        abort(404)
    else:
        catalogues = controllers.getCatalogueList()
        cases_size = controllers.getCasesSize()
        page_size = int(math.ceil(float(cases_size)/float(PAGE_LIST_SIZE)))
        if page > page_size:
            page = page_size
        elif page < 1:
            page = 1
        cases = controllers.getCases((page-1)*PAGE_LIST_SIZE, PAGE_LIST_SIZE)
        actives = getItemActives(5)
        return render_template('case.html', item_actives = actives, catalogues = catalogues, cases_size = cases_size,  cases = cases, page = page, page_size = page_size)


@app.route('/news', methods=['GET'])
def news():
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        abort(404)
    else:
        catalogues = controllers.getCatalogueList()
        newses_size = controllers.getNewesSize()
        page_size = int(math.ceil(float(newses_size)/float(PAGE_LIST_SIZE)))
        if page > page_size:
            page = page_size
        elif page < 1:
            page = 1
        newses = controllers.getNewses((page-1)*(PAGE_LIST_SIZE), (PAGE_LIST_SIZE))
        actives = getItemActives(3)
        return render_template('news.html', item_actives = actives, catalogues = catalogues, newses =newses, page = page, page_size = page_size)




@app.route('/product_details', methods=['GET'])
def do_product_details_page():
    try:
         pid = int(request.args.get('pid', -1))
    except ValueError:
        abort(404)
    else:
        product = controllers.getProductById(pid)
        catalogues = controllers.getCatalogueList()
        cur_catalogue = {}
        cur_catalogue['item'] = {}
        keywords = ''
        if(product != None):
            data = controllers.getCurCatalogue(product.catalogueitem.catalogue.id, product.catalogueitem.id)
            cur_catalogue['id'] = data['catalogue_id']
            cur_catalogue['name'] = data['catalogue_name']
            cur_catalogue['item']['id'] = data['item_id']
            cur_catalogue['item']['name'] = data['item_name']
            keywords = product.keywords
        else:
            cur_catalogue = {'id': -1, 'name': '', 'item': {'id': -1, 'name': ''}}
    actives = getItemActives(4)
    return render_template('productDetails.html', keywords=keywords, item_actives = actives, catalogues = catalogues, cur_catalogue = cur_catalogue, product = product)


@app.route('/case_details', methods=['GET'])
def do_case_details_page():
    try:
         cid = int(request.args.get('cid', -1))
    except ValueError:
        abort(404)
    else:
        keywords = ''
        case = controllers.getCaseById(cid)
        catalogues = controllers.getCatalogueList()
        if(case != None):
            keywords = case.keywords
    actives = getItemActives(5)
    return render_template('caseDetails.html', keywords= keywords, catalogues = catalogues, item_actives = actives, case = case)



@app.route('/news_details', methods=['GET'])
def do_news_details_page():
    try:
         nid = int(request.args.get('nid', -1))
    except ValueError:
        abort(404)
    else:
        keywords = ''
        news = controllers.getNewsById(nid)
        catalogues = controllers.getCatalogueList()
        if(news != None):
            keywords = news.keywords
    actives = getItemActives(3)
    return render_template('newsDetails.html', keywords = keywords, catalogues = catalogues, item_actives = actives, news = news)




