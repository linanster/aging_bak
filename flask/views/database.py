from flask import Blueprint, request, render_template, flash, redirect, url_for

from models import query_aging_all_from_view
from models import db, tb_device_type, tb_factory, tb_data_aging

blue_database = Blueprint('blue_database', __name__)

# 1. view functions definition

@blue_database.route('/info_aging/', methods=['GET'])
def info_aging():
    # results = query_aging_all()
    results = query_aging_all_from_view()
    return render_template('db_query_aging.html', results=results)
@blue_database.route('/info_device/', methods=['GET'])
def info_device():
    results = query_device_all()
    return render_template('db_query_device.html', results=results)
@blue_database.route('/info_factory/', methods=['GET'])
def info_factory():
    results = query_factory_all()
    return render_template('db_query_factory.html', results=results)

@blue_database.route('/db_create/', methods=['GET', 'POST'])
def db_create():
    create_tables()
    flash('Database Initialized!')
    return redirect(url_for('blue_index.index'))

@blue_database.route('/db_delete/', methods=['GET', 'POST'])
def db_delete():
    delete_tables()
    flash('Database deleted!')
    return redirect(url_for('blue_index.index'))
  
@blue_database.route('/db_gen_testdata/', methods=['GET', 'POST'])
def db_gen_testdata():
    gen_testdata()
    flash('Test data insert!')
    return redirect(url_for('blue_index.index'))



# 2. database CRUD functions

def create_tables():
    db.create_all()

def delete_tables():
    db.drop_all()


def query_aging_all():
    return tb_data_aging.query.all()

def query_device_all():
    return tb_device_type.query.all()

def query_factory_all():
    return tb_factory.query.all()

def gen_testdata():
    d1 = tb_device_type(1, 'C-Life', 'Gen1/Gen2 ST C-Life(Ox01)')
    d2 = tb_device_type(17, 'C-Life', 'Gen2 Andromeda C-Life(0x11)')
    d3 = tb_device_type(18, 'C-Life', 'Gen2 MFG C-Life(0x12)')
    d4 = tb_device_type(5, 'C-Sleep', 'Gen1/Gen2 ST C-Sleep(0x05)')
    d5 = tb_device_type(19, 'C-Sleep', 'Gen2 MFG C-Sleep(0x13)')
    f1 = tb_factory(1, 'Leedarson', '立达信')
    f2 = tb_factory(2, 'Innotech', 'Smart LED Light Bulbs')
    f3 = tb_factory(3, 'Tonly', '通力')
    a1 = tb_data_aging(5, 2, '3.1', -65, -33, 'd74d38dabcf1', '88:50:F6:04:62:31', True, False)
    a2 = tb_data_aging(1, 3, '3.2', -65, -33, 'd74d38dabcf5', '88:50:F6:04:62:35', True, False)
    a3 = tb_data_aging(17, 1, '3.40', -65, -33, 'd74d38dabcf7', '88:50:F6:04:62:37', True, False)

    datas = [d1, d2, d3, d4, d5, f1, f2, f3]
    for data in datas:
        db.session.add(data)
    db.session.commit()
    datas = [a1, a2, a3]
    for data in datas:
        db.session.add(data)
    db.session.commit()

