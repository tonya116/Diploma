from dataclasses import dataclass
from typing import List
import matplotlib.pyplot as plt
import numpy as np

@dataclass
class PointLoad:
    position: float  # м
    magnitude: float  # Н

@dataclass
class DistributedLoad:
    start: float      # м
    end: float        # м
    intensity: float  # Н/м (равномерная)

@dataclass
class MomentLoad:
    position: float  # м
    magnitude: float  # Н*м

@dataclass
class Support:
    position: float  # м
    type: str        # 'pin' or 'roller'

class Beam:
    def __init__(self, length: float):
        self.length = length
        self.point_loads: List[PointLoad] = []
        self.distributed_loads: List[DistributedLoad] = []
        self.moment_loads: List[MomentLoad] = []
        self.supports: List[Support] = []

    def add_point_load(self, load: PointLoad):
        self.point_loads.append(load)

    def add_distributed_load(self, load: DistributedLoad):
        self.distributed_loads.append(load)

    def add_moment_load(self, moment: MomentLoad):
        self.moment_loads.append(moment)

    def add_support(self, support: Support):
        self.supports.append(support)

    def compute_reactions(self):
        if len(self.supports) != 2:
            raise NotImplementedError("Поддерживается только два опоры")
        a, b = sorted(self.supports, key=lambda s: s.position)
        xa, xb = a.position, b.position
        L = xb - xa

        # Сумма моментов относительно xa
        moment_sum = 0
        for load in self.point_loads:
            moment_sum += load.magnitude * (load.position - xa)
        for dist in self.distributed_loads:
            w = dist.intensity
            x = (dist.start + dist.end) / 2
            moment_sum += w * (dist.end - dist.start) * (x - xa)
        for moment in self.moment_loads:
            moment_sum += moment.magnitude

        # Вертикальная сила в b
        Rb = moment_sum / L

        # Общая вертикальная сила
        total_load = sum(l.magnitude for l in self.point_loads) + \
                     sum(d.intensity * (d.end - d.start) for d in self.distributed_loads)
        Ra = total_load - Rb
        print(Ra, Rb)
        return xa, Ra, xb, Rb

    def shear_and_moment(self, resolution=500):
        xa, Ra, xb, Rb = self.compute_reactions()
        x = np.linspace(0, self.length, resolution)
        V = np.zeros_like(x)
        M = np.zeros_like(x)

        for i, xi in enumerate(x):
            v = 0
            m = 0
            # Reactions
            if xi >= xa:
                v += Ra
                m += Ra * (xi - xa)
            if xi >= xb:
                v += Rb
                m += Rb * (xi - xb)
            # Point loads
            for load in self.point_loads:
                if xi >= load.position:
                    v -= load.magnitude
                    m -= load.magnitude * (xi - load.position)
            # Distributed loads
            for dist in self.distributed_loads:
                if xi >= dist.start:
                    x1 = dist.start
                    x2 = min(xi, dist.end)
                    w = dist.intensity
                    l = x2 - x1
                    v -= w * l
                    m -= w * l * (xi - (x1 + x2) / 2)
            # Moments
            for moment in self.moment_loads:
                if xi >= moment.position:
                    m += moment.magnitude

            V[i] = v
            M[i] = m

        return x, V, M

    def plot(self):
        x, V, M = self.shear_and_moment()
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
        ax1.plot(x, V, label="Shear Force (V)")
        ax1.axhline(0, color='gray', linestyle='--')
        ax1.set_ylabel("V, N")
        ax1.grid(True)
        ax1.legend()

        ax2.plot(x, M, label="Bending Moment (M)", color='orange')
        ax2.axhline(0, color='gray', linestyle='--')
        ax2.set_ylabel("M, N*m")
        ax2.set_xlabel("x, m")
        ax2.grid(True)
        ax2.legend()
        plt.tight_layout()
        plt.show()


beam = Beam(length=10)
beam.add_support(Support(position=0, type='pin'))
beam.add_support(Support(position=10, type='roller'))  # опора не на краю

beam.add_point_load(PointLoad(position=3, magnitude=28.75))
beam.add_point_load(PointLoad(position=7, magnitude=-93.75))

beam.add_distributed_load(DistributedLoad(start=7, end=10, intensity=40))
beam.add_moment_load(MomentLoad(position=5, magnitude=60))

beam.plot()
