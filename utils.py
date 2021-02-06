import os
import shutil
import git
import numpy as np
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw

resolutions = [
    {'w': 52, 'h': 52},
    {'w': 80, 'h': 80},
    {'w': 108, 'h': 108},
    {'w': 119,'h': 119},
    {'w': 153, 'h': 152},
    {'w': 183, 'h': 183},
    {'w': 193,'h': 193},
    {'w': 258,'h': 258},
    {'w': 308,'h': 308},
    {'w': 308,'h': 309},
    {'w': 408, 'h': 408}
]
dirs = ["ad", "0c", "d0", "74", "13", "03", "66", "84", "5f", "56", "50"]
names = [
    "ad16ccdc-975e-4393-ae7b-8ac79c3795f2.png",
    "0cbb3dbb-2a85-42a5-be21-9839611e5af7.png",
    "d0c676e4-0956-4a03-90af-fee028cfabe4.png",
    "74237057-2880-4e1f-8a78-6d8ef00a1f5f.png",
    "132ded82-3e39-4e2e-bc34-fc934870f84c.png",
    "03c33f55-5932-4ff7-896b-814ba3a8edb8.png",
    "665a0ec9-6c43-4858-974c-025514f2a0e7.png",
    "84bc9d40-83d0-480c-b46a-3ef59e603e14.png",
    "5fa0264d-acbf-4a7b-8923-c106ec3b9215.png",
    "564ba620-6a55-4cbe-a5a6-6fa3edd80151.png",
    "5035266c-8df3-4236-8d82-a375e97a0d9c.png"
]

def save_img(uuid, data):
    path = 'tmp/'+uuid+'/'
    img_dirs = []
    imgs = []

    os.makedirs(path, exist_ok=True)

    for name in data:
        save_path = path+name
        img_dirs.append(save_path)
        os.makedirs(save_path, exist_ok=True)

    for index, file in enumerate(data.values()):
        filename = secure_filename(file.filename+".png")
        save_path = os.path.join(img_dirs[index], filename)
        file.save(save_path)
        imgs.append(save_path)
    
    process_img(path, imgs, img_dirs)
    
    return path

def process_img(path, imgs, img_dirs):
    asset_path = path+'raw-assets'
    os.makedirs(asset_path)
    for index, path in enumerate(imgs):
        save_path = asset_path + '/' +dirs[index]
        os.makedirs(save_path)
        resolution = resolutions[index]
        img = Image.open(path).convert("RGB").resize((resolution['w'], resolution['h']))
        npImage = np.array(img)
        h, w = img.size

        alpha = Image.new('L', img.size,0)
        draw = ImageDraw.Draw(alpha)
        draw.pieslice([0,0,h,w],0,360,fill=255)

        npAlpha=np.array(alpha)

        npImage=np.dstack((npImage, npAlpha))

        Image.fromarray(npImage).save(save_path+'/'+names[index])
    for path in img_dirs:
        shutil.rmtree(path)


def make_game(path):
    try:
        git.Repo.clone_from("https://github.com/liyupi/daxigua", path+'daxigua')
        git_path = path+'daxigua/'

        for index, name in enumerate(dirs):
            os.remove(git_path+'res/raw-assets/'+name+"/"+names[index])
            shutil.move(path+'raw-assets/'+name+"/"+names[index], git_path+'res/raw-assets/'+name+"/"+names[index])
    except Exception as e:
        print(e)
        return False
    return True