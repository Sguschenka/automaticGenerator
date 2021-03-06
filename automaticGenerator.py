import mimesis
from mimesis import Person
from mimesis.decorators import romanized
from mimesis.enums import Gender
from mimesis.builtins import RussiaSpecProvider as rsp
from mimesis import Transport
from mimesis import Business
from mimesis import Datetime
from mimesis import Address
import string
import mysql.connector
from mysql.connector import Error
import re
import random



##################################### Функции
# Функции, отвечаюшие за считывание таблиц и формирование списков с перечисленными названиями, столбцами и рангами
def getInfoAboutTables(): # Получение информации о таблицах
    cursor.execute("show tables from databasetest")
    res = cursor.fetchall()
    listTables = []
    for i in res:
        if i[0] == 'rang_table':
            continue
        else:
            cursor.execute("describe " + i[0])
            r1 = [i[0], cursor.fetchall()]
            listTables.append(r1)
    
    return listTables

def findRang(): # Получение информации о рангах и условиях
    cursor.execute('select * from rang_table')
    rangList = cursor.fetchall()
    return rangList

def getInfoForCopyTable(table_name, database_name):
    strExecute = 'SHOW CREATE TABLE '+database_name+'.'+table_name
    cursor.execute(strExecute)
    res = cursor.fetchall()
    return res



#Функции, отвечающие за анализ и генерацию данных

# Генератор данных. Передается массив с названием столбца и типом, а так же количество генерируемых строк
def generatorStr(columns, numbOfEl): # двумерный массив: название столбца, тип
   arrDictGenerator = []
    strNew = []
    for j in range(0, numbOfEl):
        dictGenerator = {}
        marqModel = ['', '']
        for i in range(1, len(columns)):
            if columns[i][0] == 'sex':
                if 'sex' not in dictGenerator:
                    data = generatorGender()
                    dictGenerator[i] = data
            if columns[i][0] == 'last_name':
                if 'sex' in dictGenerator:
                    gender = dictGenerator.get('sex')
                else:
                    gender = generatorGender()
                    dictGenerator['sex'] = gender
                dictGenerator['last_name'] = generatorLastName(gender)
                    
            if columns[i][0] == 'first_name':
                if 'sex' in dictGenerator:
                    gender = dictGenerator.get('sex')
                else:
                    gender = generatorGender()
                    dictGenerator['sex'] = gender
                dictGenerator['first_name'] = generatorFirstName(gender)
                
            if columns[i][0] == ('OGRN'):
                r = rsp()
                data = r.ogrn()
                dictGenerator['OGRN'] = data
            
            if columns[i][0] == 'marque' and 'model' not in dictGenerator:
                dictGenerator['marque'] = '0'
            elif columns[i][0] == 'marque' and 'model' in dictGenerator and marqModel == ['', '']:
                tr = Transport()
                carStr = tr.car()
                carArr = carStr.split(' ')
                dictGenerator['marque'] = carArr[0]
                marqModel[0] = carArr[0]
                if len(carArr) > 2:
                    strCar = ''
                    for i in range(1, len(carArr)):
                        strCar += str(i)
                    marqModel[1] = strCar
                elif len(carArr) < 2:
                    marqModel[1] = ''
                else:
                    marqModel[1] = carArr[1]
            elif columns[i][0] == 'marque' and 'model' in dictGenerator and marqModel != ['','']:
                dictGenerator['marque'] = marqModel[0]
                                
            if columns[i][0] == 'model' and 'marque' not in dictGenerator:
                dictGenerator['model'] = '0'
            elif columns[i][0] == 'model' and 'marque' in dictGenerator and marqModel == ['','']:
                tr = Transport()
                carStr = tr.car()
                carArr = carStr.split(' ')
                marqModel[0] = carArr[0]
                if len(carArr) > 2:
                    strCar = ''
                    for i in range(1, len(carArr)):
                        strCar += str(i)
                    marqModel[1] = strCar
                elif len(carArr) < 2:
                    marqModel[1] = ''
                else:
                    marqModel[1] = carArr[1]
                dictGenerator['model'] = marqModel[1]
                if dictGenerator['marque'] == '0':
                    dictGenerator['marque'] = marqModel[0]
            elif columns[i][0] == 'model' and 'marque' in dictGenerator and marqModel != ['','']:
                if dictGenerator['marque'] == '0':
                    dictGenerator['marque'] = marqModel[0]
                dictGenerator['model'] = marqModel[1]
                
            if columns[i][0] == 'name':
                comp = Business()
                dictGenerator['name'] = comp.company()
            
            if columns[i][0] == 'deal_date':
                dictGenerator['deal_date'] = generatorDate()
            
            if columns[i][0] == 'city':
                addr = Address()
                dictGenerator['city'] = addr.city()

            if columns[i][0] == 'transmission':
                dictGenerator['transmission'] = generatorTrans()
            
            if columns[i][0] == 'engine':
                dictGenerator['engine'] = generatorEngine()

            if columns[i][0] == 'color':
                dictGenerator['color'] = generatorColor()
            
            if columns[i][0] == 'VIN':
                vin = generatorVIN()
                dictGenerator['VIN'] = vin

            if columns[i][0] == 'kilometrage':
                dictGenerator[columns[i][0]] = random.randrange(5000, 150000, 5000)

            if columns[i][0] == 'salary':
                dictGenerator[columns[i][0]] = random.randrange(1000, 6000, 100)

            if columns[i][0] == 'power':
                dictGenerator[columns[i][0]] = random.randrange(130, 220, 10)

            if columns[i][0] == 'price':
                dictGenerator[columns[i][0]] = random.randrange(1300, 40000, 1000)

            if columns[i][1] == 'int' and columns[i][0] not in dictGenerator:
                dictGenerator[columns[i][0]] = 0

            if columns[i][1] == 'tinyint':
                dictGenerator[columns[i][0]] = 0
            
            if columns[i][1] == 'varchar(255)' and columns[i][0] not in dictGenerator:
                colstr = ''
                for j in (0, 12):
                    colstr += random.choice(string.ascii_letters)
                dictGenerator[columns[i][0]] = colstr
        arrDictGenerator.append(dictGenerator)
        #print(dictGenerator)        
    return arrDictGenerator

