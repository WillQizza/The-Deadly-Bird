CMPUT404-project-socialdistribution
===================================

Build
============
Run the backend:
```shell
git clone git@github.com:uofa-cmput404/w24-project-the-deadly-bird.git
cd w24-project-the-deadly-bird/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver 
```

Run the frontend:
```shell
cd frontend
npm i
npm run start
```

Or run everything at once with docker:
```shell
docker build -t deadly-bird .      
docker run -p 8000:8000 deadly-bird

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
