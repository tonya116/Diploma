
import csv
from dataclasses import dataclass
import json

@dataclass
class Channel:
    name: str
    h: float    # мм
    b: float    # мм
    d: float    # мм
    t: float    # мм
    A: float     # Площадь, см²
    mass: float  # Масса, кг/м
    Ix: float    # См⁴
    Wx: float    # См³
    ix: float    # См
    Sx: float    # См³
    Iy: float    # См⁴
    Wy: float    # См³
    iy: float    # См


class Sortament:
    def __init__(self):
        self.channels = {}
        types = ["IBeam", "Channel"]
        
        for channel in types:
            self.load_channels_from_csv(f"python/data/{channel}.csv", channel)

    def load_channels_from_csv(self, filename: str, type: str):
        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=" ")
            
            self.channels.update({type:[]})
            for row in reader:
                self.channels[type].append(
                    Channel(
                    name=row["Номер_балки"],
                    h=float(row["h"]),
                    b=float(row["b"]),
                    d=float(row["d"]),
                    t=float(row["t"]),
                    A=float(row["Площадь_сечения"]),
                    mass=float(row["Масса"]),
                    Ix=float(row["I_x"]),
                    Wx=float(row["W_x"]) / 1_000_000_000,
                    ix=float(row["i_x"]),
                    Sx=float(row["S_x"]),
                    Iy=float(row["I_y"]),
                    Wy=float(row["W_y"]),
                    iy=float(row["i_y"]),
                ))
    def find_by_Wx(self, Wx):
        for type, channel in self.channels.items():
            for data in channel:
                if data.Wx > Wx:                    
                    return data.Ix