#Генераторы, выделенные в отдельные функции
def generatorEngine(): # 
    engine = ['diesel', 'petrol']
    return random.choice(engine)

def generatorColor():
    color = ['red', 'blue', 'white', 'yellow', 'black', 'green', 'orange', 'violet', 'gold', 'silver', 'gray']
    return random.choice(color)
    
def generatorTrans():
    trans = ['DSG', 'manual', 'electric drive']
    return random.choice(trans)

def generatorVIN():
    alphabet = string.ascii_letters
    arrSymb = alphabet[26:] + '12345678901234567890'
    vin = ''
    for i in range(0, 17):
        vin += random.choice(arrSymb)
    return vin

def generatorDate():
    d = Datetime()
    date = d.date(start=2000, end=2020)
    date = d.date(start=2000, end= 2020)
    formatDate = str(date.year) + '-' + str(date.month) + '-' + str(date.day)
    return formatDate

#не используется
def generatorPerson(): #содержит массив из имени, фамилии и пола
    person = Person('ru')
    sex_list = ['f', 'm']
    sex = random.choice(sex_list)
    if sex == 'f':
        fullname = person.full_name(gender = Gender.FEMALE)
    else:
        fullname = person.full_name(gender = Gender.MALE)
    
    full = fullname.split(' ')
    first_name = full[0]
    last_name = full[1]
    personArr = [first_name, last_name, sex]
    return personArr
#
def generatorGender():
    person = Person('ru')
    gend = person.gender()
    if gend == 'Муж.':
        return 'M'
    else:
        return 'F'

@romanized('ru')
def russian_name(name):
    return name

def generatorFirstName(gend):
    person = Person('ru')
    if gend == 'M':
        name = person.first_name(gender = Gender.MALE)
           
    else:
        name = person.first_name(gender = Gender.FEMALE)
        
    return russian_name(name)

def generatorLastName(gend):
    person = Person('ru')
    if gend == 'M':
        name = person.last_name(gender = Gender.MALE)
    
    else:
        name = person.last_name(gender = Gender.FEMALE)

    return russian_name(name)


