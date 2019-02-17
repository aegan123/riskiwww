#!/usr/bin/env python3
import os
import sys
import urllib.request
import shutil
import zipfile
import subprocess


# Valmistelee tietokannan Djangon omalla migraatio työkalulla ja
# lisää tietokantaan muut vaaditut datat sekä
# luo superuserin sekä käyttäjän, jolla on oikeat oikeudet kantaan.
def setupDjango():
    print('Laitetaan Django käyttökuntoon.\n')
    subprocess.run(["python3", "manage.py", "makemigrations"])
    subprocess.run(["python3", "manage.py", "migrate"])
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "riskiwww.settings")
    import django
    django.setup()
    print('Lisätään kaikki EventTypes tietokantaan.\n')
    from eventsignup.models import EventType
    for x in ['custom', 'muutapahtuma', 'ekskursio', 'vuosijuhlat', 'sitz', 'sitsit']:
        etype = EventType(event_type=x)
        etype.save()
    from django.contrib.auth.models import User
#    from eventsignup.models import EventOwner
    print('Luodaan uusi superuser.')
    uname = input('Anna haluttu käyttäjänimi: ')
    pw = input('Anna salasana: ')
    user = User.objects.create_superuser(uname, 'www-asteriski@utu.fi', pw)
    user.save()
    print('Luodaan uusi käyttäjä, joka voi luoda uusia tapahtumia. Käyttäjätunnus: asteriski')
    name = 'asteriski'
    pw = input('Anna salasana: ')
    user = User.objects.create_user(name, 'asteriski@utu.fi', pw)
    user.save()
    user = User.objects.get(username=name)
    print('Asetetaan käyttäjälle <'+name+'> oikeat käyttöoikeudet.')
    from django.contrib.auth.models import Permission
#    perms=list(Permission.objects.values_list('codename',flat=True))
    for x in list(Permission.objects.values_list('codename', flat=True)):
        if(not ('log' in x or 'group' in x or 'permission' in x or 'user' in x or 'type' in x or 'owner' in x or 'session' in x)):
#            permission=Permission.objects.get(codename=x)
            user.user_permissions.add(Permission.objects.get(codename=x))
    user.save()


