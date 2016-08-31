BLOG_USER = 'BLOG_USER'
# CONNECTION_STRING = 'sqlite:////tmp/whcfix.db'
# CONNECTION_STRING = 'sqlite:///:memory:'
CONNECTION_STRING = 'mysql://whcfix_user:whcfix_password@localhost/DEV_whcfix'
BLOG_PASSWORD = 'BLOG_PASSWORD'
DEVELOPMENT_KEY = 'DEVELOPMENT_KEY'

UPLOAD_FOLDER = '/var/www/uploads'
ALLOWED_UPLOAD_EXTENSIONS = ('png', 'jpg', 'jpeg', 'gif')

LOG_FORMAT = '%(module)s %(funcName)s %(lineno)s %(message)s'

CONFIGS = {
    "configs": [
        {
            "dataSource": {
                "fixLiveNumber": "4173",
                "club_name": "Wakefield 2",
                "source": "FixturesLive",
                "league" : "NTWHL Prem Div"
            },
            "teamName": "Wakefield 2",
            "sectionName": "Ladies"
        },
        {
            "dataSource": {
                "fixLiveNumber": "4221",
                "club_name": "Wakefield 3",
                "source": "FixturesLive",
                "league" : "NTWHL D2SE"
            },
            "teamName": "Wakefield 3",
            "sectionName": "Ladies"
        },
        {
            "dataSource": {
                "fixLiveNumber": "4160",
                "club_name": "Wakefield 1",
                "source" : "FixturesLive",
                "league" : "IWHL WCN"
            },
            "teamName": "Wakefield 1",
            "sectionName": "Ladies"
        },
        {
            "dataSource": {
                "fixLiveNumber": "1131",
                "club_name": "Wakefield 2",
                "source": "FixturesLive",
                "league" : "NHML 2 East"
            },
            "teamName": "Wakefield 2",
            "sectionName": "Mens"
        },
        {
            "dataSource": {
                "fixLiveNumber": "1031",
                "club_name": "Wakefield 1",
                "source": "FixturesLive",
                "league" : "NHML Prem"
            },
            "teamName": "Wakefield 1",
            "sectionName": "Mens"
        },
        {
            "dataSource": {
                "clubId": "66",
                "leagueId": "207",
                "source": "YorkshireHA"
            },
            "sectionName": "Mens Development"
        },
        {
            "dataSource": {
                "clubId": "66",
                "leagueId": "204",
                "source": "YorkshireHA"
            },
            "sectionName": "Mens"
        },
        {
            "dataSource": {
                "clubId": "66",
                "leagueId": "205",
                "source": "YorkshireHA"
            },
            "sectionName": "Ladies"
        }
    ]
}
