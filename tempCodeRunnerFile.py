# reply as user - functionality for bot, when message is .. and is in reply to someone
    if message.content == "..":
        if not message.reference:
            await message.reply("You need to reply to someone to use this command")
            return
        reference = message.reference.resolved
        
        # add the name of sender in front of message, to make it clear for chatbot who is sending the message
        reference.content = f"{reference.author.global_name} says {reference.content}"
        await bot_reply(message=reference, user_to_mention=message.author.mention)