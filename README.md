Home Media Data Base
====

A python script to read your local videos (in the filesystem) 
and generates a nice web page with some information obtained from imdb.com
and allows the direct download.

Features:

* Automatic download of covers, pictures and information from imdb.com
* Even, if the file name is dirty, hmdb.py cleans it and try to find it in imdb.com
* Creates an index.html with the movies ordered by imdb puntuation

Warning: 

I made this software for myself, it is very simple and a quite dirty.
It may be extended with several features. The most important is add better support for tv shows.
But I have not time and I am too lazy, so if you like contribute with the code, it is AGPLv3


Requirements
===

* python 2.7
* convert from ImageMagick: apt-get install imagemagick
* any web server such as Apache or Lighttpd: apt-get install lighttpd
* any other requirement from imdbPY https://github.com/alberanid/imdbpy


Installation
===
If your document root is /var/www (most common)

    cd /var/www
    git clone https://github.com/p4u/hmdb.git hmdb
    cd hmdb
    mkdir tmp
    
Edit hmdb.conf and adapt it to your needs.

Configure MOVIES_DIR variable, it can contain several directories separated by comas
IMPORTANT: the movie's directories must be reachable from the web server, 
the easy way to do so ins creaing a symlink:
    ln -s /home/user/movies /var/www/movies

If you change the BASE_DIR or the OUTPUT_DIR variables, you need to edit the html templates.
And set properly this line depending on your local configuration:
    <link rel="stylesheet" href="/hmdb/templates/style.css" type="text/css" />
    <img height="80px" src="/hmdb/download.png" />


Usage
===

    p4u@nomada:/var/www/hmdb# python2.7 hmdb.py 
    hmdb | [Home Media Data Base]
     use: hmdb.py <-n|-u|-c|-h>
        -n: Create a new database from scratch
        -u: Update an existing databse with only new files
        -c: Continue from previous session
        -h: Print this dirty help


    p4u@nomada:/var/www/hmdb# python2.7 hmdb.py -n
    [Regenerating new index...]
    Scanning dir: /var/www/videos

    Original: The.Simpsons.S25E04.HDTV.x264-LOL.mp4
    imdb ==> The Simpsons
    ------------------------------------------------------
    Original: How.I.Met.Your.Mother.S09E12.HDTV.x264-KILLERS.mp4
    imdb ==> How I Met Your Mother
    ------------------------------------------------------
    Original: How.I.Met.Your.Mother.S09E11.HDTV.x264-KILLERS.mp4
    imdb ==> How I Met Your Mother
    ------------------------------------------------------
    Original: boardwalk.empire.s04e09.hdtv.x264-2hd.mp4
    imdb ==> Boardwalk Empire
    ------------------------------------------------------
    
