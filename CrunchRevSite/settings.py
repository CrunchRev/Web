"""
2024, Written by the CrunchRev Authors

Settings file
"""

settings = {
    "URL": "unirev.xyz",
    "Database": {
        "URL": "localhost",
        "User": "root",
        "Password": "~TKb$Dw|pE7Fm}8R2fAx{CzLsrJQnR1Q~V7Rf6VP",
        "DatabaseName": "crunchrev_database"
    },
    "whitelistedPlaceIPs": {
        "86.209.13.245",
        "52.5.217.76",
        "46.174.51.158"
    },
    "PK1024Path": "../CrunchRevKeys/PrivateKey1024.pem",
    "PK2048Path": "../CrunchRevKeys/PrivateKey2048.pem",
    "FFlagsPath": "../ClientSettings/",
    "FFlags2018LPath": "../Client2018LSettings/",
    "FFlags2021EPath": "../Client2021ESettings/",
    "HTTPMethods": ['GET', 'POST'],
    "arbiterURLs": {
        "infra.unirev.xyz:7209",
        "infra2.unirev.xyz:7209",
        "infra3.unirev.xyz:7209"
    }
}
