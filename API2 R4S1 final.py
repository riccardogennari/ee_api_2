import json
import csv
import requests
from datetime import datetime

# ---- GESTIONE DATE E ORE PER INFORMAZIONI AGGIUNTIVE
now = datetime.now()  # current date and time
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
ora = now.strftime("%H_%M_%S")
ora_log = now.strftime("%H:%M:%S")
data_ora_estrazione = year + month + day + "_" + ora
data_estrazione = day + chr(34) + month + chr(34) + day


# --------------- CREA UNA PATH PYTHON
def converti_path_python(path):
    path_python = path.replace(chr(92), chr(92) + chr(92)) + chr(92) + chr(92)
    return path_python


# --------------- RIFERIMENTI CARTELLE E FILE
path_windows = r"C:\Users\ig01849\Miei progetti\EE SYSTEM TEST\API2 - R4S1"
path_lavoro = converti_path_python(path_windows)
######################################

# --------------- CREA LA STRINGA DA SCRIVERE NEL CSV
def crea_stringa_csv(lista):
    lunghezza_lista = len(lista)
    contenuto = ""
    for n in range(0,lunghezza_lista):
        if n < lunghezza_lista-1:
            #contenuto = contenuto + str(lista[n]) + ";"
            #contenuto = contenuto + chr(39) + str(lista[n]) + chr(39) + ";"
            contenuto = contenuto + chr(34) + str(lista[n]) + chr(34) + ";"
        else:
            #contenuto = contenuto + str(lista[n])
            #contenuto = contenuto + chr(39) + str(lista[n]) + chr(39)
            contenuto = contenuto + chr(34) + str(lista[n]) + chr(34)
    return contenuto
######################################


# CREA LA URL DA RICHIAMARE SULLA BASE DEI VALORI IN LISTA
def crea_url_da_richiamare(lista_elementi_url):
    divisore = "&"
    url_da_richiamare = lista_elementi_url[0]
    for n in range(1, len(lista_elementi_url)):
        elemento_url = lista_elementi_url[n]
        if n < (len(lista_elementi_url) - 1):
            url_da_richiamare = url_da_richiamare + elemento_url[0] + "=" + elemento_url[1] + divisore
        else:
            url_da_richiamare = url_da_richiamare + elemento_url[0] + "=" + elemento_url[1]
    return url_da_richiamare
######################################

field = input("keyword o code?: ")
value = input("Inserisci il valore - una parola se hai scelto KEYWORD o un codice se hai scelto CODE: ")
language = input("Lingua - codice ISO due digit IT o EN: ")


# ---- VARIABILI PER LA GESTIONE DEI FILE API2Q2
nome_file_api2query1 = data_ora_estrazione + " -- API2Q1_" + field + "-" + value + "-" + language + ".csv"


# ---- VARIABILI PER LA GESTIONE DEI FILE API2Q2
nome_file_api2query2 = data_ora_estrazione + " -- API2Q2.csv"


lista_parametri_url_code_api2q1 = [
    'https://intesa.uat01.eesa.run/api/trade-codes?',
    ['classification', ''],
    ['field', field],
    ['value', value],
    ['strict', 'true'],
    ['language', language],
    ['limit', ''],
    ['offset', '']
]

intestazioni_file_risultati_api2q1 = ["ORA ESTRAZIONE",
                                      "DATA ESTRAZIONE",
                                      "CLASSIFICATION",
                                      "LEVEL",
                                      "MAX_LEVEL",
                                      "CODE",
                                      "PARENT_CODE",
                                      "GROUP",
                                      "PATH",
                                      "DESCRIPTION",
                                      "ULR",
                                      "RESPONSE CODE"]

intestazioni_file_risultati_api2q2 = ["ORA ESTRAZIONE",
                                      "DATA ESTRAZIONE",
                                      "CODE_API2Q1",
                                      "CLASSIFICATION",
                                      "LEVEL",
                                      "MAX_LEVEL",
                                      "CODE",
                                      "PARENT_CODE",
                                      "GROUP",
                                      "PATH",
                                      "DESCRIPTION"]
# CREO LA UTL DI API2Q1
urlcompleted_api1query1 = crea_url_da_richiamare(lista_parametri_url_code_api2q1)

print("+++++ INIZIO L'ELABORAZIONE +++++")
print(" V--- copiare da qui in caso di defect ---V")
print("*** PARAMETRI INSERITI PER LA CHIAMATA A API2Q1:")
print("Keyword o code: " + field)
print("Valore: " +  value)
print("Lingua: " + language)
print("URL COMPLETA DI API2Q2: " + urlcompleted_api1query1)
print("PROCEDO CON LA CHIAMATA")


