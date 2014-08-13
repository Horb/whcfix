whcfix 
======

A Data Aggregator for Wakefield Hockey Club Fixtures
----------------------------------------------------

A Flask application that produces a tailed view of recent fixtures, results and league tables for Wakefield Hockey Club by dynamically gathering data from various sources.

A live instance can be found [here](http://www.whcfix.com).


Setup
-----

On a Debian based system;

    apt-get install git python-dev python-pip
    pip install flask BeautifulSoup requests
    git clone https://github.com/Horb/whcfix.git
    cd whcfix
    python app.py


Open up a browser and navigate to http://localhost:5000/ and you'll see a homepage akin to whcfix.com.


Contribution/Roadmap
--------------------

* The site could be prettier.
* Integration with social media and/or user content in the form of match reports and top scorer statistics.
* Draw league tables from FixturesLive/EnglandHockey.
