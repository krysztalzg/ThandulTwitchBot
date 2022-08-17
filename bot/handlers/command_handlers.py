def add_command(context):
    message = context.message
    print(f'[{message.timestamp}] {message.author.display_name}: {message.content}')
