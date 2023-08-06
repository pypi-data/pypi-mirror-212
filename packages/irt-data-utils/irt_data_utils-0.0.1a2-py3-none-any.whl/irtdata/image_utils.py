from PIL import Image
import cv2
import matplotlib.pyplot as plt
import seaborn as sns

def crop_image(image_path,crop_size):
    #cropping images
    img = Image.open(image_path) ## 打开chess.png文件，并赋值给img
    region = img.crop(crop_size)## 0,0表示要裁剪的位置的左上角坐标，50,50表示右下角。
    # region_resized=region.resize((64,64))
    return region

def crop_image_optical(image_path, crop_size,resize_size,save_path=None):
    # cropping images
    img = Image.open(image_path)  ## 打开chess.png文件，并赋值给img
    region = img.crop(crop_size)  ## 0,0表示要裁剪的位置的左上角坐标，50,50表示右下角。
    region = region.resize(resize_size)
    # region_resized=region.resize((64,64))
    # cropped_image=crop_image(optical_path)
    if save_path!=None:
        region.save(save_path)
    return region

def resize_image(image_path, new_size, target_path):
    img = Image.open(image_path)  ## 打开chess.png文件，并赋值给img
    region = img.resize(new_size)
    region.save(target_path)


def merge_image(img_path1, image_path2,alpha=0.3):
    img = Image.open(img_path1)
    img2 = Image.open(image_path2)
    merge = Image.blend(img, img2, alpha)
    return merge


def merge_image_blocks(im1, im2, alpha=0.1):
    merge = Image.blend(im1, im2, alpha)
    return merge

def crop_image_square(image_path,square):
    #cropping images
    img = Image.open(image_path) ## 打开chess.png文件，并赋值给img
    region = img.crop((0,0,square,square))## 0,0表示要裁剪的位置的左上角坐标，50,50表示右下角。
    # region_resized=region.resize((64,64))
    return region

def write_thermal(thermal,saved_path):
    f_out=open(saved_path,'w',encoding='utf-8')
    for m in thermal:
        line=[]
        for l in m:
            line.append(str(l))
        f_out.write(','.join(line)+'\n')
    f_out.close()

def get_thermal_data_from_image(image_path,save_image_path=None,save_csv_path=None,dpi=300,base_temp=22):
    img = cv2.imread(image_path, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)

    # cv2.imshow('title',img)
    # print(img[10, 10])
    # print(img)

    # Get image dimensions
    height, width = img.shape
    # print(img.shape)
    # Loop through each pixel and get the pixel values

    color = cv2.applyColorMap(img, cv2.COLORMAP_JET)
    color1 = Image.fromarray(color.astype('uint8')).convert('RGB')

    max_value = -1
    min_value = 1000

    for y in range(height):
        for x in range(width):
            pixel = img[y, x]
            if pixel > max_value:
                max_value = pixel
            if pixel < min_value:
                min_value = pixel
    # print(min_value, max_value)

    temps = []
    for y in range(height):
        list_t = []
        for x in range(width):
            pixel = img[y, x]
            temp = base_temp + (pixel - min_value) / (max_value - min_value)
            list_t.append(round(temp, 4))
        temps.append(list_t)

    # sns.set(rc={"figure.figsize": (6, 6)})

    ax = sns.heatmap(temps,
                     xticklabels=False,  # remove the labels
                     yticklabels=False,
                     cbar=False,
                     cmap='inferno'
                     )

    plt.tight_layout()

    # plt.show()
    if save_image_path!=None:
        plt.savefig(save_image_path, dpi=dpi, bbox_inches='tight', pad_inches=0)
    if save_csv_path!=None:
        write_thermal(temps, saved_path=save_csv_path)
    return temps
