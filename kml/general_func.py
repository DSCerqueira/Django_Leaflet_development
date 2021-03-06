#general functions
import pandas as pd
import sqlite3, sys, os, kml2geojson
import math as mt
from django.core.files.storage import FileSystemStorage


pathl = sys.path

def upload_sites(table):
    con = sqlite3.connect('dbtables.sqlite3')
    cur = con.cursor()
    try:
        cur.execute('DROP TABLE sites')
    except:
        pass

    dataframe = pd.read_csv(table)
    strqueryend = '(STID INTEGER PRIMARY KEY AUTOINCREMENT,'
    strquery = '('
    for i in list(dataframe.columns):
        strqueryend = strqueryend + i + ','
        strquery = strquery + i + ','

    strqueryend = strqueryend + 'SELECTOR,COLOR)'
    strquery = strquery + 'SELECTOR,COLOR)'
    sqlqueryend = 'CREATE TABLE sites ' + strqueryend
    cur.execute(sqlqueryend)
    row = 0
    sqlcoluna = ''
    dima = dataframe.shape

    #collecting data
    for i in range(dima[0]):
        col = 0
        sqlrow = '('
        for n in list(dataframe.loc[i]):
            sqlrow = sqlrow + '"' + str(n) + '",'
            col = col + 1
        sqlrow = sqlrow + '"","")'

        if i < int(dima[0] - 1):
            sqlcoluna = sqlcoluna + sqlrow + ','

        if i == int(dima[0] - 1):
            sqlcoluna = sqlcoluna + sqlrow + ';'

    #####insertin data into the table sites######
    sqlquery = 'INSERT INTO sites ' + strquery + ' VALUES' + sqlcoluna
    cur.execute(sqlquery)
    con.commit()
    try:
        cur.execute('DROP TABLE sitestemp')
        sqlquery = 'CREATE TABLE sitestemp AS SELECT * FROM sites;'
        cur.execute(sqlquery)
    except:
        sqlquery = 'CREATE TABLE sitestemp AS SELECT * FROM sites;'
        cur.execute(sqlquery)

def upload_sectors(table):
    con = sqlite3.connect('dbtables.sqlite3')
    cur = con.cursor()
    try:
        cur.execute('DROP TABLE sectors')
    except:
        pass

    dataframe = pd.read_csv(table)
    strqueryend = '(SECID INTEGER PRIMARY KEY AUTOINCREMENT,'
    strquery = '('
    for i in list(dataframe.columns):
        strqueryend = strqueryend + i + ','
        strquery = strquery + i + ','

    strqueryend = strqueryend + 'SELECTOR,COLOR)'
    strquery = strquery + 'SELECTOR,COLOR)'
    sqlqueryend = 'CREATE TABLE sectors ' + strqueryend
    cur.execute(sqlqueryend)
    row = 0
    sqlcoluna = ''
    dima = dataframe.shape

    #collecting data
    for i in range(dima[0]):
        col = 0
        sqlrow = '('
        for n in list(dataframe.loc[i]):
            sqlrow = sqlrow + '"' + str(n) + '",'
            col = col + 1
        sqlrow = sqlrow + '"","")'

        if i < int(dima[0] - 1):
            sqlcoluna = sqlcoluna + sqlrow + ','

        if i == int(dima[0] - 1):
            sqlcoluna = sqlcoluna + sqlrow + ';'

    #####insertin data into the table sites######
    sqlquery = 'INSERT INTO sectors ' + strquery + ' VALUES' + sqlcoluna
    cur.execute(sqlquery)
    con.commit()
    try:
        cur.execute('DROP TABLE sectorstemp')
        sqlquery = 'CREATE TABLE sectorstemp AS SELECT * FROM sectors;'
        cur.execute(sqlquery)
    except:
        sqlquery = 'CREATE TABLE sectorstemp AS SELECT * FROM sectors;'
        cur.execute(sqlquery)

