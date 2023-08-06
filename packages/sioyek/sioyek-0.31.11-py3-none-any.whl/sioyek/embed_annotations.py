import sys
from .sioyek import Sioyek, clean_path

if __name__ == '__main__':
    SIOYEK_PATH = clean_path(sys.argv[1])
    LOCAL_DATABASE_PATH = clean_path(sys.argv[2])
    SHARED_DATABASE_PATH = clean_path(sys.argv[3])
    FILE_PATH = clean_path(sys.argv[4])

    if len(sys.argv) > 5:
        embed_method = sys.argv[5] 
    else:
        embed_method = 'custom'


    sioyek = Sioyek(SIOYEK_PATH, LOCAL_DATABASE_PATH, SHARED_DATABASE_PATH)
    sioyek.set_highlight_embed_method(embed_method)
    document = sioyek.get_document(FILE_PATH)
    document.embed_new_annotations(save=True)
    document.close()
    sioyek.reload()
    sioyek.close()
