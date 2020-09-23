DEVELOPMENT_KEY = ''

UPLOAD_FOLDER = '/var/www/uploads'
ALLOWED_UPLOAD_EXTENSIONS = ('png', 'jpg', 'jpeg', 'gif')

LOG_FORMAT = '%(module)s %(funcName)s %(lineno)s %(message)s'

CONFIGS = {
    "configs": [
        {
            "dataSource": {
                "clubId": "66",
                "leagueId": "328",
                "source": "YorkshireHA"
            },
            "sectionName": "Mens"
        },
        {
            "dataSource": {
                "clubId": "66",
                "leagueId": "330",
                "source": "YorkshireHA"
            },
            "sectionName": "Ladies"
        },
        {
            "dataSource": {
                "clubId": "66",
                "leagueId": "332",
                "source": "YorkshireHA"
            },
            "sectionName": "Mens Development"
        },
        {
            "dataSource": {
                "fixLiveNumber": "4173",
                "club_name": "Wakefield 2",
                "source": "FixturesLive",
                "league" : "NHL Div1 W"
            },
            "teamName": "Wakefield 2",
            "sectionName": "Ladies"
        },
        {
            "dataSource": {
                "fixLiveNumber": "1131",
                "club_name": "Wakefield 2",
                "source": "FixturesLive",
                "league" : "NHL EDiv3SM"
            },
            "teamName": "Wakefield 2",
            "sectionName": "Mens"
        },
    ]
}

DISABLED_CONFIGS = {
    "configs" : [
    ]
}
