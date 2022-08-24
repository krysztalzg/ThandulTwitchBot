def handle_add_command(context, database):
    message = context.message
    message.content = message.content.replace('!add', '')
    if message.author.color == '':
        message.author.color = '#000000'
    try:
        database.execute(
            'INSERT INTO todo (id, server, username, color, task) VALUES (?, ?, ?, ?, ?)',
            (str(message.id), str(message.channel.name.lower()), str(message.author.display_name), str(message.author.color), str(message.content)),
        )
        database.commit()
        print(f'Added {message.content}[{message.id}] from {message.author.display_name}[{message.author.color}] on channel {message.channel.name.lower()}')
    except database.IntegrityError:
        return "Task is already added."
