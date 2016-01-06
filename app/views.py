from app import app
from flask import render_template, request, jsonify, abort
import controllers

#list size per page
PAGE_LIST_SIZE = 4

@app.route('/')
def do_home_page():
    #return 'Hello World Hopoite'
    #catalogues = controllers.getCatalogueList()
    #return render_template('home.html', catalogues = catalogues)
    return render_template('home.html')

@app.route('/service')
def do_service_page():
    catalogues = controllers.getCatalogueList()
    return render_template('service.html', catalogues = catalogues)

@app.route('/about')
def do_about_page():
    catalogues = controllers.getCatalogueList()
    return render_template('about.html', catalogues = catalogues)


@app.route('/test')
def test_page():
    return render_template('test.html')


@app.route('/add_product_page')
def add_product_page():
    return render_template('addProduct.html')


@app.route('/add_news')
def add_news_page():
    return render_template('addNews.html')


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
        page_size = int(products_size/PAGE_LIST_SIZE+1)
        if page > page_size:
            page = page_size
        elif page < 1:
            page = 1
        products = controllers.getProducts(catalogue['item']['id'], (page-1)*PAGE_LIST_SIZE, PAGE_LIST_SIZE)
        return render_template('product.html', catalogues = catalogues, cur_catalogue = catalogue, products_size = products_size,  products = products, page = page, page_size = page_size)


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
        if(product != None):
            data = controllers.getCurCatalogue(product.catalogueitem.catalogue.id, product.catalogueitem.id)
            cur_catalogue['id'] = data['catalogue_id']
            cur_catalogue['name'] = data['catalogue_name']
            cur_catalogue['item']['id'] = data['item_id']
            cur_catalogue['item']['name'] = data['item_name']
        else:
            cur_catalogue = {'id': -1, 'name': '', 'item': {'id': -1, 'name': ''}}
    return render_template('productDetails.html', catalogues = catalogues, cur_catalogue = cur_catalogue, product = product)


@app.route('/admin')
def admin():
    return render_template('boss.html')


@app.route('/catalogue_list')
def do_catalogue_list():
    print 'catalogue_list'
    data = controllers.getCatalogueList()
    return jsonify({'catalogue_list': data})


@app.route('/add_catalogue', methods=['POST'])
def do_add_catalogue():
    print 'add_catalogue'
    data = request.get_json()
    r = controllers.addCatalogue(data['catalogue_name'])
    print 'JSON: ',data
    return jsonify({'ret': r})


@app.route('/del_catalogue', methods=['POST'])
def do_del_catalogue():
    print 'del_catalogue'
    data = request.get_json()
    r = controllers.delCatalogue(data['catalogue_id'])
    print 'JSON: ',data
    return jsonify({'ret': r})


@app.route('/add_catalogue_item', methods=['POST'])
def do_add_catalogue_item():
    data = request.get_json()
    r = controllers.addCatalogueItem(data['catalogue_item_name'], data['catalogue_id'])
    return jsonify({'ret': r})


@app.route('/del_catalogue_item', methods=['POST'])
def do_del_catalogue_item():
    print 'del_catalogue_item'
    data = request.get_json()
    r = controllers.delCatalogueItem(data['catalogue_item_id'])
    print 'JSON: ',data
    return jsonify({'ret': r})


@app.route('/upload_file', methods=['POST'])
def do_upload_file():
    print 'upload_file'
    file = request.files['file']
    ret = -1
    if(file != None):
        ret = controllers.uploadImage(file)
    return jsonify({'ret': ret})


@app.route('/get_images', methods=['GET'])
def do_get_images():
    ret = controllers.getImages()
    return jsonify({'images': ret})


@app.route('/add_product', methods=['POST'])
def do_add_product():
    data = request.get_json()
    r = controllers.addProduct(data['date'], data['title'], data['keywords'], data['partno'], data['power'], data['voltage'], data['introduction'], data['description'], data['catalogue_item_id'], data['image_ids'])
    return jsonify({'ret': r})
