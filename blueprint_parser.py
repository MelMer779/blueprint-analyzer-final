import os
import cv2
import math
import numpy as np
import easyocr
from bs4 import BeautifulSoup

#Default values for conversions
svg_to_sqft = 0.01
ceiling_height = 8
paint_coverage = 350
drywall_coverage = 32

#Initialize OCR reader
reader = easyocr.Reader(['en'])

#Functions for room area and center points
def polygon_area(coords):
    area = 0.0
    for i in range(len(coords)):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % len(coords)]
        area += (x1 * y2 - x2 * y1)
    return abs(area) / 2

def polygon_centroid(coords):
    x_coords = [p[0] for p in coords]
    y_coords = [p[1] for p in coords]
    return (sum(x_coords) / len(x_coords), sum(y_coords) / len(y_coords))

#Main function to parse blueprint folder and extract room measurements
def parse_blueprint_folder(folder_path):
    files = os.listdir(folder_path)

    if 'model.svg' not in files:
        raise FileNotFoundError("Missing model.svg")

    png_candidates = sorted([f for f in files if 'scaled' in f.lower() and f.lower().endswith('.png')])
    if not png_candidates:
        raise FileNotFoundError("No scaled PNG found")

    svg_path = os.path.join(folder_path, 'model.svg')
    image_path = os.path.join(folder_path, png_candidates[0])

    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = reader.readtext(img_rgb)

    ocr_rooms = []
    room_id = 1
    for (bbox, text, conf) in results:
        if conf > 0.6 and text.strip():
            pts = np.array(bbox).astype(int)
            center_x = int(np.mean(pts[:, 0]))
            center_y = int(np.mean(pts[:, 1]))
            ocr_rooms.append((f"Room {room_id}", center_x, center_y))
            room_id += 1

    with open(svg_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'xml')

    room_areas = {}
    for poly in soup.find_all('polygon'):
        points = poly.get('points')
        if not points:
            continue

        coords = []
        for p in points.strip().split():
            parts = p.split(',')
            if len(parts) == 2:
                try:
                    x, y = map(float, parts)
                    coords.append((x, y))
                except:
                    continue

        if len(coords) < 3:
            continue

        centroid = polygon_centroid(coords)
        area = polygon_area(coords)

        min_dist = float('inf')
        closest_room = None
        for room_name, x, y in ocr_rooms:
            dist = math.hypot(centroid[0] - x, centroid[1] - y)
            if dist < min_dist:
                min_dist = dist
                closest_room = room_name

        if closest_room:
            room_areas[closest_room] = room_areas.get(closest_room, 0) + area

    if not room_areas:
        raise ValueError("No rooms matched")

    results = []
    totals = {
        "area_sqft": 0.0,
        "flooring_sqft": 0.0,
        "paint_gallons": 0.0,
        "drywall_sheets": 0
    }

    for room, svg_area in sorted(room_areas.items(), key=lambda x: int(x[0].split()[1])):
        sqft = svg_area * svg_to_sqft
        flooring = sqft * 1.10
        wall_perimeter = math.sqrt(sqft) * 4
        wall_area = wall_perimeter * ceiling_height
        drywall = math.ceil(wall_area / drywall_coverage)
        paint = wall_area / paint_coverage

        row = {
            "room": room,
            "area_sqft": round(sqft, 2),
            "flooring_sqft": round(flooring, 2),
            "paint_gallons": round(paint, 2),
            "drywall_sheets": drywall
        }

        totals["area_sqft"] += sqft
        totals["flooring_sqft"] += flooring
        totals["paint_gallons"] += paint
        totals["drywall_sheets"] += drywall
        results.append(row)

    return {
        "blueprint": os.path.basename(folder_path),
        "totals": {k: round(v, 2) for k, v in totals.items()},
        "rooms": results
    }
