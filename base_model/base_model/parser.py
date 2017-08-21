# -*- coding: utf-8 -*-
from lxml import etree
import uno
import sys
sys.path.append("..")
from scripts_settings import global_path

def get_document(filename):
    local = uno.getComponentContext()
    resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
    context = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
    desktop = context.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", context)
    document = desktop.loadComponentFromURL(uno.systemPathToFileUrl(filename), "_blank", 0, tuple())
    return document

def xml_file(Person, Order, primary_key, path=global_path + 'templates/documents/skeleton_iit.xml', type='FizLico', isBoss=False):
    tree = etree.parse(path)
    # Установка base = true (Базовый сертификат)
    node_ugis = tree.xpath('/regform/abonent/general/UGIS')[0]
    node_ugis[0].text = 'true'
    # Установка параметров заказа, таких как помощь и токен, а так же установка формата КриптоПро
    node_dopuslugi = tree.xpath('/regform/abonent/general/DopUslugi')[0]
    if Order.Token:
        node_dopuslugi[1].text = 'true'
    if Order.Help:
        node_dopuslugi[2].text = 'true'
    node_dopuslugi[5].text = 'true' # КриптоПро
    # Установка параметров организации
    node_org = tree.xpath('/regform/abonent/organization')[0]
    node_org[0].text = 'FizLico'
    node_org[3].text = Person.INN
    # Установка руководителя организации
    node_certowner = tree.xpath('/regform/abonent/organization/certificateowner')[0]
    node_certowner[0].text = 'Surname' # Фамилия
    node_certowner[1].text = 'Валерий'
    node_certowner[2].text = 'Александрович'
    node_certowner[3].text = 'Должность' # Должность
    node_certowner[4].text = 'email' # Email
    node_certowner[5].text = 'Устава'
    # Установка контактного лица
    node_contact = tree.xpath('/regform/abonent/organization/contact')[0]
    node_contact[0].text = Person.Surname
    node_contact[1].text = Person.Firstname
    node_contact[2].text = Person.GivenName
    node_contact[3].text = 'Должность' # Если физ. лицо??
    node_contact[4].text = Person.email
    node_contact[5].text = 'Phone' # Нет телефона
    # Установка issued
    node_issued = tree.xpath('/regform/abonent/organization/issued')[0]
    node_issued.attrib['IsBoss'] = "true"
    node_issued.attrib['IsContact'] = "true"
    node_issued[0].text = Person.Surname
    node_issued[1].text = Person.Firstname
    node_issued[2].text = Person.GivenName
    node_issued[3].text = 'Должность' # Если физ. лицо?
    node_issued[4].text = Person.email
    node_issued[5].text = 'Phone' # Нет телефона
    node_issued[7].text = Person.SNILS
    # Установка addressCr
    node_addr = tree.xpath('/regform/abonent/organization/addressCR')[0]
    node_addr[0].text = 'INDEX' # Нет индекса
    node_addr[1].text = Person.Locality
    node_addr[2].text = Person.State
    node_addr[3].text = '' # Нет дистрикта
    node_addr[4].text = Person.StreetAddress
    # Запись результата в файл
    file = open(global_path + 'uploads/xml/{}.xml'.format(primary_key), 'w')
    file.write(str(etree.tostring(tree, pretty_print=True,encoding='utf-8', xml_declaration=True), encoding='UTF-8'))
    file.close()

def in_pdf(pathIn, pathOut, isInvoice=True):
    import subprocess
    subprocess.call([global_path + 'scripts/toPdf.sh', pathOut, pathIn])


def statement(Person, primary_key):
    input_path_file = global_path + 'templates/documents/statement_ib.xlsx'
    destination_path_file = global_path + 'uploads/statements/{}.xlsx'.format(primary_key)

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
    input_path_file = global_path + 'templates/documents/cheque.xlsx'
    destination_path_file = global_path + 'uploads/invoices/{}.xlsx'.format(primary_key)

    document = get_document(input_path_file)
    sheet = document.getSheets().getByIndex(0)
    sheet.getCellByPosition(1, 12).setString('Счет на оплату № ' + str(primary_key) + ' от ')
    sheet.getCellByPosition(6, 18).setString('{} {} {}, ИНН {},  {}, {}, {}'.format(
        Person.Surname, Person.Firstname, Person.GivenName, Person.INN, 'INDEX', Person.State, Person.StreetAddress))
    sheet.getCellByPosition(3, 21).setString('Выпуск Квалифицированноо сертификата (базового)')
    sheet.getCellByPosition(1, 26).setString('Всего наименований 1, на сумму 1900, 00 руб.')
    sheet.getCellByPosition(1, 27).setString('Одна тысяча девятьсот рублей 00 копеек')
    document.storeToURL(uno.systemPathToFileUrl(destination_path_file), ())
