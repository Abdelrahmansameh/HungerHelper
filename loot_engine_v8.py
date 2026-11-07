# Loot Engine V8: Updated with Yellow / Purple / Blue priority colors

def get_map_loot(map_name):
    points = []
    
    # Priority Colors:
    # Priority 1 = Yellow (255, 234, 0)
    # Priority 2 = Purple (168, 85, 247)
    # Priority 3 = Blue (56, 189, 248)

    if map_name == "Sarlat Farm":
        # Master Granary Cluster (Flour) -> Priority 1 (Yellow)
        granary_pts = [
            (1259, 1065), (1240, 1080), (1280, 1050), (1220, 1100), (1310, 1040),
            (1265, 1120), (1295, 1090), (1235, 1060), (1275, 1140), (1250, 1030),
            (1330, 1070), (1300, 1115), (1220, 1045), (1285, 1160), (1340, 1095),
            (1210, 1085), (1270, 1015), (1315, 1135)
        ]
        for x, y in granary_pts:
            points.append({'x': x, 'y': y, 'prio': 1, 'color': (255, 234, 0), 'is_100': True, 'type': 'Flour Sack'})
            
        # Sarlat Village Granaries -> Priority 1 (Yellow)
        village_pts = [
            (2368, 1475), (2340, 1450), (2390, 1500), (2320, 1480), (2410, 1460),
            (2355, 1520), (2385, 1430), (2330, 1510), (2420, 1490), (2370, 1410),
            (2400, 1530), (2310, 1440), (2430, 1470), (2360, 1540)
        ]
        for x, y in village_pts:
            points.append({'x': x, 'y': y, 'prio': 1, 'color': (255, 234, 0), 'is_100': True, 'type': 'Flour Sack'})

        # Priority 2 (Purple): Bullion Boxes on Sarlat
        bullion_pts = [
            (1280, 1100), (2380, 1450), (1750, 2100), (1920, 1850), (1450, 2600),
            (2100, 2500), (2800, 2100), (1600, 1400), (2650, 1750), (950, 2200),
            (2250, 1950), (1850, 2300)
        ]
        for x, y in bullion_pts:
            points.append({'x': x, 'y': y, 'prio': 2, 'color': (168, 85, 247), 'is_100': True, 'type': 'Bullion Box'})

        # Priority 2 (Purple): Wall Cabinets (China Bowl)
        cabinet_pts = [(1245, 1075), (2350, 1460), (1880, 1820), (2750, 2080)]
        for x, y in cabinet_pts:
            points.append({'x': x, 'y': y, 'prio': 2, 'color': (168, 85, 247), 'is_100': True, 'type': 'Wall Cabinet'})

        # Priority 3 (Blue): Piles of Ash (15x Charcoal)
        ash_pts = [
            (1230, 1050), (1270, 1110), (2330, 1470), (2400, 1440), (1720, 2080),
            (1950, 1830), (1420, 2580), (2120, 2480), (2780, 2120), (1580, 1380),
            (2220, 1970), (1830, 2280), (1050, 2150), (2550, 1700), (2850, 2050)
        ]
        for x, y in ash_pts:
            points.append({'x': x, 'y': y, 'prio': 3, 'color': (56, 189, 248), 'is_100': True, 'type': 'Pile of Ash'})

    elif map_name == "Jacques Bridge":
        # Guardhouse Bullion Boxes -> Priority 2 (Purple)
        bullion_pts = [
            (2050, 2020), (2075, 2040), (2030, 2060), (2090, 2010),
            (1380, 1540), (2110, 1330), (1800, 2500), (2400, 1800)
        ]
        for x, y in bullion_pts:
            points.append({'x': x, 'y': y, 'prio': 2, 'color': (168, 85, 247), 'is_100': True, 'type': 'Bullion Box'})

        # Tooling Bins & Cabinets -> Priority 3 (Blue)
        tool_pts = [
            (2040, 2030), (2060, 2050), (1390, 1520), (2100, 1350),
            (1780, 2480), (2420, 1820), (1950, 2200), (2200, 1900)
        ]
        for x, y in tool_pts:
            points.append({'x': x, 'y': y, 'prio': 3, 'color': (56, 189, 248), 'is_100': True, 'type': 'Tooling Bin'})

    elif map_name == "Sombre Forest":
        # Outer Ramparts Merchants -> Priority 2 (Purple)
        merch_pts = [(2100, 950), (2120, 970), (2080, 960), (2140, 940)]
        for x, y in merch_pts:
            points.append({'x': x, 'y': y, 'prio': 2, 'color': (168, 85, 247), 'is_100': True, 'type': 'Merchant'})

        # Surface Sacks -> Priority 1 (Yellow)
        sack_pts = [
            (1500, 1800), (1520, 1820), (1480, 1790), (2800, 2200),
            (2820, 2230), (1900, 2500), (2200, 1600), (2500, 2900)
        ]
        for x, y in sack_pts:
            points.append({'x': x, 'y': y, 'prio': 1, 'color': (255, 234, 0), 'is_100': True, 'type': 'Sack'})

    return points
