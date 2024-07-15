#from heic2png import HEIC2PNG
from os import listdir
from os.path import isfile, join, exists
import re
import concurrent.futures
from PIL import Image
import pillow_heif
from tqdm import tqdm

def convert_img(path : str, pbar):
    if not exists(path.split('.')[0] + '.png'):
        img = Image.open(path)
        img.save(path.split('.')[0] + '.png', format='PNG')
    else:
        print(f'File {path} already exists.')
    pbar.update(1)
    #try:
        #heic_img = HEIC2PNG(path, quality=50)
        #heic_img.save()   
    #except FileExistsError:
        #print(f'File {path} already exists.')


def convert_images(folder_path : str):
    onlyfiles = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
    
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=3)

    pillow_heif.register_heif_opener()

    pbar = tqdm(total=len(onlyfiles))

    for file in onlyfiles:
        if re.search('.HEIC', file) != None:
            pool.submit(convert_img, join(folder_path, file), pbar)
            #convert_img(join(folder_path,file))
        else:
            pbar.update(1)
    pool.shutdown(wait=True)

if __name__ == '__main__':
    path = input('Caminho das imagens: ')
    convert_images(path)