import traceback

async def handle_add_command(context, database):
    message = context.message
    message.content = message.content.replace('!add ', '')
    username = message.author.display_name
    if message.author.color == '':
        message.author.color = '#000000'
    try:
        database.execute(
            'INSERT INTO todo (id, server, username, color, task) VALUES (?, ?, ?, ?, ?)',
            (str(message.id), str(message.channel.name.lower()), str(username), str(message.author.color), str(message.content)),
        )
        database.commit()
        await message.channel.send(f'Added new task from @{username}!')
        # print(f'Added new task from @{username}!')
        return
    except :
        await message.channel.send(f"@{username},  your task couldn't be added. Please try again later.")
        # print(f"@{username}, your task couldn't be added. Please try again later.")
        traceback.print_exc()
        return

async def handle_done_command(context, database):
    message = context.message
    message.content = message.content.replace('!done ', '')
    channel = message.channel.name.lower()
    username = message.author.display_name

    try:
        user_tasks = database.execute(f'SELECT * FROM todo where server = "{channel.lower()}" AND done = FALSE AND username = "{username}"').fetchall()

        try:
            task_index = int(message.content) - 1
            _mark_task_as_done(user_tasks[task_index], database)
            await message.channel.send(f'🎉 @{username} finished their task 🎉')
            # print(f'🎉 @{username} finished their task 🎉')
            return
        except:
            pass

        if len(user_tasks) < 1:
            return # NO TASKS

        elif len(user_tasks) == 1:
            _mark_task_as_done(user_tasks[0], database)
            await message.channel.send(f'🎉 @{username} finished their task 🎉')
            # print(f'🎉 @{username} finished their task 🎉')
        else:
            indexed_tasks = [f'{it + 1} - {task[4]}' for it, task in enumerate(user_tasks)]
            await message.channel.send(f'@{username}, you have more ongoing tasks, select which to complete with "!done x", where x is the number of a task: {", ".join(indexed_tasks)}.')
            # print(f'@{username}, you have more ongoing tasks, select which to complete with "!done x", where x is the number of a task: {", ".join(indexed_tasks)}.')
            return
    except:
        await message.channel.send(f"@{username}, your task couldn't be marked as finished. Please try again later.")
        # print(f"@{username}, your task couldn't be marked as finished. Please try again later.")
        traceback.print_exc()
        return

async def handle_clear_command(context, database):
    message = context.message
    channel = message.channel.name.lower()
    username = message.author.display_name

    if channel != username.lower():
        # print(f"{username} tried to clear list as not channel owner.")
        return

    try:
        database.execute(f'UPDATE todo SET done = TRUE WHERE server = "{channel}"')
        database.commit()
    except:
        await message.channel.send(f"@{username}, list of tasks couldn't be cleared. Please try again later.")
        # print(f"@{username}, list of tasks couldn't be cleared. Please try again later.")
        traceback.print_exc()
        return

def _mark_task_as_done(task, database):
    try:
        database.execute(f'UPDATE todo SET done = TRUE WHERE id = "{task[0]}"')
        database.commit()
    except:
        traceback.print_exc()
        raise Exception('Failed to set task as finished')