# Функции, отвечающие за формирование запроса sql и отправку данных

def formSQL(dictItems, table_name, database_name): #формирование запроса на вставку данных 
    
    maskSQL = "INSERT INTO " + database_name + "." + table_name + "("
    keyDict = dictItems.keys()
    #print(keyDict)
    valDict = dictItems.values()
    #print(valDict)
    for i in keyDict:
        maskSQL += " " + str(i) + ","
    maskSQL = maskSQL[:-1]
    maskSQL += ') VALUES ('
    for i in valDict:
        maskSQL += " `" + str(i) + "`,"
    maskSQL = maskSQL[:-1]
    maskSQL += ');'
    return maskSQL

def formDropTableSQL(table_name, database_name):
    maskSQL = 'DROP TABLE ' + database_name + '.' + table_name
    return maskSQL



# Проходка по всем таблицам, алгоритм распределения по рангам
def keyFunc(item):
    return item[2]

def goToTable(rangList, listTables, numb): #список с рангами, список таблиц со столбцами, список с количеством элементов (для 1-2 рпнга и для 3-го ранга)
    rangList.sort(key=keyFunc)
    #print(rangList)
    colAll = {}
    
    for k in listTables:
        colTable = []
        for b in k[1]:
            colTable.append([b[0], b[1]])          
        colAll[k[0]] = colTable
    #print(colAll)
    rezStrArr = []
    for i in rangList:
        tablecolumns = []
        table_name = i[1]
        
        rezStr = []
        table_columns = colAll[table_name]
        #print(table_columns)
        
        if i[2] == 1:
            rezArrDict = generatorStr(table_columns, numb[0])
            print()
            for j in rezArrDict:
                rezStr.append(formSQL(j, table_name, database_name))
            rezStrArr.append(rezStr)
            print(rezStr)
        elif i[2] == 2:
            rezArrDict = generatorStr(table_columns, numb[0])
            print()
            for j in rezArrDict:
                rezStr.append(formSQL(j, table_name, database_name))
            print(rezStr)
            rezStrArr.append(rezStr)
        elif i[2] == 3:
            rezArrDict = generatorStr(table_columns, numb[1])
            print()
            condition = i[3]
            conditionArr = condition.split(", ")
            print(conditionArr)
            print()
            for j in rezArrDict:
                rezIntermediant = formSQL(j, table_name, database_name)
                
                rezStr.append(rezIntermediant)
            rezStrArr.append(rezStr)
            print(rezStr)

   
    return rezStrArr
###############################################

###############################################
## исполняющая часть, коннект с бд и последовательное выполнение алгоритма

database_from = 'databasetest'
database_in = 'databasetesttopython'


try: 
    conn = mysql.connector.connect(user='root', password='12345', host='localhost', database=database_from)
    
except Error as e:
    print('Error while connecting to MySql', e)
finally:
    if (conn.is_connected()):
        strArrGlobal = []
        cursor = conn.cursor()
        listTable = getInfoAboutTables(database_from)
        rangList = findRang()
        

        ddlSQL = []
        for i in listTable:
            ddlSQL.append(getInfoForCopyTable(i[0], 'databasetest'))
        print(ddlSQL)
        conn.close()    
        try:
            conn = mysql.connector.connect(user='root', password='12345', host='localhost', database=database_in)
    
        except Error as e:
            print('Error while connecting to MySql', e)
        finally:
            cursor = conn.cursor()
            listTableNew = getInfoAboutTables(database_in)
            if len(listTableNew) != 0:
                for i in listTableNew:
                    strEx = formDropTableSQL(i[0], database_in)
                    cursor.execute(strEx)
                cursor.execute("COMMIT")
            
            for i in ddlSQL:
                for j in i:
                    cursor.execute(j[1])
            cursor.execute("COMMIT")

            rez = goToTable(rangList, listTable, [10, 5], database_in)
            print(rez)
                            
            for i in rez:
                for j in i:
                    cursor.execute(j)
            cursor.execute("COMMIT")
            cursor.close()
            conn.close()

#################################################








