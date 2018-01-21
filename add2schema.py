import re

d='''NOT Whitebalance=AUTO
NOT ExifOffset=284
NOT ImageDescription=          
NOT XResolution=300
NOT Make=NIKON
NOT ColorMode=COLOR
NOT ResolutionUnit=Pixels/Inch
NOT YResolution=300
NOT AFFocusPosition=CenterCenterCenterCenter
NOT ISOSelection=AUTO  
NOT DateTime=2004:07:21 10:31:51
NOT ManualFocusDistance=1/0
NOT ImageSharpening=AUTO  
NOT Software=E4300v1.5
NOT Quality=FINE  
NOT YResolution=300
NOT AuxiliaryLens=OFF         
NOT Model=E4300
NOT Orientation=Horizontal (normal)
NOT YCbCrPositioning=Co-sited
NOT JPEGInterchangeFormat=4084
NOT ResolutionUnit=Pixels/Inch
NOT SceneMode=LAND SCAPE     
NOT XResolution=300
NOT ImageAdjustment=AUTO         
NOT NoiseReduction=OFF 
NOT JPEGInterchangeFormatLength=5502
NOT FocusMode=AF-C  
NOT Compression=JPEG (old-style)
NOT FlashSetting=       
NOT DigitalZoomFactor=1
NOT ISOSetting=[0, 0]'''

t = '''"%%name%%": {
        "CHARACTER_MAXIMUM_LENGTH": 50, 
        "CHARACTER_OCTET_LENGTH": 50, 
        "CHARACTER_SET_NAME": "utf8", 
        "COLLATION_NAME": "utf8_unicode_ci", 
        "COLUMN_COMMENT": "", 
        "COLUMN_DEFAULT": null, 
        "COLUMN_KEY": "", 
        "COLUMN_NAME": "%%name%%", 
        "COLUMN_TYPE": "varchar(50)", 
        "DATA_TYPE": "varchar", 
        "EXTRA": "", 
        "IS_NULLABLE": "YES", 
        "NUMERIC_PRECISION": null, 
        "NUMERIC_SCALE": null, 
        "ORDINAL_POSITION": 16, 
        "PRIVILEGES": "select,insert,update,references", 
        "TABLE_CATALOG": "def", 
        "TABLE_NAME": "images", 
        "TABLE_SCHEMA": "images"
    }, '''

for r in d.split("\n"):
    colname = r.split('=')[0].split(" ")[-1]
    new = re.sub('%%name%%', colname, t)
    print new


