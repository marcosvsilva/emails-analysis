from simplegmail.message import Message
from unicodedata import name

from api.gmail_api import (SubjectEmail, get_emails)


def process_history_emails(subject: SubjectEmail):
    messages = get_emails(subject)
    informations = [extract_informations(mess, subject) for mess in messages]

    return messages, informations

def extract_informations(mes: Message, subject: SubjectEmail):
    id_email = mes.id
    text = mes.html

    if not "Razão Social" in text:
        raise Exception(
            "Email of %s doesn't information to extract!" % subject.system)

    text_split = text.split('\n')

    line_nfe_number=2
    line_nfe_serie=3
    line_nfe_key=4
    line_nfe_date=5
    line_nfe_social=6
    line_nfe_name=7
    line_nfe_id=8
    line_nfe_adress_st=9
    line_nfe_adress_n=10
    line_nfe_city=11

    nfe_model = text_split[line_nfe_key]
    nfe_model = nfe_model[nfe_model.find(': ')-5:nfe_model.find(': ')]
    if 'NF-E' in nfe_model.upper() or 'NFE' in nfe_model.upper():
        nfe_model = 'NF-e'
    elif 'NFC-E' in nfe_model.upper() or 'NFCE' in nfe_model.upper():
        nfe_model = 'NFC-e'
    elif 'CT-E' in nfe_model.upper() or 'CTE' in nfe_model.upper():
        nfe_model = 'CT-e'
    elif 'NFS-E' in nfe_model.upper() or 'NFSE' in nfe_model.upper():
        nfe_model = 'NFS-e'
    elif 'MDF-E' in nfe_model.upper() or 'MDFE' in nfe_model.upper():
        nfe_model = 'MDF-e'
    else:
        nfe_model = '-'

    nfe_number = text_split[line_nfe_number]
    nfe_number = nfe_number[nfe_number.find(': ')+2:len(nfe_number)]

    nfe_serie = text_split[line_nfe_serie]
    nfe_serie = nfe_serie[nfe_serie.find(': ')+2:len(nfe_serie)]

    nfe_date = text_split[line_nfe_date]
    nfe_date = nfe_date[nfe_date.find(': ')+2:len(nfe_date)]
    nfe_date = nfe_date.replace(' ', '')
    date_parts = nfe_date.split('/')

    if len(date_parts) != 3:
        raise Exception('Date is correct invalid!')

    date, month, year = date_parts
    if len(date) < 2:
        date = '0{}'.format(date)
    if len(month) < 2:
        month = '0{}'.format(month)
    if len(year) < 4:
        if int(year) > 70:
            year = '19{}'.format(year)
        else:
            year = '20{}'.format(year)

    if int(month) >= 12:
        if int(date) <= 12:
            aux = month
            month = date
            date = aux
        else:
            month = 12

    if int(date) > 31:
        date = 30

    nfe_date = '{}/{}/{}'.format(date, month, year)

    nfe_social = text_split[line_nfe_social]
    nfe_social = nfe_social[nfe_social.find(': ')+2:len(nfe_social)]
    nfe_social = nfe_social[0:60]

    nfe_name = text_split[line_nfe_name]
    nfe_name = nfe_name[nfe_name.find(': ')+2:len(nfe_name)]
    nfe_name = nfe_name[0:60]

    nfe_id = text_split[line_nfe_id]
    nfe_id = nfe_id[nfe_id.find(': ')+2:len(nfe_id)]
    nfe_id = nfe_id[0:14]

    nfe_adress_st = text_split[line_nfe_adress_st]
    nfe_adress_st = nfe_adress_st[nfe_adress_st.find(': ')+2:len(nfe_adress_st)]
    nfe_adress_st = nfe_adress_st[0:200]

    nfe_adress_n = text_split[line_nfe_adress_n]
    nfe_adress_n = nfe_adress_n[nfe_adress_n.find(': ')+2:len(nfe_adress_n)]
    nfe_adress_n = nfe_adress_n[0:60]

    nfe_city = text_split[line_nfe_city]
    nfe_city = nfe_city[nfe_city.find(': ')+2:len(nfe_city)]
    if nfe_city.find('<') > 0:
        nfe_city = nfe_city[0:nfe_city.find('<')]
    nfe_city = nfe_city[0:60]

    return {"id": id_email,
            "description": {
                "EMDF_SISTEMA": subject.system,
                "EMDF_MODELO": clear_information(nfe_model),
                "EMDF_DATA_EMISSAO": clear_information(nfe_date),
                "EMDF_NUMERO": int(nfe_number),
                "EMDF_SERIE": clear_information(nfe_serie),
                "EMDF_CNPJ": clear_information(nfe_id),
                "EMDF_RAZAO_SOCIAL": clear_information(nfe_social),
                "EMDF_FANTASIA": clear_information(nfe_name),
                "EMDF_ENDERECO": clear_information(nfe_adress_st),
                "EMDF_BAIRRO": clear_information(nfe_adress_n),
                "EMDF_MUNICIPIO": clear_information(nfe_city)}}

def clear_information(information: str) -> str:
    information = information.replace('\r\n', '')
    information = information.replace('\r', '')
    information = information.replace('\n', '')
    return information
