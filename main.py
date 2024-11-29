import configparser
config = configparser.ConfigParser()
config.read(seting.ini)
vk_token = config['Tokens']['vk_tokens']
