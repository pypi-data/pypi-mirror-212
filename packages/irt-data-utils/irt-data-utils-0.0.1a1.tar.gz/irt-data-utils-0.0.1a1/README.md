## Infrared Thermal Data Utils

### Examples

```python
import irtdata.DDTFile as ddt

ddt.convert_ddt_to_csv_png(
    ddt_path="data/test1.ddt",
    csv_path='outputs/test1.csv',
    png_path='outputs/test1.png',
    bmp_path='outputs/test1.bmp')

```

```python
import irtdata.FLIR as flir
flir_path='data/test2.jpg'
flir.extract_temperature(flir_path,save_csv_path='outputs/test2.csv')
temp_data = flir.get_heatmap('outputs/test2.csv',
                             save_image_path='outputs/test2.jpg',show=True)
```