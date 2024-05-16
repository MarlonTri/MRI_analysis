import bpy
import json

infos_path  = r"C:\Users\marlon\Documents\projects\MRI_mesher\infos.json"
with open(infos_path) as f:
    infos = json.load(f)
filt="SE000003"

for info in infos:
    file_path = info["img_path"]
    if filt not in file_path:
        continue
    bpy.ops.import_image.to_plane(shader='SHADELESS', files=[{'name':file_path}])
    obj = bpy.data.objects[-1]
    obj.location = tuple(info["pos"])