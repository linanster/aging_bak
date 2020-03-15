from flask import Blueprint, request, render_template, flash, redirect, url_for
import datetime

from app.models import db, db_stage, db_archive, tb_device_type, tb_factory, tb_data_aging
from app.models import view, view_data_aging

# create_view and delete_view is actually two pymysql execute function
# not that like typical models, such as db
from app.lib import create_view, delete_view

blue_database = Blueprint('blue_database', __name__)

# 1. view functions definition

@blue_database.route('/info_aging/', methods=['GET'])
def info_aging():
    # results = tb_data_aging.query.all()
    results = view_data_aging.query.all()
    refresh = request.args.get('refresh')
    # print('==refresh==:', refresh)
    if refresh:
        return render_template('db_query_aging.html', results=results, refresh=True)
    return render_template('db_query_aging.html', results=results)


@blue_database.route('/info_device/', methods=['GET'])
def info_device():
    results = tb_device_type.query.all()
    return render_template('db_query_device.html', results=results)

@blue_database.route('/info_factory/', methods=['GET'])
def info_factory():
    results = tb_factory.query.all()
    return render_template('db_query_factory.html', results=results)

@blue_database.route('/db_create/', methods=['GET', 'POST'])
def db_create():
    db.create_all()
    db_stage.create_all()
    db_archive.create_all()
    flash('Database Initialized!')
    return redirect(url_for('blue_index.index'))


@blue_database.route('/db_delete/', methods=['GET', 'POST'])
def db_delete():
    db.drop_all()
    db_stage.drop_all()
    db_archive.drop_all()
    flash('Database deleted!')
    return redirect(url_for('blue_index.index'))
  
@blue_database.route('/db_gen_testdata/', methods=['GET', 'POST'])
def db_gen_testdata():
    gen_testdata()
    flash('Test data insert!')
    return redirect(url_for('blue_index.index'))

@blue_database.route('/view_create/', methods=['GET', 'POST'])
def view_create():
    # todo: find a solution that let flask-sqlalchemy support View
    # view.create_all()
    create_view()
    flash('View Created!')
    return redirect(url_for('blue_index.index'))
@blue_database.route('/view_delete/', methods=['GET', 'POST'])
def view_delete():
    # todo: find a solution that let flask-sqlalchemy support View
    # view.drop_all()
    delete_view()
    flash('View Deleted!')
    return redirect(url_for('blue_index.index'))

# 2. database CRUD functions


def gen_testdata():
    d1 = tb_device_type(1, 'C-Life', 'Gen1/Gen2 ST C-Life(Ox01)')
    d2 = tb_device_type(17, 'C-Life', 'Gen2 Andromeda C-Life(0x11)')
    d3 = tb_device_type(18, 'C-Life', 'Gen2 MFG C-Life(0x12)')
    d4 = tb_device_type(5, 'C-Sleep', 'Gen1/Gen2 ST C-Sleep(0x05)')
    d5 = tb_device_type(19, 'C-Sleep', 'Gen2 MFG C-Sleep(0x13)')
    f1 = tb_factory(1, 'Leedarson', '立达信')
    f2 = tb_factory(2, 'Innotech', 'Smart LED Light Bulbs')
    f3 = tb_factory(3, 'Tonly', '通力')
    a1 = tb_data_aging(5, 2, '3.1', -65, -33, 'd74d38dabcf1', '88:50:F6:04:62:31', True, False, datetime.datetime.now())
    a2 = tb_data_aging(1, 3, '3.2', -65, -33, 'd74d38dabcf5', '88:50:F6:04:62:35', True, False, datetime.datetime.now())
    a3 = tb_data_aging(17, 1, '3.40', -65, -33, 'd74d38dabcf7', '88:50:F6:04:62:37', True, False, datetime.datetime.now())

    datas = [d1, d2, d3, d4, d5, f1, f2, f3]
    for data in datas:
        db.session.add(data)
    db.session.commit()
    datas = [a1, a2, a3]
    for data in datas:
        db.session.add(data)
    db.session.commit()

