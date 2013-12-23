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
    mkdir tmp covers
    
Edit hmdb.conf and adapt it to your needs.

If you change the BASE_DIR or the OUTPUT_DIR variables, you need to edit the html templates.
And set properly this line depending on your local configuration:
    <link rel="stylesheet" href="/hmdb/templates/style.css" type="text/css" />
    <img height="80px" src="/hmdb/download.png" />


Usage
===

    python2.7 hmdb.py -n
    [Regenerating new index...]
    Scanning dir: /var/www/videos

    Original: The.Simpsons.S25E04.HDTV.x264-LOL.mp4
    imdb ==> The Simpsons Movie
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
    