# ---- CHIAMATA A API2Q1 DI EE
payload = {}
headers = {
    'Authorization': 'Basic aW50ZXNhOjdqb0x2RFd5a21tTWR3NUc='
}

response_api2q1 = requests.request("GET", urlcompleted_api1query1, headers=headers, data=payload)

# ----- RESPONSE CODE ----
response_code_api2q1_str = str(response_api2q1.status_code)
response_code_api2q1 = response_api2q1.status_code

if response_code_api2q1 != 200:
    print("QUALCOSA E' ANDATO STORTO!!!!")
    print("LA RESPONSE E':\n")
    print(response_code_api2q1_str)
else:
    print("IL CODE RESPONSE E': " + response_code_api2q1_str)
    print("Creo il file:" + nome_file_api2query1)
    # ---- APRO IL DOCUMENTO PER LA REGISTRAZIONE DELLE INFORMAZIONI DI API2Q1
    oggetto_file_risultati_api2q1 = open(path_lavoro + nome_file_api2query1, "a", encoding='utf-8')
    # ---- APRO IL DOCUMENTO PER LA REGISTRAZIONE DELLE INFORMAZIONI DI API2Q2
    oggetto_file_risultati_api2q2 = open(path_lavoro + nome_file_api2query2, "a", encoding='utf-8')
    # ---- STAMPO NEL FILE DI RISULTATI DI API2Q1 LE INTESTAZIONI DI COLONNA
    oggetto_file_risultati_api2q1.write(crea_stringa_csv(intestazioni_file_risultati_api2q1)+"\n")
    # ---- STAMPO NEL FILE DI RISULTATI DI API2Q2 LE INTESTAZIONI DI COLONNA
    oggetto_file_risultati_api2q2.write(crea_stringa_csv(intestazioni_file_risultati_api2q2) + "\n")

    data_estrazione = day + chr(47) + month + chr(47) + day
    ora_log = now.strftime("%H:%M:%S")
    lista_orario_api2q1 = [ora_log, data_estrazione]
    #oggetto_file_risultati_api2q1.write(crea_stringa_csv(lista_orario))
    #oggetto_file_risultati_api2q1.close()
    data_api2q1 = json.loads(response_api2q1.text)
    print("Gli item restituiti da API2Q1 sono: "+str(data_api2q1["totalItems"]))
    # ---- ESTRAGGO LA LISTA CHE CONTIENE I DIZIONARI CON I DATI DAI VARI ITEMS
    items_api2q1 = data_api2q1["items"]
    dict_data_api2q1 = {}
    i = 0
    for n in items_api2q1:
        i = i + 1
        dict_data_api2q1 = n
        classification_api2q1 = str(dict_data_api2q1["classification"])
        level_api2q1 = str(dict_data_api2q1["level"])
        max_level_api2q1 = str(dict_data_api2q1["max_level"])
        code_api2q1 = str(dict_data_api2q1["code"])
        parent_code_api2q1 = str(dict_data_api2q1["parent_code"])
        group_api2q1 = str(dict_data_api2q1["group"])
        path_api2q1 = str(dict_data_api2q1["path"])
        description_api2q1 = str(dict_data_api2q1["description"])
        elementi_risposta_api2q1 = [classification_api2q1, level_api2q1, max_level_api2q1, code_api2q1, parent_code_api2q1, group_api2q1, path_api2q1, description_api2q1]
        code_api2q2 = code_api2q1
        dict_data_api2q2 = n
        lista_parametri_url_code_api2q2 = [
            'https://intesa.uat01.eesa.run/api/trade-codes/hierarchy?',
            ['classification', 'HS17A'],
            ['codeValue', code_api2q1],
            ['language', language],
            ['limit', '10000']
        ]
        urlcompleted_api2query2 = crea_url_da_richiamare(lista_parametri_url_code_api2q2)
        print("Elaboro l'item " + str(i) + " di " + str(data_api2q1["totalItems"])+" ITEM:" + code_api2q2+" URL API2Q2: " + urlcompleted_api2query2)
        #print("ITEM:" + code_api2q2+"URL API2Q2: " + urlcompleted_api2query2)
        #print("URL API2Q2: " + urlcompleted_api2query2)
        # ---- CHIAMATA A API2Q2 DI EE
        payload = {}
        headers = {
            'Authorization': 'Basic aW50ZXNhOjdqb0x2RFd5a21tTWR3NUc='
        }
        ora_log = now.strftime("%H:%M:%S")
        lista_orario_api2q2 = [ora_log, data_estrazione]
        response_api2q2 = requests.request("GET", urlcompleted_api2query2, headers=headers, data=payload)
        response_code_api2q2_str = str(response_api2q2.status_code)
        response_code_api2q2 = response_api2q2.status_code
        da_stampare_api2q1 = lista_orario_api2q1 + elementi_risposta_api2q1 + [urlcompleted_api2query2] + [response_code_api2q2]
        oggetto_file_risultati_api2q1.write(crea_stringa_csv(da_stampare_api2q1) + "\n")

        if response_code_api2q2 != 200:
            print("La chiamata a API2Q2 è andata maluccio..")
            print("Response code: " + response_code_api2q2_str)
            print("Response: " + response_code_api2q2_str)
            contenuto_api2q1 = lista_orario_api2q1 + elementi_risposta_api2q1 + [response_code_api2q2,response_code_api2q2_str]
            oggetto_file_risultati_api2q1.write(crea_stringa_csv(contenuto_api2q1))

        else:

            dict_data_api2q2 = {}
            data_api2q2 = json.loads(response_api2q2.text)
            items_api2q2 = data_api2q2["items"]
            dict_data_api2q2 = {}
            for m in items_api2q2:
                dict_data_api2q2 = m


                classification_api2q2 = str(dict_data_api2q2["classification"])
                level_api2q2 = str(dict_data_api2q2["level"])
                max_level_api2q2 = str(dict_data_api2q2["max_level"])
                code_api2q2 = str(dict_data_api2q2["code"])
                parent_code_api2q2 = str(dict_data_api2q2["parent_code"])
                group_api2q2 = str(dict_data_api2q2["group"])
                path_api2q2 = str(dict_data_api2q2["path"])
                description_api2q2 = str(dict_data_api2q2["description"])
                elementi_risposta_api2q2 = [classification_api2q2, level_api2q2, max_level_api2q2, code_api2q2, parent_code_api2q2, group_api2q2, path_api2q2, description_api2q2]
                elementi_api2q2_x_risp_api2q1 = [response_code_api2q2, items_api2q1, urlcompleted_api2query2]
                #da_stampare_api2q1 = lista_orario_api2q1 + elementi_risposta_api2q1 + [urlcompleted_api2query2] + [response_code_api2q2]
                #oggetto_file_risultati_api2q1.write(crea_stringa_csv(da_stampare_api2q1) + "\n")
                da_stampare_api2q2 = lista_orario_api2q2 + [code_api2q1] + elementi_risposta_api2q2
                oggetto_file_risultati_api2q2.write(crea_stringa_csv(da_stampare_api2q2) + "\n")

    oggetto_file_risultati_api2q1.close()
    oggetto_file_risultati_api2q2.close()

    print("#### FAI RIFERIMENTO AI FILE:\n")
    print("Scarico della chiamata ad API2Q1 - ELENCO degli item individuati: "+nome_file_api2query1)
    print("Scarico della chiamata ad API2Q2 - STRUTTURA degli item individuati: "+nome_file_api2query2)
    print("""
    
    ______ _____ _   _ _____ _____ _____ _ _ _
    |  ___|_   _| \ | |_   _|_   _|  _  | | | |
    | |_    | | |  \| | | |   | | | | | | | | |
    |  _|   | | | . ` | | |   | | | | | | | | |
    | |    _| |_| |\  |_| |_  | | \ \_/ /_|_|_|
    \_|    \___/\_| \_/\___/  \_/  \___/(_|_|_)
    #
    #
    #
    """)
    print("""
    TUTTAPPPPOOOOOO....
    
    SALUTAMI I FRANCESI:
    
         _
       _| |
     _| | |
    | | | |
    | | | | __
    | | | |/  |
    |       /\ |
    |      /  \/
    |      \  /|
    |       \/ /
     \        /
      |     /
      |    |
    
    """)
            # file_risultati_api2q2_nocode.write(
