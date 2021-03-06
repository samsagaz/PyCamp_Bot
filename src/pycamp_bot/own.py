from telegram.ext import (ConversationHandler, CommandHandler, MessageHandler,
                          Filters)

from pycamp_bot.models import (Pycampista, Project, ProjectOwner, Slot, Vote,
                               Wizard)

OWNING = range(1)


def own(bot, update):
    lista_proyectos = [p.name for p in Project.select()]
    dic_proyectos = dict(enumerate(lista_proyectos))
    bot.send_message(
        chat_id=update.message.chat_id,
        text="¿A qué proyecto querés agregarte como responsable? (Dar número)"
    )
    for k, v in dic_proyectos.items():
        bot.send_message(
            chat_id=update.message.chat_id,
            text="{}: {}".format(k, v)

        )
    bot.send_message(
        chat_id=update.message.chat_id,
        text="-"*77

    )
    return OWNING


def owning(bot, update):
    '''Dialog to set project responsable'''
    username = update.message.from_user.username
    text = update.message.text
    chat_id = update.message.chat_id

    lista_proyectos = [p.name for p in Project.select()]
    dic_proyectos = dict(enumerate(lista_proyectos))

    project_name = dic_proyectos[int(text)]
    new_project = Project.get(Project.name == project_name)

    user = Pycampista.get_or_create(username=username, chat_id=chat_id)[0]
    new_project.owner = user
    new_project.save()

    bot.send_message(
        chat_id=update.message.chat_id,
        text="Perfecto. Chauchi"
    )


def cancel(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Has cancelado la carga del proyecto"
        )
    return ConversationHandler.END


own_project_handler = ConversationHandler(
       entry_points=[CommandHandler('ownear', own)],
       states={
           OWNING: [MessageHandler(Filters.text, owning)],
       },
       fallbacks=[CommandHandler('cancel', cancel)]
   )