def upload_table(table,name):

    tbname=name

    con = sqlite3.connect('dbtables.sqlite3')
    cur = con.cursor()

    try:
        sqlquery = 'DROP TABLE ' + tbname
        cur.execute(sqlquery)
    except:
        pass
    dataframe = pd.read_csv(table)
    strqueryend = '('
    strquery = '('
    for i in list(dataframe.columns):
        strqueryend = strqueryend + i + ','
        strquery = strquery + i + ','

    strqueryend = "CREATE TABLE " + tbname + " " + strqueryend + "random )"
    strquery = strquery + "random)"
    try:
        cur.execute(strqueryend)
    except:
        pass

    row = 0
    sqlcoluna = ''
    dima = dataframe.shape

    #collecting data
    for i in range(dima[0]):
        col = 0
        sqlrow = '('
        for n in list(dataframe.loc[i]):
            sqlrow = sqlrow + '"' + str(n) + '",'
            col = col + 1
        sqlrow = sqlrow + '"")'

        if i < int(dima[0] - 1):
            sqlcoluna = sqlcoluna + sqlrow + ','

        if i == int(dima[0] - 1):
            sqlcoluna = sqlcoluna + sqlrow + ';'

    #####insertin data into the table sites######
    sqlquery = 'INSERT INTO '+tbname+" " + strquery + ' VALUES' + sqlcoluna
    try:
        cur.execute(sqlquery)
        con.commit()
    except sqlite3.OperationalError as err:
        erroname = 'Connection failed. Erro type: ' + str(err)
        return(erroname)

def runqdtb(query):
    query=query
    con = sqlite3.connect('dbtables.sqlite3')
    cur = con.cursor()
    try:
        cur.execute(query)
        table=pd.DataFrame(cur.fetchall())
        field=cur.description
        serie=table.values.tolist()
        fieldname=[]
        for i in field:
            fieldname.append(i[0])
        seriepass=serie[0:500]
        #creating a temporary view#
        try:
            cur.execute('DROP VIEW temporaryview;')
        except:
            pass
        query='CREATE VIEW temporaryview AS '+query
        cur.execute(query)
        return(fieldname,seriepass)
    except:
        return([],[])

def listables():
    con = sqlite3.connect('dbtables.sqlite3')
    cur = con.cursor()
    try:
        query="SELECT name FROM sqlite_master WHERE type = " + "'table';"
        cur.execute(query)
        tables=pd.DataFrame(cur.fetchall())
        tables=tables.values.tolist()
        serie=[]
        for i in tables:
            serie.append(i[0])
        serie=list(serie)
        return(serie)
    except:
        return([])

def colorsetting(color):
    try:
        con = sqlite3.connect('dbtables.sqlite3')
        cur = con.cursor()
        cur.execute('SELECT site from temporaryview')
        lista=pd.DataFrame(cur.fetchall())
        lista=lista.values.tolist()
        setcolor = '('
        for i in lista:
            setcolor = setcolor + "'" +str(i[0]) + "',"
        setcolor = setcolor + '"")'
        query = "UPDATE sites SET COLOR='" + color + "' WHERE SITE IN " + setcolor;
        cur.execute(query)
        con.commit()
        return
    except:
        pass

def colorsettingsec(color):
    try:
        con = sqlite3.connect('dbtables.sqlite3')
        cur = con.cursor()
        cur.execute('SELECT sector from temporaryview')
        lista=pd.DataFrame(cur.fetchall())
        lista=lista.values.tolist()
        setcolor = '('
        for i in lista:
            setcolor = setcolor + "'" +str(i[0]) + "',"
        setcolor = setcolor + '"")'
        query = "UPDATE sectors SET COLOR='" + color + "' WHERE sector IN " + setcolor;
        cur.execute(query)
        con.commit()
        return
    except:
        pass

