BLOG_USER = 'BLOG_USER'
#CONNECTION_STRING = 'sqlite:////tmp/whcfix.db'
#CONNECTION_STRING = 'sqlite:///:memory:'
CONNECTION_STRING = 'mysql://whcfix_user:whcfix_password@localhost/DEV_whcfix'
BLOG_PASSWORD = 'BLOG_PASSWORD'
DEVELOPMENT_KEY = 'DEVELOPMENT_KEY'

LOG_FORMAT = '%(module)s %(funcName)s %(lineno)s %(message)s'

CONFIGS = {
    "configs": [
        {
            "dataSource": {
                "code": "4173", 
                "name": "Wakefield-Ladies-2s", 
                "source": "FixturesLive"
            }, 
            "teamName": "Wakefield 2", 
            "sectionName": "Ladies"
        }, 
        {
            "dataSource": {
                "code": "4221", 
                "name": "Wakefield-Ladies-3s", 
                "source": "FixturesLive"
            }, 
            "teamName": "Wakefield 3", 
            "sectionName": "Ladies"
        }, 
        {
            "dataSource": {
                "code": "4160", 
                "name": "Wakefield-Ladies-1s", 
                "source": "FixturesLive"
            }, 
            "teamName": "Wakefield 1", 
            "sectionName": "Ladies"
        }, 
        {
            "dataSource": {
                "code": "1131", 
                "name": "Wakefield-Mens-2s", 
                "source": "FixturesLive"
            }, 
            "teamName": "Wakefield 2", 
            "sectionName": "Mens"
        }, 
        {
            "dataSource": {
                "code": "1031", 
                "name": "Wakefield-Mens-1s", 
                "source": "FixturesLive"
            }, 
            "teamName": "Wakefield 1", 
            "sectionName": "Mens"
        }, 
        {
            "dataSource": {
                "club": "66", 
                "league": "138", 
                "source": "YorkshireHA"
            }, 
            "sectionName": "Mens"
        }, 
        {
            "dataSource": {
                "club": "66", 
                "league": "137", 
                "source": "YorkshireHA"
            }, 
            "sectionName": "Ladies"
        } 
    ]
}
