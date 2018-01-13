import re
import csv
import sys
import json
import mysql.connector
import exifread
import hashlib
import yaml
import pprint


def dump(obj):
    print json.dumps(obj, sort_keys=True, indent=4)

def edump(obj):
    return json.dumps(obj, sort_keys=True, indent=4)

def getMysqlConn():
    cnx = mysql.connector.connect(user='root', password='spine4me',
                              host='127.0.0.1',
                              database='images')
    return cnx

def loadImageSchema(filename = 'images_schema.json'):
    json_data=open(filename).read()
    data = json.loads(json_data)
    cols=[]
    for colname in data:
        ct = data[colname]["COLUMN_TYPE"]
        cl = data[colname]["COLLATION_NAME"]
        cs = data[colname]["CHARACTER_SET_NAME"]
        xtra = data[colname]["EXTRA"]
        if cl != None:
            sql = "{} {} CHARACTER SET {} COLLATE {} {}".format(colname, ct, cs, cl, xtra)
        else:
            sql = "{} {} {}".format(colname, ct, xtra)
        cols.append(sql)
    return cols

def getImageSchema(myconn, filename = 'images_schema.json'):
    cur = myconn.cursor();
    sql = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS where table_name = 'images'"
    cur.execute(sql)
    cols=[]
    for r in cur.description:
        cols.append(r[0])
    sc={}
    for r in cur:
        i = 0
        schema={}
        for k in r:
            #print k
            schema[cols[i]] = k
            i = i + 1
        sc[schema['COLUMN_NAME']] = schema
    with open(filename, 'w') as outfile:
        json.dump(sc, outfile, sort_keys=True, indent=4)
    
def createImageTable(myconn):
    cur = myconn.cursor();
    cur.execute("drop table if exists images")
    columns = loadImageSchema()
    sql = '''
    CREATE TABLE IF NOT EXISTS images (
    {},
    PRIMARY KEY (id)
    )
'''.format( ",\n".join(columns))
    cur.execute(sql);
    cur.close();
    return

def getImageInfo(image):
    f = open(image,'rb')
    tags = exifread.process_file(f)
    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            print "%s=%s" % (tag, tags[tag])

def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()

if __name__ == '__main__':
    myconn = getMysqlConn()
    #getImageSchema(myconn)
    createImageTable(myconn)
    sys.exit()
    print myconn
    ti = '/var/www/schoenster.com/html/images/DSCN0337[1].jpg'
    getImageInfo(ti)
    h = md5sum(ti)
    myconn.close()
