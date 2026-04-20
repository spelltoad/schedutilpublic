import json, os, requests, random, time, difflib, re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin

DATA_ROOT = Path(__file__).parent.parent / 'data' / 'regions'

def get_available_dates(region_config):
    dates = [datetime.strptime(f.name, '%d.%m.%Y') for f in os.scandir(DATA_ROOT / region_config['id']) if f.is_dir()]
    dates.sort(reverse=True)
    dates = [datetime.strftime(s, '%d.%m.%Y') for s in dates]
    return dates

def compare_dirs(date1, date2, region_config):
    differences = []
    new = []
    path1 = DATA_ROOT / region_config['id'] / date1
    path2 = DATA_ROOT / region_config['id'] / date2 
    files1 = set(os.listdir(path1))
    files2 = set(os.listdir(path2))
    common_files = files1.intersection(files2)
    new_files = files1.difference(files2)
    for file in common_files:
        with open(os.path.join(path1, file), 'rb') as f1, open(os.path.join(path2, file), 'rb') as f2:
            timetable1 = f1.read()
            timetable2 = f2.read()
            if timetable1 != timetable2:
                href1 = f"/{region_config['id']}/file/{date1}/{file}"
                href2 = f"/{region_config['id']}/file/{date2}/{file}"
                differences.append((file, href1, href2))
    for file in new_files:
        href = f"/{region_config['id']}/file/{date1}/{file}"
        new.append((file, href))
    differences.sort()
    new.sort()
    return (differences, new)

def generate_dummy_timetable(region_id, routes, transport_type="bus"):
    if not routes:
        return

    current_date = datetime.today().strftime("%d.%m.%Y")
    dirpath = DATA_ROOT / region_id / current_date
    
    os.makedirs(dirpath, exist_ok=True)

    for route in routes:
        start_time = datetime.strptime("05:30", "%H:%M")
        end_time = datetime.strptime("23:45", "%H:%M")
        interval_minutes = random.choice([10, 15, 20, 25, 30])
        timetable_lines = [
            f"{route}",
            f"{transport_type.capitalize()}"
        ]
        current_time = start_time
        times = []
        while current_time <= end_time:
            times.append(current_time.strftime("%H:%M"))
            current_time += timedelta(minutes=interval_minutes)
        for i in range(0, len(times), 10):
            timetable_lines.append("  ".join(times[i:i+10]))
        content = "\n".join(timetable_lines)
        
        file_path = dirpath / f"{route}.txt"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        time.sleep(random.uniform(0.1, 0.4))
        print(f"[{region_id.upper()}] Route {route} schedule saved.")
        
    print(f"[{region_id.upper()}] Update completed.\n")


def bryansk():
    dummy_routes = ['101', '102', '103', '104']
    generate_dummy_timetable('bryansk', dummy_routes, transport_type='bus')

def bryansk_obl():
    dummy_routes = ['105', '106']
    generate_dummy_timetable('bryansk-obl', dummy_routes, transport_type='bus')

def smolensk():
    dummy_routes = ['bus_1', 'tram_1', 'trolleybus_1']
    generate_dummy_timetable('smolensk', dummy_routes, transport_type='mixed')

def sochi():
    dummy_routes = ['1', '2', '3', '4', '5']
    generate_dummy_timetable('sochi', dummy_routes, transport_type='bus')

def tula():
    dummy_routes = ['11', '12', 'Тр1', 'Тб1']
    generate_dummy_timetable('tula', dummy_routes, transport_type='mixed')

def tyumen():
    dummy_routes = ['1', '2', '3']
    generate_dummy_timetable('tyumen', dummy_routes, transport_type='bus')

def tambov():
    dummy_routes = ['1', '8', '9']
    generate_dummy_timetable('tambov', dummy_routes, transport_type='bus')
