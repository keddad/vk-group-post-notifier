from tinydb import TinyDB, Query
import utils

db = TinyDB("db.json")


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hi. To subscribe onto commmunity's updates, run \n/addgroup vk.com/someamazinggroup"
    )


def onerror(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Shit happens, errors too. Debug info: \n{context.error}"
    )


def addgroup(update, context):
    text = update.message.text

    try:
        link = text.split()[1]
    except IndexError:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="This link is wrong. Send me a link like vk.com/someamazinggroup"
        )
        return

    if not utils.is_valid_link(link):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="This link is wrong. Send me a link like vk.com/someamazinggroup"
        )
        return

    if not utils.is_community_open(link):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="This community is closed or have no posts."
                 " I can only work with open communities with at least one post"
        )
        return

    link = "vk.com/" + link.split("/")[-1]
    link = link.split("?")[0]

    Group = Query()
    if db.contains(Group.link == link):
        group = db.get(Group.link == link)

        new_users_list = group["users"]

        if update.effective_chat.id not in new_users_list:
            new_users_list.append(update.effective_chat.id)
            group["users"] = new_users_list
            db.write_back([group])

        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="You are already subscribed to this group"
            )
            return

    else:
        db.insert(
            {
                "link": link,
                "users": [update.effective_chat.id],
                "last_post_id": utils.get_current_latest_post(link)
            }
        )

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"You are now subscribed to the updates of group {link}"
    )


def removegroup(update, context):
    text = update.message.text

    try:
        link = text.split()[1]
    except IndexError:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="This link is wrong. Send me a link like vk.com/someamazinggroup"
        )
        return

    if not utils.is_valid_link(link):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="This link is wrong. Send me a link like vk.com/someamazinggroup"
        )
        return

    link = "vk.com/" + link.split("/")[-1]

    Group = Query()
    if not db.contains(Group.link == link):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="There are no such group"
        )
        return

    document = db.get(Group.link == link)

    if not update.effective_chat.id in document["users"]:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You are not subscribed to this group"
        )
        return

    document["users"].remove(update.effective_chat.id)

    if len(document["users"]) == 0:
        db.remove(doc_ids=[document.doc_id])
    else:
        db.write_back([document])

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Group {link} removed"
    )


def checkupdates(bot):
    for document in iter(db):
        current_post_id = utils.get_current_latest_post(document["link"])

        if current_post_id != document["last_post_id"]:
            for uid in document["users"]:
                bot.send_message(
                    chat_id=uid,
                    text=f"New post in group {document['link']}"
                )

            document["last_post_id"] = current_post_id
            db.write_back([document])
