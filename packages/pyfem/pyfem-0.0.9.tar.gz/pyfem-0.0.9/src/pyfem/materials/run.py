# -*- coding: utf-8 -*-
"""

"""
from typing import Optional, Tuple

from numba import njit
from numpy import zeros, ndarray, dot, sqrt, outer, array, ones

from pyfem.fem.constants import DTYPE
from pyfem.io.Material import Material
from pyfem.materials.BaseMaterial import BaseMaterial
from pyfem.materials.ElasticIsotropic import get_stiffness_from_young_poisson
from pyfem.utils.colors import error_style
from pyfem.utils.wrappers import show_running_time


class PlasticKinematicHardening(BaseMaterial):
    allowed_option = ['PlaneStress', 'PlaneStrain', None]

    def __init__(self, material: Material, dimension: int, option: Optional[str] = None) -> None:
        super().__init__(material, dimension, option)
        self.young: float = self.material.data[0]
        self.poisson: float = self.material.data[1]
        self.yield_stress: float = self.material.data[2]
        self.hard: float = self.material.data[3]
        self.EBULK3: float = self.young / (1.0 - 2.0 * self.poisson)
        self.EG2: float = self.young / (1.0 + self.poisson)
        self.EG: float = self.EG2 / 2.0
        self.EG3: float = 3.0 * self.EG
        self.ELAM: float = (self.EBULK3 - self.EG2) / 3.0
        self.tolerance: float = 1.0e-10
        self.create_tangent()

    def create_tangent(self):
        if self.option in self.allowed_option:
            if self.dimension == 3:
                self.option = None
            self.ddsdde = get_stiffness_from_young_poisson(self.dimension, self.young, self.poisson, self.option)
        else:
            error_msg = f'{self.option} is not the allowed options {self.allowed_option}'
            raise NotImplementedError(error_style(error_msg))


def get_smises(s: ndarray) -> float:
    if len(s) == 3:
        smises = sqrt(s[0] ** 2 + s[1] ** 2 - s[0] * s[1] + 3 * s[2] ** 2)
        return float(smises)
    elif len(s) == 6:
        smises = (s[0] - s[1]) ** 2 + (s[1] - s[2]) ** 2 + (s[2] - s[0]) ** 2
        smises += 6 * sum([i ** 2 for i in s[3:]])
        smises = sqrt(0.5 * smises)
        return float(smises)
    else:
        raise NotImplementedError(error_style(f'unsupported stress dimension {len(s)}'))


@njit('float64')
def get_tangent2(props,
                 state_variable,
                 ddsdde,
                 state: ndarray,
                 dstate: ndarray,
                 element_id: int,
                 igp: int,
                 ntens: int,
                 ndi: int,
                 nshr: int) -> Tuple[ndarray, ndarray]:
    young = props[0]
    poisson = props[1]
    yield_stress = props[2]
    hard = props[3]
    EBULK3 = young / (1.0 - 2.0 * poisson)
    EG2 = young / (1.0 + poisson)
    EG = EG2 / 2.0
    EG3 = 3.0 * EG
    ELAM = (EBULK3 - EG2) / 3.0
    tolerance = 1.0e-10

    elastic_strain = zeros(ntens, dtype=DTYPE)
    plastic_strain = zeros(ntens, dtype=DTYPE)
    back_stress = zeros(ntens, dtype=DTYPE)
    stress = zeros(ntens, dtype=DTYPE)

    dstrain = dstate
    elastic_strain += dstrain
    stress += dot(ddsdde, dstrain)
    s = stress - back_stress

    smises = sqrt(s[0] ** 2 + s[1] ** 2 - s[0] * s[1] + 3 * s[2] ** 2)

    if smises > (1.0 + tolerance) * yield_stress:
        hydrostatic_stress = sum(stress[:ndi]) / 3.0
        flow = stress - back_stress
        flow[:ndi] = flow[:ndi] - hydrostatic_stress
        flow *= 1.0 / smises

        delta_p = (smises - yield_stress) / (EG3 + hard)
        back_stress += hard * flow * delta_p

        plastic_strain[:ndi] += 1.5 * flow[:ndi] * delta_p
        elastic_strain[:ndi] -= 1.5 * flow[:ndi] * delta_p

        plastic_strain[ndi:] += 3.0 * flow[ndi:] * delta_p
        elastic_strain[ndi:] -= 3.0 * flow[ndi:] * delta_p

        stress = back_stress + flow * yield_stress
        stress[:ndi] += hydrostatic_stress

        EFFG = EG * (yield_stress + hard * delta_p) / smises
        EFFG2 = 2.0 * EFFG
        EFFG3 = 3.0 * EFFG
        EFFLAM = (EBULK3 - EFFG2) / 3.0
        EFFHRD = EG3 * hard / (EG3 + hard) - EFFG3

        ddsdde = zeros(shape=(ntens, ntens))
        ddsdde[:ndi, :ndi] = EFFLAM

        for i in range(ndi):
            ddsdde[i, i] += EFFG2

        for i in range(ndi, ntens):
            ddsdde[i, i] += EFFG

        ddsdde += EFFHRD * outer(flow, flow)

    return ddsdde, stress


@show_running_time
def main():
    from pyfem.Job import Job

    job = Job(r'F:\Github\pyfem\examples\rectangle\rectangle.toml')

    material_data = PlasticKinematicHardening(job.props.materials[0], 2)

    for i in range(2):
        gp_ddsdde, gp_stress = get_tangent2(props=array(material_data.material.data),
                                            state_variable=zeros(0),
                                            ddsdde=material_data.ddsdde,
                                            state=ones(3),
                                            dstate=ones(3),
                                            element_id=1,
                                            igp=1,
                                            ntens=3,
                                            ndi=2,
                                            nshr=1)

if __name__ == "__main__":
    main()

