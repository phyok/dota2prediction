dota2prediction
===============

A cool app to predict Dota 2 games!

To get started, run <tt>scrape.sh</tt>.
This will initialize and populate the database with scraped data.  It will also generate the csv and npz files needed by the predictor.

To launch the web app, enter the dota2_predictor directory (this contains the source for the web app) and run
<tt>python manage.py runserver</tt> to launch the server.

Visit localhost:8000 and start making predictions!
