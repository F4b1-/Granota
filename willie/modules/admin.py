# coding=utf-8

import willie
import willie.module
from willie.module import commands, rule, event, NOLIMIT
from willie import module
import sys

def configure(config):
    """
    | [admin] | example | purpose |
    | -------- | ------- | ------- |
    | hold_ground | False | Auto re-join on kick |
    """
    config.add_option('admin', 'hold_ground', u"Enable auto-rejoin on kick?")

@willie.module.commands('join', 'entra')
@willie.module.priority('low')
def join(bot, trigger):
    # Can only be done in privmsg by an admin
    if trigger.sender.startswith('#'):
        if bot.config.lang == 'en':
            bot.reply(u"Only works in private")
        if bot.config.lang == 'es':
            bot.reply(u"Solo funciona en privado")
        elif bot.config.lang == 'ca':
            bot.reply(u"Nomes funciona en privat")
        return

    if trigger.admin:
        channel, key = trigger.group(2), trigger.group(3)
        if not channel:
            return
        elif not key:
            bot.join(channel)
        else:
            bot.join(channel, key)
    if not trigger.admin:
        if bot.config.lang == 'en':
            bot.reply(u"You need admin rights.")
        if bot.config.lang == 'ca':
            bot.reply(u"No ets admin")
        elif bot.config.lang == 'es':
            bot.reply(u"No eres admin")
        return

@willie.module.commands('part', 'surt', 'sal')
@willie.module.priority('low')
def part(bot, trigger):
    if trigger.sender.startswith('#'):
        return
    if not trigger.admin:
        if bot.config.lang == 'en':
            bot.reply(u"You don't have admin rights")
        elif bot.config.lang == 'es':
            bot.reply(u"No eres admin")
        else:
            bot.reply(u"No ets admin")
        return
    # Can only be done in privmsg by an admin

    channel, _sep, part_msg = trigger.group(2).partition(' ')
    if part_msg:
        bot.part(channel, part_msg)
    else:
        bot.part(channel)

@willie.module.commands('quit')
@willie.module.priority('low')
def quit(bot, trigger):
    if trigger.sender.startswith('#'):
        return
    if not trigger.owner:
        return
    # Can only be done in privmsg by the owner

    quit_message = trigger.group(2)
    if bot.config.lang == 'es':
        bot.quit(quit_message + " [comando ejecutado por %s]" % trigger.nick)
    elif bot.config.lang == 'ca':
        bot.quit(quit_message + " [ordre executada per %s]" % trigger.nick)
    else:
        bot.quit(quit_message + " [by %s]" % trigger.nick)
    sys.exit()

@willie.module.commands('msg')
@willie.module.priority('low')
def msg(bot, trigger):
    if trigger.sender.startswith('#'):
        return
    if not trigger.admin:
        return
    try:
        channel, _sep, message = trigger.group(2).partition(' ')
        message = message.strip()
        if not channel or not message:
            return
        bot.msg(channel, message)
    except AttributeError:
        if bot.config.lang == "ca":
            message = "No has posat missatge!"
        elif bot.config.lang == "es":
            message = u"No has introducido ningún mensaje!"
        else:
            message = "You have not entered a message!"
        bot.reply(message)

@willie.module.commands('me')
@willie.module.priority('low')
def me(bot, trigger):
    if trigger.sender.startswith('#'):
        return
    if not trigger.admin:
        return

    channel, _sep, action = trigger.group(2).partition(' ')
    action = action.strip()
    if not channel or not action:
        return

    msg = '\x01ACTION %s\x01' % action
    bot.msg(channel, msg)

@willie.module.event('INVITE')
@willie.module.rule('.*')
@willie.module.priority('low')
def invite_join(bot, trigger):
    if not trigger.admin:
        return
    bot.join(trigger.args[1])


@willie.module.event('KICK')
@willie.module.rule(r'.*')
@willie.module.priority('low')
def hold_ground(bot, trigger):
    """
    This function monitors all kicks across all channels granota is in. If it
    detects that it is the one kicked it'll automatically join that channel.

    WARNING: This may not be needed and could cause problems if willie becomes
    annoying. Please use this with caution.
    """
    if bot.config.has_section('admin') and bot.config.admin.hold_ground:
        channel = trigger.sender
        if trigger.args[1] == bot.nick:
            bot.join(channel)


@willie.module.commands('mode')
@willie.module.priority('low')
def mode(bot, trigger):
    if trigger.sender.startswith('#'):
        return
    if not trigger.admin:
        return

    mode = trigger.group(3)
    bot.write(('MODE ', bot.nick + '' + mode))


