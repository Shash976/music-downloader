from download_mp3 import *

destination = input("Destination: ")
while 1:
    link = input("Youtube Link: ")
    getMP3fromLink(link, destination)