#     intestazioni_file_risultati_api2q2_nocode + "\n")  # stampo la stringa + a capo nel file
#
# # ---- ELABORAZIONE RISULTATO
# if response_code != 200:
#     # ---- CHIAMATA NEGATIVA
#     print("IL CODICE E' UN ERRORE: NON E' POSSIBILE SCARICARE LA STRUTTURA")
#     nd = "N.D."
#     file_risultati_api2q2_nocode_contenuto_no200 = ora_log + ";" + data_estrazione + ";" + nd + ";" + nd + ";" + nd + ";" + nd + ";" + nd + ";" + nd + ";" + nd + ";" + nd + ";" + urlcompleted_api1query2 + ";" + response_code_str
#     file_risultati_api2q2_nocode.write(file_risultati_api2q2_nocode_contenuto_no200)
#     file_risultati_api2q2_nocode.close()
#     #     print("""
#     #
#     #  _____  ____  ____   ____  ______   ____  __  __  __      ___ ___   ____        ___ __       ____  ____   ___     ____  ______   ____      ___ ___   ____  _        ___  __
#     # |     ||    ||    \ |    ||      | /    ||  ||  ||  |    |   |   | /    |      /  _]  |     /    ||    \ |   \   /    ||      | /    |    |   |   | /    || |      /  _]|  |
#     # |   __| |  | |  _  | |  | |      ||  o  ||  ||  ||  |    | _   _ ||  o  |     /  [_|_ |    |  o  ||  _  ||    \ |  o  ||      ||  o  |    | _   _ ||  o  || |     /  [_ |  |
#     # |  |_   |  | |  |  | |  | |_|  |_||     ||__||__||__|    |  \_/  ||     |    |    _] \|    |     ||  |  ||  D  ||     ||_|  |_||     |    |  \_/  ||     || |___ |    _]|__|
#     # |   _]  |  | |  |  | |  |   |  |  |  _  | __  __  __     |   |   ||  _  |    |   [_        |  _  ||  |  ||     ||  _  |  |  |  |  _  |    |   |   ||  _  ||     ||   [_  __
#     # |  |    |  | |  |  | |  |   |  |  |  |  ||  ||  ||  |    |   |   ||  |  |    |     |       |  |  ||  |  ||     ||  |  |  |  |  |  |  |    |   |   ||  |  ||     ||     ||  |
#     # |__|   |____||__|__||____|  |__|  |__|__||__||__||__|    |___|___||__|__|    |_____|       |__|__||__|__||_____||__|__|  |__|  |__|__|    |___|___||__|__||_____||_____||__|
#     #
#     #
#     #     """)
#     print("""
#     Quindi l'API2Q2 ti fa un bel....
#
#      _            _   _
#     | |          | | | |
#   __| | ___  __ _| |_| |__
#  / _` |/ _ \/ _` | __| '_ \
# | (_| |  __/ (_| | |_| | | |
#  \__,_|\___|\__,_|\__|_| |_|
#
#     """)
# else:
#     data_api2q2_nocode = json.loads(response.text)
#     print("STAMPO IL JSON DESERIALIZZATO:\n")
#     print(data_api2q2_nocode)
#     totalItems = str(data_api2q2_nocode["totalItems"])
#     print("IL NUMERO TOTALE DI ITEMS E': " + totalItems)
#     # ---- ESTRAGGO LA LISTA CHE CONTIENE I DIZIONARI CON I DATI DAI VARI ITEMS
#     items = data_api2q2_nocode["items"]
#     dict_data_api2q2_nocode = {}
#     for n in items:
#         dict_data_api2q2_nocode = n
#         classification = str(dict_data_api2q2_nocode["classification"])
#         level = str(dict_data_api2q2_nocode["level"])
#         max_level = str(dict_data_api2q2_nocode["max_level"])
#         code = str(dict_data_api2q2_nocode["code"])
#         parent_code = str(dict_data_api2q2_nocode["parent_code"])
#         group = str(dict_data_api2q2_nocode["group"])
#         path = str(dict_data_api2q2_nocode["path"])
#         description = str(dict_data_api2q2_nocode["description"])
#         file_risultati_api2q2_nocode_contenuto_200 = ora_log + ";" + data_estrazione + ";" + classification + ";" + level + ";" + max_level + ";" + code + ";" + parent_code + ";" + group + ";" + path + ";" + chr(
#             34) + description + chr(34) + ";" + urlcompleted_api1query2 + ";" + response_code_str
#         file_risultati_api2q2_nocode.write(
#             file_risultati_api2q2_nocode_contenuto_200 + "\n")  # stampo la stringa + a capo nel file
#
# file_risultati_api2q2_nocode.close()
#
# print("""
#
# ______ _____ _   _ _____ _____ _____ _ _ _
# |  ___|_   _| \ | |_   _|_   _|  _  | | | |
# | |_    | | |  \| | | |   | | | | | | | | |
# |  _|   | | | . ` | | |   | | | | | | | | |
# | |    _| |_| |\  |_| |_  | | \ \_/ /_|_|_|
# \_|    \___/\_| \_/\___/  \_/  \___/(_|_|_)
#
#
#
# """)
#
# print("""
# TUTTAPPPPOOOOOO....
#
# SALUTAMI I FRANCESI:
#
#      _
#    _| |
#  _| | |
# | | | |
# | | | | __
# | | | |/  |
# |       /\ |
# |      /  \/
# |      \  /|
# |       \/ /
#  \        /
#   |     /
#   |    |
#
#
# """)