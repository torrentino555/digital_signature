# -*- coding: utf-8 -*-
from lxml import etree
import uno

def get_document(filename):
    local = uno.getComponentContext()
    resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
    context = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
    desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
    document = desktop.loadComponentFromURL(uno.systemPathToFileUrl(filename), "_blank", 0, tuple())
    return document

def xml_file(Person, primary_key, path='/home/olof/Projects/base_model/base_model/templates/documents/skeleton_iit.xml', type='FizLico', isBoss=False):
    tree = etree.parse(path)
    node = tree.xpath('/regform/abonent/organization/certificateowner')[0]
    node[0].text = Person.Surname
    node[1].text = Person.Firstname
    node[2].text = Person.GivenName
    node[3].text = Person.Country
    node[4].text = Person.email

    node = tree.xpath('/regform/abonent/organization/issued')[0]
    if isBoss:
        node.attrib['IsBoss'] = "true"
    else:
        node.attrib['IsContact'] = "true"
    file = open(u'/home/olof/Projects/base_model/base_model/uploads/xml/{}.xml'.format(primary_key), 'w')
    file.write(str(etree.tostring(tree, pretty_print=True,encoding='utf-8', xml_declaration=True), encoding='UTF-8'))
    file.close()

def in_pdf(pathIn, pathOut, isInvoice=True):
    import subprocess
    subprocess.call(['/home/olof/Projects/base_model/base_model/scripts/toPdf.sh', pathOut, pathIn])


def statement(Person, primary_key):
    input_path_file = '/home/olof/Projects/base_model/base_model/templates/documents/statement_ib.xlsx'
    destination_path_file = '/home/olof/Projects/base_model/base_model/uploads/statements/{}.xlsx'.format(primary_key)

    document = get_document(input_path_file)
    sheet = document.getSheets().getByIndex(0)
    sheet.getCellByPosition(2, 7).setString(Person.Surname)
    sheet.getCellByPosition(2, 8).setString(Person.Firstname)
    sheet.getCellByPosition(2, 9).setString(Person.GivenName)
    sheet.getCellByPosition(4, 19).setString(Person.Surname)
    sheet.getCellByPosition(4, 20).setString(Person.Firstname + " " + Person.GivenName)
    sheet.getCellByPosition(4, 21).setString(Person.Country)
    sheet.getCellByPosition(4, 22).setString(Person.State)
    sheet.getCellByPosition(4, 23).setString(Person.Locality)
    sheet.getCellByPosition(4, 24).setString(Person.StreetAddress)
    sheet.getCellByPosition(4, 27).setString(Person.email)
    sheet.getCellByPosition(4, 28).setString(Person.INN)
    sheet.getCellByPosition(4, 30).setString(Person.SNILS)
    document.storeToURL(uno.systemPathToFileUrl(destination_path_file), ())

def invoice(Person, primary_key, date):
    input_path_file = '/home/olof/Projects/base_model/base_model/templates/documents/cheque.xlsx'
    destination_path_file = '/home/olof/Projects/base_model/base_model/uploads/invoices/{}.xlsx'.format(primary_key)

    document = get_document(input_path_file)
    sheet = document.getSheets().getByIndex(0)
    sheet.getCellByPosition(1, 12).setString('Счет на оплату № ' + str(primary_key) + ' от ')
    sheet.getCellByPosition(6, 18).setString('{} {} {}, ИНН {},  {}, {}, {}'.format(
        Person.Surname, Person.Firstname, Person.GivenName, Person.INN, 'INDEX', Person.State, Person.StreetAddress))
    sheet.getCellByPosition(3, 21).setString('Выпуск Квалифицированноо сертификата (базового)')
    sheet.getCellByPosition(1, 26).setString('Всего наименований 1, на сумму 1900, 00 руб.')
    sheet.getCellByPosition(1, 27).setString('Одна тысяча девятьсот рублей 00 копеек')
    document.storeToURL(uno.systemPathToFileUrl(destination_path_file), ())