def kmlsectors(elementtyp):
    fs = FileSystemStorage()
    con = sqlite3.connect('dbtables.sqlite3')
    cur = con.cursor()
    limiter = 0
    try:
        sqlquery = 'SELECT * FROM sites'
        cur.execute(sqlquery)
        tablesites = pd.DataFrame(cur.fetchall())
        tablesites.sort_values(by=[1, 2], inplace=True)
        aux = list(cur.description)
        fields = []
        for i in aux:
            fields.append(i[0])

        try:
            sqlquery = 'SELECT * FROM sectors'
            cur.execute(sqlquery)
            tablesectors = pd.DataFrame(cur.fetchall())
            tablesectors.sort_values(by=[1, 3, 4], inplace=True)
            agregation = list(tablesites[1].unique())
            aux = list(cur.description)
            fieldsect = []
            for i in aux:
                fieldsect.append(i[0])
        except:
            agregation = list(tablesites[1].unique())
            pass

        ############creating agregation style#############

        kmltext = open('kml/static/fileserver/geomap.txt', 'w')
        kmltext.writelines(['<?xml version="1.0" encoding="UTF-8"?>\n',
                                 '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" \n',
                                 'xmlns:atom="http://www.w3.org/2005/Atom" >\n'])
        kmltext.close()
        kmltext = open('kml/static/fileserver/geomap.txt', 'a')
        kmltext.writelines(['<Document>\n',
                                 '\t<name>KML_File_Sectors</name>\n'])
        listcolor = ['FF0000FF', 'FFB469FF', 'FFB469FF', 'FF9314FF', 'FF9314FF', 'FF00FF00', 'FF00FF00', 'FF00FF7F',
                     'FF00FF7F', 'FF9AFA00', 'FF9AFA00', 'FF2FFFAD', 'FF2FFFAD', 'FF32CD32', 'FF32CD32', 'FF32CD9A',
                     'FF32CD9A', 'FF228B22', 'FF228B22', 'FFFF7084', 'FFFF7084', 'FFCD0000', 'FFCD0000', 'FFE16941',
                     'FFE16941', 'FFFF0000', 'FFFF0000', 'FF00FFFF', 'FF00FFFF', 'FF00D7FF', 'FF00D7FF', 'FF82DDEE',
                     'FF82DDEE', 'FF20A5DA', 'FF20A5DA', 'FF0B86B8', 'FF0B86B8', 'FF8B7B6C', 'FF8B7B6C', 'FFFFF500',
                     'FFFFF500', 'FF3333CD', 'FF3333CD', 'FF23238B', 'FF23238B', 'FF698CFF', 'FF698CFF', 'FF8B008B',
                     'FF8B008B', 'FF00008B', 'FF00008B', 'FF90EE90', 'FF90EE90', 'FF1D66CD', 'FF1D66CD', 'FF86838B',
                     'FF86838B', 'FFD2D5EE', 'FFD2D5EE', 'FFB5B7CD', 'FFB5B7CD', 'FFED9564', 'FFED9564', 'FFE1E4FF',
                     'FFE1E4FF', 'FFFFFFFF', 'FFFFFFFF', 'FF000000', 'FF000000', 'FF4F4F2F', 'FF4F4F2F', 'FF696969',
                     'FF696969', 'FF394FCD', 'FF394FCD', 'FF26368B', 'FF26368B', 'FF0045FF', 'FF0045FF']
        ncolor = -1

        for i in agregation:
            ncolor = ncolor + 1
            kmltext.writelines(['\t<Style id="' + i + '">\n',
                                     '\t\t<IconStyle>\n',
                                     '\t\t\t<color>' + listcolor[ncolor] + '</color>\n',
                                     '\t\t\t<scale>0.5</scale>\n',
                                     '\t\t\t<Icon>\n',
                                     '\t\t\t\t<href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href>\n',
                                     '\t\t\t</Icon>\n',
                                     '\t\t</IconStyle>\n',
                                     '\t</Style>\n'])
        ########################creating folder agregation-sites#############################

        for n in range(len(agregation)):
            kmltext.writelines(['\t<Folder>\n', '\t\t<name>' + agregation[n] + '</name>\n'])

            for i in range(tablesites.shape[0]):

                if tablesites[1][i] == agregation[n]:

                    auxcolor = tablesites[tablesites.shape[1] - 1][i]
                    if auxcolor != '':
                        color = 'FF' + auxcolor[5] + auxcolor[6] + auxcolor[3] + auxcolor[4] + auxcolor[1] + \
                                auxcolor[2]
                    elif auxcolor == '':
                        color = 'ffffffff'
                    selected = tablesites[tablesites.shape[1] - 2][i]
                    site = tablesites[2][i]
                    lat = float(tablesites[3][i])
                    long = float(tablesites[4][i])
                    altitude = 0
                    terminator = 0
                    contador = 0
                    aux2 = 0

                    if elementtyp == 'sectorclick':
                        for isc in range(tablesectors.shape[0]):
                            terminator = terminator + 1
                            if tablesectors[3][isc] == site:
                                count = 'start'
                                contador = terminator
                                aux = float(tablesectors[5][isc] * 1) + float(tablesectors[13][isc] * 1)
                                if aux2 > aux:
                                    aux = aux2
                                if aux * 1 > altitude:
                                    altitude = aux
                            elif count == 'start' and terminator > contador and contador > 0:
                                aux2 = float(tablesectors[5][isc] * 1) + float(tablesectors[13][isc] * 1)
                                break
                            else:
                                pass
                    else:
                        pass

                    kmltext.writelines(['\t\t<Style id="corsite">\n', '\t\t\t<IconStyle>\n',
                                             '\t\t\t\t<color>' + color + '</color>\n',
                                             '\t\t\t\t<scale>0.5</scale>\n',
                                             '\t\t\t\t<Icon>\n',
                                             '\t\t\t\t\t<href>http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png</href>\n',
                                             '\t\t\t\t</Icon>\n', '\t\t\t</IconStyle>\n', '\t\t</Style>\n'])
                    kmltext.writelines(
                        ['\t\t<Folder>\n', '\t\t\t<name>' + site + '</name>\n', '\t\t\t<Placemark>\n',
                         '\t\t\t\t<name>' + site + '</name>\n'])

                    ###############starting site description##################
                    kmltext.writelines(
                        ['\t\t\t\t\t<description><![CDATA[<table border="1" padding="0"></tr><td>'])

                    for l in range(5, tablesites.shape[1] - 2):
                        paramsites = tablesites[l][i]
                        kmltext.writelines('<tr><td>' + fields[l] + '=' + paramsites + '</tr><td>')
                    kmltext.writelines([']]></description>\n', '\t\t\t\t<styleUrl>#corsite</styleUrl>\n'])
                    kmltext.writelines(['\t\t\t\t<Point>\n', '\t\t\t\t\t<extrude>1</extrude>\n',
                                             '\t\t\t\t\t<altitudeMode>absolute</altitudeMode>\n',
                                             '\t\t\t\t\t<coordinates>' + str(long) + ',' + str(lat) + ',' + str(
                                                 altitude) + '</coordinates>\n', '\t\t\t\t</Point>\n',
                                             '\t\t\t</Placemark>\n'])

                    ###################starting sector creation##################################

                    if elementtyp == 'sectorclick':
                        counter = 0
                        terminator = 0
                        for isc in range(limiter, tablesectors.shape[0]):

                            if site == tablesectors[3][isc]:
                                counter = terminator
                                limiter = limiter + 1
                                auxcolorsec = tablesectors[tablesectors.shape[1] - 1][isc]
                                if auxcolorsec != '':
                                    colorsec = "80" + auxcolorsec[5] + auxcolorsec[6] + auxcolorsec[3] + \
                                               auxcolorsec[4] + auxcolorsec[1] + auxcolorsec[2]
                                elif auxcolorsec == '':
                                    colorsec = '28FFFFFF'
                                selectedsec = tablesectors[tablesectors.shape[1] - 2][isc]
                                sector = tablesectors[4][isc]
                                height = float(tablesectors[5][isc] * 1) + float(
                                    tablesectors[13][isc] * 1)
                                azimuth = float(tablesectors[6][isc] * 1)
                                tilt = float(tablesectors[7][isc] * 1) + float(tablesectors[8][isc] * 1)
                                bandvert = float(tablesectors[10][isc] * 1)
                                bandhor = float(tablesectors[9][isc] * 1)
                                altitude = float(tablesectors[13][isc] * 1)

                                kmltext.writelines(['\t\t\t<Placemark>\n'])
                                kmltext.writelines(
                                    ['\t\t\t\t<description><![CDATA[<table border="1" padding="0"></tr><td>',
                                     '<tr><td>SETOR = ' + sector + '</tr><td>'])

                                for lns in range(14, tablesectors.shape[1] - 2):
                                    paramsector = tablesectors[lns][isc]
                                    kmltext.writelines(
                                        ['<tr><td>' + fieldsect[lns] + '=' + paramsector + '</tr><td>'])
                                kmltext.writelines([']]></description>\n'])

                                kmltext.writelines(['\t\t\t<Style id="corset">\n', '\t\t\t\t<PolyStyle>\n',
                                                         '\t\t\t\t\t<color>' + colorsec + '</color>\n',
                                                         '\t\t\t\t</PolyStyle>\n',
                                                         '\t\t\t</Style>\n'])
                                latp1 = lat + (250 * (180 / mt.pi) * mt.cos(
                                    (azimuth - bandhor / 2) * mt.pi / 180)) / 6371000
                                lonp1 = long + (250 * (180 / mt.pi) * mt.sin(
                                    (azimuth - bandhor / 2) * mt.pi / 180)) / 6371000

                                latp2 = lat + (250 * (180 / mt.pi) * mt.cos(
                                    (azimuth + bandhor / 2) * mt.pi / 180)) / 6371000
                                lonp2 = long + (250 * (180 / mt.pi) * mt.sin(
                                    (azimuth + bandhor / 2) * mt.pi / 180)) / 6371000
                                heigthf = height - 250 * mt.tan(tilt * mt.pi / 180)

                                kmltext.writelines(
                                    ['\t\t\t\t<Polygon>\n', '\t\t\t\t\t<altitudeMode>absolute</altitudeMode>\n',
                                     '\t\t\t\t\t<outerBoundaryIs>\n', '\t\t\t\t\t\t<LinearRing>\n'
                                                                      '\t\t\t\t\t\t\t<coordinates>\n',
                                     '\t\t\t\t\t\t\t\t' + str(long) + ',' + str(lat) + ',' + str(height) + ' ' +
                                     str(lonp1) + ',' + str(latp1) + ',' + str(heigthf) + ' ' + str(
                                         lonp2) + ',' + str(latp2) + ',' + str(heigthf) + ' '
                                     + str(long) + ',' + str(lat) + ',' + str(height) + '\n',
                                     '\t\t\t\t\t\t\t</coordinates>\n',
                                     '\t\t\t\t\t\t</LinearRing>\n', '\t\t\t\t\t</outerBoundaryIs>\n',
                                     '\t\t\t\t\t<heading>90</heading><tilt>10</tilt>\n',
                                     '\t\t\t\t</Polygon>\n', '\t\t\t\t<StyleUrl>#corset</StyleUrl>\n',
                                     '\t\t\t</Placemark>\n'])

                            else:
                                pass
                            if counter > 0:
                                xy = terminator - counter
                                if xy == 1:
                                    break
                            terminator = terminator + 1

                    kmltext.writelines(['\t\t</Folder>\n'])
                else:
                    pass
            kmltext.writelines(['\t</Folder>\n'])
        kmltext.writelines(['</Document>\n', '</kml>\n'])
        kmltext.close()
        elementtyp == 'site'
        try:
            pathfile = 'del ' + fs.location + '/kml/static/fileserver/geomap.kml'
            pathfile = pathfile.replace('/', os.sep)
            os.system(pathfile)
        except:
            pass
        pathfile = 'rename ' + fs.location + '/kml/static/fileserver/geomap.txt geomap.kml'
        pathfile = pathfile.replace('/', os.sep)
        os.system(pathfile)
    except:
        elementtyp == 'site'
        pass


