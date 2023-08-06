import os

import flyr
import matplotlib.pyplot as plt
import seaborn as sns

def extract_temperature(flir_path,save_csv_path=None):
    # extract temperature information
    thermogram = flyr.unpack(flir_path)
    # thermal = thermogram.kelvin  # As kelvin
    thermal = thermogram.celsius  # As celsius
    # thermal = thermogram.fahrenheit  # As fahrenheit
    # print(thermal)
    # print(f'width:{len(thermal[0])},height:{len(thermal)}')
    if save_csv_path!=None:
        f_out = open(save_csv_path, 'w', encoding='utf-8')
        for m in thermal:
            line = []
            for l in m:
                line.append(str(l))
            f_out.write(','.join(line) + '\n')
        f_out.close()
    return thermal

# show heatmap of temperature information
def read_infrared_data(csv_path):
  lines = open(csv_path, "r", encoding='utf-8')
  data = []
  for line in lines:
    vs = line.strip().split(",")
    row = [float(v) for v in vs]
    data.append(row)
  return data

def get_heatmap(csv_path,show=False,save_image_path=None,dpi=300,cmap='inferno',figure_size=(3,4)):
    temp_data = read_infrared_data(csv_path)

    sns.set(rc={"figure.figsize": figure_size})

    # print(len(temp_data), len(temp_data[0]))
    ax = sns.heatmap(temp_data,
                     xticklabels=False,  # remove the labels
                     yticklabels=False,
                     cbar=False,
                     cmap=cmap
                     )

    plt.tight_layout()

    if show:
        plt.show()

    if save_image_path!=None:
        plt.savefig(save_image_path, dpi=dpi, bbox_inches='tight', pad_inches=0)
    return temp_data


def get_optical_image(flir_path,save_image_path=None):
    thermogram = flyr.unpack(flir_path)
    optical_arr = thermogram.optical  # Also works
    if save_image_path!=None:
        thermogram.optical_pil.save(save_image_path)
    return optical_arr

def render_thermal_with_colorsets(flir_path,custom_palettes=None,min_v=27.1,max_v=35.6,unit="celsius",display=False,save_root_path=None):
    palettes = ["turbo", "cividis", "inferno", "grayscale", "hot"]
    if custom_palettes!=None:
        palettes=custom_palettes
    renders = []
    thermogram = flyr.unpack(flir_path)
    for p in palettes:
        # The below call returns a Pillow Image object.
        # A sibling method called `render` returns a numpy array.
        render = thermogram.render_pil(
            min_v=min_v,
            max_v=max_v,
            unit=unit,
            palette=p,
        )
        renders.append(render)
        if save_root_path!=None:
            if not os.path.exists(save_root_path):
                os.mkdir(save_root_path)
            render.save(f"results/render-{p}.png")

    # display
    if display:
        fig, axes = plt.subplots(1, 5, figsize=(20, 4))
        for render, ax in zip(renders, axes.ravel()):
            ax.grid(False)
            ax.axis('off')
            ax.imshow(render)
    return renders

def render_by_percentiles(flir_path,min_v=0,max_v=1.0,save_image_path=None,palette="copper"):
    thermogram = flyr.unpack(flir_path)
    # To render by percentiles, call as below.
    # This approach is useful when it isn't known what temperature range to render.
    render = thermogram.render_pil(
        min_v=min_v,
        max_v=max_v,
        unit="percentiles",
        palette=palette,
    )
    if save_image_path!=None:
        render.save(save_image_path)
    return render

def get_thermogram(flir_path):
    return flyr.unpack(flir_path)

def render_with_mask(thermogram,mask,save_path=None):
    render=thermogram.render_pil(mask=mask)
    if save_path!=None:
        render.save(save_path)
    return render

def adjust_emissivity(flir_path,emissivity=1.0,min_v=27.1,max_v=35.6):
    thermogram = flyr.unpack(flir_path)
    thermogram = thermogram.adjust_metadata(emissivity=emissivity)
    # thermal = thermogram.celsius  # Access updated data as normal
    render = thermogram.render_pil(
        min_v=min_v,
        max_v=max_v,
        unit="celsius",
        palette="viridis",
    )
    return render

def get_flir_metadata(flir_path):
    thermogram = flyr.unpack(flir_path)
    cm = thermogram.camera_metadata
    print(cm.data)  # Raw EXIF data (dict)
    print(cm.gps_data)  # Raw GPS data (dict)
    print(cm.date_time)  # Parsed datetime object of when picture was taken (datetime)
    print(cm.gps_altitude)  # (float)
    print(cm.gps_image_direction)  # (float)
    print(cm.gps_latitude)  # (float)
    print(cm.gps_longitude)  # (float)
    print(cm.gps_map_datum)  # (str)
    print(cm.make)  # (str)
    print(cm.model)  # (str)
    print(cm.software)  # (str)
    print(cm.x_resolution)  # (float)
    print(cm.y_resolution)  # (float)
    return cm

def picture_in_picture(flir_path,mask,mode='classical',save_image_path=None):
    # mode =  alternative
    thermogram = flyr.unpack(flir_path)
    # mask = thermogram.kelvin > thermogram.kelvin.mean()
    render1 = thermogram.picture_in_picture_pil(mask=mask, mask_mode=mode)
    if save_image_path!=None:
        fig, axes = plt.subplots(1, 2, figsize=(8, 4))
        for render, ax in zip([render1], axes.ravel()):
            ax.grid(False)
            ax.axis('off')
            ax.imshow(render)
    return render1
