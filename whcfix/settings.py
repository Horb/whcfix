DEVELOPMENT_KEY = ''

UPLOAD_FOLDER = '/var/www/uploads'
ALLOWED_UPLOAD_EXTENSIONS = ('png', 'jpg', 'jpeg', 'gif')

LOG_FORMAT = '%(module)s %(funcName)s %(lineno)s %(message)s'

CONFIGS = {
    "configs": [
        {
            "dataSource": {
                "clubId": "66",
                "leagueId": "268",
                "source": "YorkshireHA"
            },
            "sectionName": "Mens"
        },
        {
            "dataSource": {
                "clubId": "66",
                "leagueId": "270",
                "source": "YorkshireHA"
            },
            "sectionName": "Ladies"
        },
        {
            "dataSource": {
                "clubId": "66",
                "leagueId": "269",
                "source": "YorkshireHA"
            },
            "sectionName": "Mens Development"
        },
        {
            "dataSource": {
                "fixLiveNumber": "4173",
                "club_name": "Wakefield 2",
                "source": "FixturesLive",
                "league" : "NTWHL Div 1"
            },
            "teamName": "Wakefield 2",
            "sectionName": "Ladies"
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
                "fixLiveNumber": "4160",
                "club_name": "Wakefield 1",
                "source" : "FixturesLive",
                "league" : "NTWHL Prem Div"
            },
            "teamName": "Wakefield 1",
            "sectionName": "Ladies"
        },
    ]
}

OLD_CONFIGS = {
    "configs": [
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
    ]
}
