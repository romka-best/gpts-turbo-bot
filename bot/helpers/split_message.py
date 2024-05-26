def split_message(message_content, chunk_size=4096):
    return [message_content[i:i + chunk_size] for i in range(0, len(message_content), chunk_size)]
