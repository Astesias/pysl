# from MyQR import myqr    

from pysl import cmd
import os

def qrcode(word,pic=None,save="二维码.png"):
    from PIL import Image as img 
    # word="https://www.baidu.com"
    # save="二维码.png"
    # pic=r"D:\Desktop\Image\6945ab7f7ef0153745264d990cc3274.png"

    # myqr.run(                        
    #         words = "https://www.baidu.com",         
    #         level='H',
    #         picture = r"D:\Desktop\Image\6945ab7f7ef0153745264d990cc3274.png",
    #         colorized=True,                             
    #         save_name=save,
    #         )

    if pic:
        cmd(f'myqr {word} -v 4 -p {pic} -d {os.getcwd()} -n {save} -c')
    else:
        cmd(f'myqr {word} -v 4 -d {os.getcwd()} -n {save} ')
    
    i=img.open(save)
    i.resize((200,200),img.ANTIALIAS)
    i.show()
