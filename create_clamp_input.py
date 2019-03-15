from note_cleaning.pitt_handler import PittHandler

if __name__ == '__main__':
    handler = PittHandler()
    handler.split_reports('../data/raw/pitt.txt')
    outdir = '../data/processed/pitt_cleaned'
    handler.to_files(outdir)
