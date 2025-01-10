from ultralytics import YOLO
import cv2
import numpy as np
import pandas as pd
from glob import glob
import matplotlib.pylab as plt
import torch
import matplotlib.pyplot as plt1

model_type = "MiDaS_small"
midas = torch.hub.load('intel-isl/MiDaS', model_type)
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
midas.to(device)
midas.eval()

# Input transformation pipeline
transforms = torch.hub.load('intel-isl/MiDaS', 'transforms')
if model_type == "DPT_Large" or model_type == "DPT_Hybrid":
    transform = transforms.dpt_transform
else:
    transform = transforms.small_transform


def find_largest_max_depth_area(depth_map):
    THRESHOLD = 100
    max_depth = np.max(depth_map)
    print("MAX DEPTH: ", max_depth)
    
    # binary mask (0,1)
    mask = depth_map >= max_depth - THRESHOLD
    mask = mask.astype(np.uint8)
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # key=cv2.contourArea -> identifies the largest connected region 
    largest_contour = max(contours, key=cv2.contourArea) 
    
    # Get bounding box and centroid
    x, y, w, h = cv2.boundingRect(largest_contour)
    centroid_x = x + w // 2
    centroid_y = y + h // 2
    
    return max_depth, (centroid_x, centroid_y), contours



def visualize_largest_max_depth_area(depth_map, rgb_image):
    max_depth, centroid, contours = find_largest_max_depth_area(depth_map)
    
    for contour in contours:
        cv2.polylines(img, [contour], True, color=(0, 255, 0), thickness=2)
        # centroid
        cv2.circle(rgb_image, (centroid[0], centroid[1]), 5, (0, 255, 0), -1)
    
    return rgb_image


model = YOLO('/best.pt')
class_names = model.names


cap = cv2.VideoCapture("../images/1.jpg")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
          
    # Process frame for both predictions (depth and object detection)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imgbatch = transform(img).to(device)

    with torch.no_grad():
        depth_prediction = midas(imgbatch)
        depth_prediction = torch.nn.functional.interpolate(
            depth_prediction.unsqueeze(1), size=img.shape[:2], mode='bicubic', align_corners=False
        ).squeeze()
        depth_output = depth_prediction.cpu().numpy()


    # Normalize depth values to 0-255 for visualization
    output = (depth_output - depth_output.min()) / (depth_output.max() - depth_output.min()) * 255
    output = output.astype(np.uint8)
    output = cv2.applyColorMap(output, cv2.COLORMAP_WINTER)
    cv2.imshow('Depth Map', output)
    
    image_with_depth = visualize_largest_max_depth_area(depth_output, img)
    

    results = model.predict(img.copy())  

    for r in results:
        boxes = r.boxes
        masks = r.masks

        if masks is not None:
            masks = masks.data.cpu()
            
            for seg, box in zip(masks.data.cpu().numpy(), boxes):
                seg = cv2.resize(seg, (img.shape[1], img.shape[0])) 
                contours, _ = cv2.findContours((seg).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
                # print(sorted_contours)
                for i, contour in enumerate(sorted_contours):
                    M = cv2.moments(contour)
                    if M["m00"] == 0:
                        continue
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    
                    d = int(box.cls)
                    c = class_names[d]
                    x, y, x1, y1 = cv2.boundingRect(contour)

                    depth_at_center = depth_output[cY, cX]  # Get depth at object center
                    cv2.putText(img, "Est.:{}".format(str(round(depth_at_center, 2))), (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)

                    cv2.polylines(img, [contour], True, color=(0, 0, 255), thickness=1)
                    cv2.putText(img, str(i) + c, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.circle(img, (cX, cY), 5, (0, 0, 255), -1)

                    ratio_pixel_mm = 155 / 14 # 14 mm = 155 pixels
                    mm = x1 / ratio_pixel_mm
                    cm = mm / 10
                    cv2.putText(img, str(round(cm, 2)), (x, y-30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
                    
                    rect = cv2.minAreaRect(contour)
                    (mx,my),(mw,mh),angle = rect
                    cv2.putText(img, "Angle:{}".format(angle), (int(x), int(y)-40), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1 )
                    cv2.putText(img, "Area:{}".format(cv2.contourArea(contour)), (int(x), int(y)), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1 )

    # Display results
    cv2.imshow('Combined Prediction', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)