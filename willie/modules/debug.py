# coding=utf-8

from willie.module import commands, example
import platform, sys, time
from os import path
import urllib, json

@commands('privs')
def privileges(bot, trigger):
    if trigger.group(2):
        try:
            bot.say(str(bot.privileges[trigger.group(2)]))
        except Exception:
            if bot.config.lang == 'ca':
                bot.reply("Canal desconegut.")
            elif bot.config.lang == 'es':
                bot.reply("Canal desconocido.")
            else:
                bot.reply("Channel not found.")
    else:
        bot.say(str(bot.privileges))

@commands('admins')
def admins(bot, trigger):
    owner = bot.config.core.owner
    admins = bot.config.core.get_list('admins')
    if len(admins) == 0:
        if bot.config.lang == 'ca':
            bot.say("\x02Owner:\x02 "+owner+" - No tinc administradors.")
        elif bot.config.lang == 'es':
            bot.say("\x02Owner:\x02 "+owner+" - No tengo administradores.")
        else:
            bot.say("\x02Owner:\x02 "+owner+" - I don't have any admins.")
    else:
        bot.say("\x02Owner:\x02 "+owner+" - \x02Admins:\x02 "+", ".join(admins))

def git_info():
    repo = path.join(path.dirname(path.dirname(path.dirname(__file__))), '.git')
    head = path.join(repo, 'HEAD')
    if path.isfile(head):
        with open(head) as h:
            head_loc = h.readline()[5:-1]  # strip ref: and \n
        head_file = path.join(repo, head_loc)
        if path.isfile(head_file):
            with open(head_file) as h:
                sha = h.readline()
                if sha:
                    return sha
                else:
                    return ''

def get_latest_version():
    web = urllib.urlopen("https://api.github.com/repos/Worldev/Granota/releases/latest")
    data = json.load(web)
    n = data['tag_name']
    url = data['html_url']
    return n, url

@commands('version', 'versio')
def version(bot, trigger):
    version = 'v2.8'
    if platform.system() == 'Linux':
        osver = ("%s %s" % (platform.linux_distribution()[0], platform.linux_distribution()[1]))
    elif platform.system() == 'Windows':
        osver = ("%s %s" % (platform.system(), platform.release()))
    else:
        osver = ("some OS which is not Linux or Windows")
    pyver = sys.version.split()[0]
    commit = git_info()
    latestver, latesturl = get_latest_version()
    if latestver != version:
        if bot.config.lang == 'ca':
            latestmsg = u"L'última versió estable disponible de Grantota és \x02%s\x02 (%s)." % (latestver, latesturl)
        elif bot.config.lang == 'es':
            latestmsg = u"La última versión estable disponible de Granota es \x02%s\x02 (%s)." % (latestver, latesturl)
        else:
            latestmsg = u"The lastest stable version of Granota available is \x02%s\x02 (%s)." % (latestver, latesturl)
    else:
        if bot.config.lang == 'ca':
            latestmsg = u"Estic utilitzant l'última versió estable de Granota."
        elif bot.config.lang == 'es':
            latestmsg = u"Estoy usando la última versión estable de Granota."
        else:
            latestmsg = u"I'm using the latest stable version of Granota."
    if bot.config.lang == ('ca', 'es'):
        unstable = 'inestable'
        stable = 'estable'
    else:
        unstable = 'unstable'
        stable = 'stable'
    if commit == '' or commit == None:
        commitinfo = ' (\x0303%s\x03)' % stable
    else:
        commitinfo = ' (\x0304%s\x03, commit %s)' % (unstable, commit)
        latestmsg = ''
    if bot.config.lang == 'ca':
        bot.say(u"Sóc \x02Granota %s\x02%s, en el sistema operatiu %s i utilitzant Python %s. %s" % (version, commitinfo, osver, pyver, latestmsg))
    elif bot.config.lang == 'es':
        bot.say(u"Soy \x02Granota %s\x02%s, en el sistema operativo %s y usando Python %s. %s" % (version, commitinfo, osver, pyver, latestmsg))
    else:
        bot.say(u"I'm \x02Granota %s\x02%s, on %s and using Python %s. %s" % (version, commitinfo, osver, pyver, latestmsg))
    
    if bot.config.lang == 'ca':
        update_msg = u"Estic obsolet! La meva versió actual és la \x02%s\x02 però l'última versió estable és \x02%s\x02! " + \
        u"Descarregueu l'última versió amb alguns errors corregits i noves funcionalitats aquí: %s"
    elif bot.config.lang == 'es':
        update_msg = "Estoy desfasado! Mi versión actual es la \x02%s\x02 pero la última versión estable es \x02%s\x02! " + \
        "Por favor, descarga la última versión con algunos errores corregidos y nuevas funcionalidades aquí: %s"   
    else:        
        update_msg = "I'm outdated! My current version is \x02%s\x02 but the latest stable version is \x02%s\x02! " + \
        "Please download the last version here with some bugs fixed and nice features added: %s"
    if latestver != version:
        bot.msg(bot.config.owner.split('@')[0], update_msg % (version, latestver, latesturl))
    
@commands('debug_print')
def debug_print(bot, trigger):
    version(bot, trigger)
    admins(bot, trigger)
    privileges(bot, trigger)

@commands('raiseException', 'causeProblems', 'giveError')
def cause_problems(bot, trigger):
    raise Exception("Problems were caused on command.")
