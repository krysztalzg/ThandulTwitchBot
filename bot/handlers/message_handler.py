def handle_message(message):
    if message.echo:
        return

    print(f'[{message.timestamp}] {message.author.display_name}: {message.content}')
