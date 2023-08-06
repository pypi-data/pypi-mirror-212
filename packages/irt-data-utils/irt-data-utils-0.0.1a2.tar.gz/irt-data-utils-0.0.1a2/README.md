## Infrared Thermal Data Utils

### Examples
1. convert ddt file to images
```python
import irtdata.DDTFile as ddt

ddt.convert_ddt_to_csv_png(
    ddt_path="data/test1.ddt",
    csv_path='outputs/test1.csv',
    png_path='outputs/test1.png',
    bmp_path='outputs/test1.bmp')

```
2. Get temperature arrays from FLIR images
```python
import irtdata.FLIR as flir
flir_path='data/test2.jpg'
flir.extract_temperature(flir_path,save_csv_path='outputs/test2.csv')
temp_data = flir.get_heatmap('outputs/test2.csv',
                             save_image_path='outputs/test2.jpg',show=True)
```

3. Get Face Info

```python
import src.irtdata.face_detection as fd

list_node=fd.get_face_info(optical_path,csv_path)

print(list_node)
```

4. Fetch temperature info from gray images with temperature info

```python
import src.irtdata.image_utils as iu

temp_image_path=r'data/FLIR_00004.jpeg'

temps=iu.get_thermal_data_from_image(image_path=temp_image_path)

print(temps)
```