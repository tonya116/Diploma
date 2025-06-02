
import csv
from dataclasses import dataclass
import json

@dataclass
class Channel:
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

def load_channels_from_csv(filename: str) -> list[Channel]:
    channels = {}
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=" ")
        for row in reader:
            channels.update({row["Номер_балки"]:
                Channel(
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
            )})
    return channels