# Lataa ja purkaa Bulma css:n tiedostot oikeaan paikkaan.
def setupBulma():
    global bulma
    print('Ladataan ja puretaan Bulma css.\n')
    with urllib.request.urlopen('https://github.com/jgthms/bulma/releases/download/0.7.2/bulma-0.7.2.zip') as response, open('delete_me.zip', 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    with zipfile.ZipFile('./delete_me.zip', 'r') as zipref:
        zipref.extractall('./mybulma/')
    os.unlink('./delete_me.zip')
    shutil.rmtree('./mybulma/__MACOSX/')


def getDBInfo():
    db_name = input('Anna tietokannan nimi: ')
    db_user = input('Anna tietokantaan tarvittava käyttäjätunnus: ')
    db_pw = input('Anna salasana: ')
    db_host = input('Anna tietokantapalvelimen ip osoite: ')
    db_port = input('Anna käytetty portti: ')
    return [db_name, db_user, db_pw, db_host, db_port]


def getSmtpInfo():
    email_host = input('Anna smtp palvelimen nimi: ')
    email_user = input('Anna smtp palvelimen käyttäjänimi (jos tarvitaan): ')
    email_pw = input('Anna salasana (jos tarvitaan): ')
    email_port = input('Anna smtp palvelimen käyttämä portti: ')
    return [email_host, email_user, email_pw, email_port]


# Valmistelee järjestelmätason käyttöympäristön kuntoon ja
# generoi Djangolle tarvittavat konffit.
def setupEnv(rerun):
    if(not rerun):
        print('Asennetaan tarvittavat python moduulit.\n')
        try:
            with open('./requirements.txt', 'r') as f:
                modules = []
                for line in f:
                    modules.append(line.replace('\n', ''))
                for module in modules:
                    subprocess.run(["pip3", "install",  module])
        except IOError:
            print('Tiedosto requirements.txt ei löydy! Skriptin suoritusta ei voi jatkaa. Varmista, että repo on kloonattu kunnolla.\n')
            exit(1)
    from django.core.management.utils import get_random_secret_key
    print('Luodaan tarvittava .env tiedosto.\n')
    forcedInfo = False
    if(rerun):
        oldDBSettings = ''
        oldSmtpSettings = []
        oldUrl = ''
        try:
            with open('./riskiwww/.env', 'r') as f:
                for line in f:
                    if('DATABASE_URL' in line):
                        oldDBSettings = line
                    if('EMAIL' in line):
                        oldSmtpSettings.append(line)
                    if('ALLOWED_HOSTS' in line):
                        oldUrl = line
        except IOError:
            print('Virhe! Vanhaa .env tiedostoa ei löydy. Asetusten uudelleen määrittely on pakollista.\n')
            forcedInfo = True
    with open('./riskiwww/.env', 'w') as f:
        writeDB = False
        writeSmtp = False
        writeHost = False
        url = ''
        f.write('SECRET_KEY='+get_random_secret_key()+'\n')
        f.write('DEBUG=False\n')
        if(forcedInfo or (rerun and input('Uusitaanko url tiedot? [k/e]: ').casefold() == 'k')):
            url = input('Anna url osoite, josta palvelun saa kiinni (eg. url.asteriski.fi) (lisätään allowed host tietoihin): ')
            writeHost = True
        elif(not rerun):
            url = input('Anna url osoite, josta palvelun saa kiinni (eg. url.asteriski.fi) (lisätään allowed host tietoihin): ')
            writeHost = True
        if(writeHost):
            f.write('ALLOWED_HOSTS=.localhost,127.0.0.1,'+url+'\n')
        if(forcedInfo or (rerun and input('Uusitaanko tietokannan tiedot? [k/e]: ').casefold() == 'k')):
            dbInfo = getDBInfo()
            writeDB = True
        elif(not rerun):
            dbInfo = getDBInfo()
            writeDB = True
        if(writeDB):
            f.write("DATABASE_URL={'ENGINE': 'django.db.backends.mysql','NAME': '"+dbInfo[0]+"','USER': '"+dbInfo[1]+"','PASSWORD': '"+dbInfo[2]+"','HOST': '"+dbInfo[3]+"','PORT': '"+dbInfo[4]+"',}}\n")
        f.write('EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend\n')
        if(forcedInfo or (rerun and input('Uusitaanko smtp asetukset? [k/e]: ').casefold() == 'k')):
            smtpInfo = getSmtpInfo()
            writeSmtp = True
        elif(not rerun):
            smtpInfo = getSmtpInfo()
            writeSmtp = True
        if(writeSmtp):
            f.write('EMAIL_HOST='+smtpInfo[0]+'\n')
            if(not (smtpInfo[1] is None)):
                f.write('EMAIL_HOST_PASSWORD='+smtpInfo[1]+'\n')
            if(not(smtpInfo[2] is None)):
                f.write('EMAIL_HOST_USER='+smtpInfo[2]+'\n')
            f.write('EMAIL_PORT='+smtpInfo[3]+'\n')
        if(rerun and not writeDB):
            f.write(oldDBSettings)
            f.write('\n')
        if(rerun and not writeSmtp):
            for line in oldSmtpSettings:
                f.write(line+'\n')
            f.write('\n')
        if(rerun and not writeHost):
            f.write(oldUrl+'\n')
        f.write('SECURE_CONTENT_TYPE_NOSNIFF=True\n')
        f.write('SECURE_BROWSER_XSS_FILTER=True\n')
        f.write('SESSION_COOKIE_SECURE=True\n')
        f.write('CSRF_COOKIE_SECURE=True\n')
        f.write('X_FRAME_OPTIONS=DENY\n')
        f.write('SESSION_COOKIE_SECURE=True\n\n')


# Kääntää css:n valmiiksi käytettävään muotoon.
def setupCss():
    print('Käännetään css.')
    import sass
    path = os.getcwd()
    sass.compile(dirname=(path+"/mybulma/sass/", path+"/static/css/"))


def printEnv():
    with open('./riskiwww/.env', 'r') as f:
        print('.env tiedosto luotiin seuraavilla tiedoilla. Mikäli syötetyissä tiedoissa oli virheitä, aja skripti uudestaan: python3 '+sys.argv[0]+' -r')
        for line in f:
            print(line)


if __name__ == '__main__':
    if(len(sys.argv) > 1):
        if(sys.argv[1] == '-r'):
            setupEnv(True)
            printEnv()
            exit()
        else:
            exit()
    else:
        setupEnv(False)
        setupDjango()
        setupBulma()
        setupCss()
        printEnv()
