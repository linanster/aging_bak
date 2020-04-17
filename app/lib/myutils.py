import xlwt
import os
import datetime

from app.models import db, Testdata, TestdataArchive
# from app.myglobal import topdir


def gen_excel(tableclass, filename):
    # 1.prepare table heads
    # heads_raw = db.metadata.tables.get('testdatas').c
    tablename = tableclass.__tablename__
    heads_raw = db.metadata.tables.get(tablename).c
    heads = list()
    for item in heads_raw:
        # heads.append(str(item).replace('testdatas.','',1))
        heads.append(str(item).replace(tablename+'.','',1))
    # 2.prepare table data
    # datas = Testdata.query.all()
    datas = tableclass.query.all()
    # 3.prepare excel object
    book = xlwt.Workbook()
    sheet1 = book.add_sheet('sheet1')
    # todo
    # dateFormat = xlwt.XFStyle()
    # dateFormat.num_format_str = '%y-%m-%d %h:%m:%s'
    # dateFormat.num_format_str = 'yyyy/mm/dd'
    # 4. insert table head row
    for col,field in enumerate(heads):
        sheet1.write(0, col, field)
    # 5.insert data rows
    row = 1
    for data in datas:
        col = 0
        while col < len(heads):
            cell = data.__dict__.get(heads[col])
            if heads[col] == 'datetime':
                cell = cell.strftime('%Y-%m-%d %H:%M:%S')
            sheet1.write(row, col, cell)
            col += 1
        row += 1
    # 6.save
    # timestamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    # filename = 'testdatas-' + timestamp + '.xls'
    # filename = os.path.join(topdir, 'updownload', filename)
    book.save(filename)


# please be very careful to call this function
def empty_folder(folder):
    files = os.listdir(folder)
    for file in files:
        if file == '.gitkeep':
            continue
        file = os.path.join(folder, file)
        # todo
        # if file type is folder, here will raise IsADirectoryError
        os.remove(file)
