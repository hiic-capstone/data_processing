from getpass import getpass

from note_cleaning.pitt_handler import PittHandler

if __name__ == '__main__':
    user = 'root'
    password = getpass(f'Password for {user}: ')
    params = {'user': user, 'password': password,
              'db': 'derived', 'host': 'localhost'}

    handler = PittHandler()
    handler.split_reports('../data/raw/pitt.txt')
    outdir = '../data/clamp_input/pitt_cleaned'
    handler.to_files(outdir)
    handler.meta_to_db(params=params, table='metadata', drop=True)
