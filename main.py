from model import get_yolov5
from fastapi import FastAPI, File, UploadFile
from PIL import Image
from io import BytesIO
from fastapi.responses import Response

app = FastAPI(title="Temperature Detection API",
    description="""Upload image and the API will response temperature shown on the Thermometer""",
    version="0.0.1",)

## สร้าง object ของโมเดลไว้สำหรับการเช็คโลโก้ในภาพ
model_logo = get_yolov5(0.4)

@app.post("/detectImage")
async def detect_image(file: UploadFile):
    ## รับ input เป็นรูปภาพซึ่งผู้ใช้งานอัพโหลดเข้ามา
    
    ## Read Image
    img = Image.open(BytesIO(await file.read()))
    
    ## Inference โดย input คือรูปที่เราอ่านมา และใช้ขนาด 640
    results = model_logo(img, size= 640)
    results.render()
    
    ## เก็บภาพใน memory เพื่อให้ไวขึ้น และทำการ return รูปไปให้ผู้ใช้งาน
    bytes_io = BytesIO()
    img_base64 = Image.fromarray(results.imgs[0])
    img_base64.save(bytes_io, format="jpeg")
    
    return Response(content=bytes_io.getvalue(),media_type="image/jpeg")

@app.post("/getTemperature")
async def detect_image_label(file: UploadFile):
  
    img = Image.open(BytesIO(await file.read()))
    results = model_logo(img, size= 640)
    #thermo_result =  results.pandas().xyxy[0].sort_values('xmin').reset_index().values.tolist()
    temp=results.pandas().xyxy[0].sort_values('xmin')  # sorted left-right on X AXIS
    temp1=temp.loc[temp['name'] != 'screen'] #filter screen out which we dont use
    #temp2=temp1.loc[temp1['confidence'] > 0.5]
    thermo_result=temp1['name'].values.tolist()
    confident_result=temp1['confidence'].values.tolist()                        ##<-----------------เพิ่มผลความมั่นใจ
    return {"thermo": thermo_result, "confidence": confident_result}            ##<-----------------เพิ่มAPI resulf