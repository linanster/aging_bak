from flask import Blueprint, request, render_template, flash, redirect, url_for
from app.models import view_data_aging, tb_data_aging
from flask_paginate import Pagination, get_page_parameter


blue_nav = Blueprint('blue_nav', __name__)


@blue_nav.route('/')
@blue_nav.route('/index/')
def index():
    return render_template('index.html')


@blue_nav.route('/about/')
def about():
    return render_template('about.html')

@blue_nav.route('/testing/')
def testing():
    # results = tb_data_aging.query.all()
    results = view_data_aging.query.all()
    control_index = request.args.get('control_index')
    print("==control_index==", control_index)
    print("==type(control_index)==", type(control_index))
    
    # pagination code
    # PER_PAGE = 30
    # page = request.args.get(get_page_parameter(), type=int, default=1) #获取页码，默认为第一页
    # start = (page-1)*PER_PAGE
    # end = page * PER_PAGE if len(results) > page * PER_PAGE else len(results)
    # pagination = Pagination(page=page, total=len(results), per_page=PER_PAGE, bs_version=3)
    # ret = view_data_aging.query.slice(start, end)
    # return render_template('testing.html', pagination=pagination, results=ret)
    return render_template('testing.html', results=results, control_index=control_index)
