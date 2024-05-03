def word_wrap(string, n_chars=72):
    # Wrap a string at the next space after n_chars
    if len(string) < n_chars:
        return string
    else:
        return string[:n_chars].rsplit(' ', 1)[0] + '\n' + word_wrap(string[len(string[:n_chars].rsplit(' ', 1)[0])+1:], n_chars)


def process_title(title):
    try:
        title = title.split('# ')[1]
        title = title.split('<a')[0]
    except Expection as e:
        logging.error(f'Failed to process {title}: {e}')
    finally:
        return title
    
