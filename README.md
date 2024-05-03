The Deadly Bird
===================================

A distributed social media platform similiar to Mastodon.

- <a href="https://www.figma.com/file/0yC4iSm1go8vglzSXZPfhy/the-deadly-bird?type=design&node-id=0%3A1&mode=design&t=mczNMkpmOdCOt6Ki-1">Figma</a>
- <a href="https://thedeadlybird.willqi.dev">Demo Site (User Content Restricted!)</a>

Running
============
Run the app locally:
```shell
docker run -p 8000:8000 registry.willqi.dev/public-thedeadlybird:1
```

Run the app without Docker:
```shell
cd frontend
npm install
npm run build
cd ../backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Contributing
============

Send a pull request and be sure to update this file with your name.

Contributors / Licensing
========================

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle.

All text is licensed under the CC-BY-SA 4.0 http://creativecommons.org/licenses/by-sa/4.0/deed.en_US

Contributors:

    Karim Baaba
    Ali Sajedi
    Kyle Richelhoff
    Chris Pavlicek
    Derek Dowling
    Olexiy Berjanskii
    Erin Torbiak
    Abram Hindle
    Braedy Kuzma
    Nhan Nguyen 
    William Qi
    Justin Meimar
    Ritwik Rastogi
    Irene Sun
    Chase Johnson
