import os, math, sqlite3
from PIL import Image, ImageDraw

def cluster_points(points, threshold=36):
    """
    points: list of dicts with 'x', 'y', 'type', 'rate', 'img', etc.
    Returns list of points with updated (mx, my) de-clustered radially.
    """
    clusters = []
    for p in points:
        placed = False
        for c in clusters:
            cx = sum(item['raw_mx'] for item in c) / len(c)
            cy = sum(item['raw_my'] for item in c) / len(c)
            if math.hypot(p['raw_mx'] - cx, p['raw_my'] - cy) < threshold:
                c.append(p)
                placed = True
                break
        if not placed:
            clusters.append([p])
            
    result = []
    for c in clusters:
        n = len(c)
        if n == 1:
            c[0]['mx'] = c[0]['raw_mx']
            c[0]['my'] = c[0]['raw_my']
            result.append(c[0])
        else:
            cx = sum(item['raw_mx'] for item in c) / n
            cy = sum(item['raw_my'] for item in c) / n
            rad = 20 if n <= 3 else (26 if n <= 5 else 32)
            for i, item in enumerate(c):
                angle = (2 * math.pi * i) / n
                item['mx'] = int(cx + rad * math.cos(angle))
                item['my'] = int(cy + rad * math.sin(angle))
                result.append(item)
    return result

print("Cluster function defined.")