def geojsonsectors(elementtyp):
    fs = FileSystemStorage()
    con = sqlite3.connect('dbtables.sqlite3')
    cur = con.cursor()
    limiter = 0
    try:
        sqlquery = 'SELECT * FROM sites'
        cur.execute(sqlquery)
        tablesites = pd.DataFrame(cur.fetchall())
        tablesites.sort_values(by=[1, 2], inplace=True)
        aux = list(cur.description)
        fields = []
        for i in aux:
            fields.append(i[0])

        try:
            sqlquery = 'SELECT * FROM sectors'
            cur.execute(sqlquery)
            tablesectors = pd.DataFrame(cur.fetchall())
            tablesectors.sort_values(by=[1, 3, 4], inplace=True)
            agregation = list(tablesites[1].unique())
            aux = list(cur.description)
            fieldsect = []
            for i in aux:
                fieldsect.append(i[0])
        except:
            pass

        ############creating agregation style#############

        kmltext = open('kml/static/fileserver/geomap.txt', 'w')
        kmltext.writelines(['{ \n "type": "FeatureCollection",\n'])
        kmltext.writelines(['"features":[\n'])

        kmltext.close()
        kmltext = open('kml/static/fileserver/geomap.txt', 'a')

        ########################creating folder agregation-sites#############################
        for i in range(tablesites.shape[0]):

            colorsite = tablesites[tablesites.shape[1] - 1][i]
            if colorsite == '':
                colorsite = '#eaebec'

            selected = tablesites[tablesites.shape[1] - 2][i]
            site = tablesites[2][i]
            lat = round(float(tablesites[3][i]), 8)
            long = round(float(tablesites[4][i]), 8)
            ###############starting site description##################
            # estou aqyi
            kmltext.writelines('{\n"type": "Feature",\n')
            kmltext.writelines('"properties": {')
            kmltext.writelines('"Site":"' + str(site) + '",\n')
            for l in range(5, tablesites.shape[1] - 2):
                paramsites = tablesites[l][i]
                kmltext.writelines('"' + fields[l] + '": "' + tablesites[l][i] + '",')
            kmltext.writelines('"none":""},\n')
            kmltext.writelines('"geometry": {\n')
            kmltext.writelines('"type": "Point",\n')
            kmltext.writelines('"coordinates": [' + str(long) + "," + str(lat) + ']\n')
            kmltext.writelines('}\n')
            kmltext.writelines('},\n')  # ending site

            ###################starting sector creation##################################

            if elementtyp == 'sectorclick':
                counter = 0
                terminator = 0
                for isc in range(limiter, tablesectors.shape[0]):

                    if site == tablesectors[3][isc]:
                        counter = terminator
                        limiter = limiter + 1

                        kmltext.writelines('{\n"type": "Feature",\n')


                        colorsec = tablesectors[tablesectors.shape[1] - 1][isc]
                        if colorsec == '':
                            colorsec = '#55ffff'
                        selectedsec = tablesectors[tablesectors.shape[1] - 2][isc]
                        sector = tablesectors[4][isc]
                        azimuth = float(tablesectors[6][isc] * 1)
                        bandhor = float(tablesectors[9][isc] * 1)

                        kmltext.writelines('"properties": {')
                        kmltext.writelines('"sector":"' + str(sector) + '",\n')
                        for lns in range(14, tablesectors.shape[1] - 2):
                            paramsector = tablesectors[lns][isc]
                            kmltext.writelines('"' + fieldsect[lns] + '": "' + tablesectors[lns][isc] + '",')
                        kmltext.writelines('"color":"' + str(colorsec) + '"},\n')
                        #kmltext.writelines('"none":""},\n')
                        kmltext.writelines('"geometry": {\n')
                        kmltext.writelines('"type": "Polygon",\n')

                        latp1 = lat + (250 * (180 / mt.pi) * mt.cos(
                            (azimuth - bandhor / 2) * mt.pi / 180)) / 6371000
                        lonp1 = long + (250 * (180 / mt.pi) * mt.sin(
                            (azimuth - bandhor / 2) * mt.pi / 180)) / 6371000

                        latp2 = lat + (250 * (180 / mt.pi) * mt.cos(
                            (azimuth + bandhor / 2) * mt.pi / 180)) / 6371000
                        lonp2 = long + (250 * (180 / mt.pi) * mt.sin(
                            (azimuth + bandhor / 2) * mt.pi / 180)) / 6371000

                        kmltext.writelines('"coordinates": [[[' + str(round(long,6)) + "," + str(round(lat ,6)) +'],'\
                                            +'['+str(round(lonp1,6))+','+str(round(latp1 ,6))+'],'
                                            +'['+str(round(lonp2,6))+','+str(round(latp2 ,6))+'],'
                                            +'['+str(round(long,6))+','+str(round(lat ,6))+']]]\n')

                        kmltext.writelines('}\n')
                        kmltext.writelines('},\n')  # ending sector

                    else:
                        pass
                    if counter > 0:
                        xy = terminator - counter
                        if xy == 1:
                            break
                    terminator = terminator + 1

        kmltext.writelines('{"type": "Feature",\n"properties": {"":""},\n"geometry": {\n"type": "Point",\n"coordinates": [0,0]\n}\n}')

        kmltext.writelines(']\n}\n')
        kmltext.close()
        elementtyp == 'site'
        try:
            pathfile = 'del ' + fs.location + '/kml/static/fileserver/geomap.geojson'
            pathfile = pathfile.replace('/', os.sep)
            os.system(pathfile)
        except:
            pass
        pathfile = 'rename ' + fs.location + '/kml/static/fileserver/geomap.txt geomap.geojson'
        pathfile = pathfile.replace('/', os.sep)
        os.system(pathfile)

    except:
        elementtyp == 'site'
        pass