@willie.module.commands('set')
@willie.module.example('.set core.owner nick')
def set_config(bot, trigger):
    if trigger.sender.startswith('#'):
        if bot.config.lang == 'ca':
            bot.reply("Només funciona en un missatge privat.")
        elif bot.config.lang == 'es':
            bot.reply("Solo en mensaje privado.")
        else:
            bot.reply("Private message only.")
        return
    if not trigger.admin:
        if bot.config.lang == 'ca':
            bot.reply("Necessites ser administrador del bot.")
        elif bot.config.lang == 'es':
            bot.reply("Necesitas ser administrador del bot.")
        else:
            bot.reply("You are not bot admin.")
        return

    # Get section and option from first argument.
    arg1 = trigger.group(3).split('.')
    if len(arg1) == 1:
        section, option = "core", arg1[0]
    elif len(arg1) == 2:
        section, option = arg1
    else:
        if bot.config.lang == 'ca':
            bot.reply(u"Ús: .set secció.opció nou valor")
        elif bot.config.lang == 'es':
            bot.reply(u"Uso: .set sección.opción nuevo valor")
        else:
            bot.reply(u"Use: .set section.option new value")
        return

    # Display current value if no value is given.
    value = trigger.group(4)
    if not value:
        if not bot.config.has_option(section, option):
            if bot.config.lang == 'ca':
                bot.reply("L'opcio %s.%s no existeix." % (section, option))
            elif bot.config.lang == 'es':
                bot.reply("La opcion %s.%s no existe." % (section, option))
            else:
                bot.reply("Option %s.%s does not exist." % (section, option))
            return
        # Except if the option looks like a password. Censor those to stop them
        # from being put on log files.
        if option.endswith("password") or option.endswith("pass"):
            if bot.config.lang == 'ca':
                value = "(contrasenya censurda)"
            elif bot.config.lang == 'es':
                value = "(contraseña censurda)"
            else:
                value = "(password censored)"
        else:
            value = getattr(getattr(bot.config, section), option)
        if not isinstance(value, basestring):
            finalvalue = ",".join(value)
        else:
            finalvalue = value
        bot.say("\x02%s.%s\x02: %s" % (section, option, finalvalue))
        return

    # Otherwise, set the value to one given as argument 2.
    setattr(getattr(bot.config, section), option, value)


@willie.module.commands('save', 'guardar', 'desa', 'desar')
@willie.module.example('.save')
def save_config(bot, trigger):
    if trigger.sender.startswith('#'):
        return
    if not trigger.admin:
        return
    if bot.config.lang == 'ca':
        bot.say(u"Nova configuracio guardada. Pot ser que necessitis reiniciar-me perque tingui efecte.")
    elif bot.config.lang == 'es':
        bot.say(u"Nueva configuracion guardada. Quizas tendras que reiniciarme para que tenga efecto.")
    else:
        bot.say(u"New configuration saved. Maybe you will have to reboot me to apply the changes.")
    bot.config.save()

@commands('nick', 'nom', 'nombre')
def nick(bot, trigger):
    if trigger.admin:
        bot.write(("NICK", trigger.group(2)))
        if trigger.group(2) == bot.config.nick:
            return
        bot.msg("NickServ", "GROUP") # Tries to automatically group de nickname
        if bot.config.lang == 'ca':
            msg = (u"He intentat agrupar el nou nick '%s' al meu compte del NickServ. " +
                    u"Si no estic registrat o identificat, l'ordre no haurà funcionat. " +
                    u"Si la xarxa IRC no disposa de serveis, o el servei de nicks no és 'NickServ', " +
                    u"l'ordre tampoc haurà funcionat.")
        elif bot.config.lang == 'es':
            msg = (u"He intentado agrupar mi nuevo nick '%s' a mi cuenta de NickServ. " +
                    u"Si no estoy registrado o identificado, el comando no habrá funcionado. " +
                    u"Si la red IRC no dispone de servicios, o el servicio de nicks no es 'NickServ', " +
                    u"el comando tampoco habrá funcionado.")
        else:
            msg = ("I tried to group the new nickname '%s' to my NickServ account. " +
                    "If I'm not registered or identified with NickServ, the command have not worked. " +
                    "If the network does not have services, or the nick service is not 'NickServ', " +
                    "the command haven't worked neither.")
        bot.msg(trigger.nick,  msg % trigger.group(2))
        return
    if not trigger.admin:
        return
    
@event('PRIVMSG')
@rule('(.*)')
def pm_tell_owner(bot, trigger):
    if trigger.sender.startswith("#"):
        return
    if trigger.owner or trigger.admin:
        return
    bot.msg(bot.config.owner, "<%s> %s" % (trigger.nick, trigger.group(0)))
    for i in bot.config.admins.split(","):
        bot.msg(i, "<%s> %s" % (trigger.nick, trigger.group(0)))
    return

@commands('configchan')
def add_chansection(bot, trigger):
    if not trigger.admin:
        return
    if not trigger.group(2):
        if bot.config.lang == 'ca':
            bot.reply(u"Ús: .configchan #canal")
        elif bot.config.lang == 'es':
            bot.reply(u"Uso: .configchan #canal")
        else:
            bot.reply(u"Use: .configchan #channel")
        return
    bot.say("blah")
    bot.say(str(bot.config.add_section(trigger.group(2).replace('#', ''))))
    setattr(getattr(bot.config, 'neomahler'), 'ops', 'testttt')
    bot.say("Done")
    return NOLIMIT
    
if __name__ == '__main__':
    print __doc__.strip()
