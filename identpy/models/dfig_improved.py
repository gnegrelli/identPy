import numpy as np

from identpy.objects import Model


class DFIG_improved(Model):

    parameters = {
        'R': 'Equivalent Resistance',
        'X': 'Equivalent Reactance',
        'k<sub>I</sub>': 'PI Gain',
        'T<sub>I</sub>': 'PI Time Constant',
        'T<sub>V</sub>': 'Delay Time Constant',
        'k<sub>VC</sub>': 'Voltage Controller Gain',
        'i<sub>max</sub>': 'Maximum Current',
    }

    inputs = {
        'v<sub>T</sub>': 'Terminal Voltage Magnitude',
        'i<sub>P</sub>': 'Current Active Component',
        'i<sub>Q</sub>': 'Current Reactive Component',
    }

    outputs = {
        'P<sub>e</sub>': 'Active Power',
        'Q<sub>e</sub>': 'Reactive Power',
    }

    states = {
        'v<sub>d</sub>': 'Direct component',
        'v<sub>q</sub>': 'Quadrature component',
    }

    def __init__(self, x_0=0, u_0=0, u=0, method=None, step_int=0.001, v_tref=1.010484848484848, p_tref=0.982,
                 q_tref=0.057595555555556, v_tmin=0.9):
        super().__init__(x_0, u_0, u, method)

        self.step_int = step_int
        self.v_tref = v_tref
        self.p_tref = p_tref
        self.q_tref = q_tref
        self.v_tmin = v_tmin

        self.v_pa_adj = 0
        self.v_qa_adj = 0

        self.last_v_pa = 0
        self.last_v_qa = 0

    def update_parameters(self, p):
        super().update_parameters(p)
        self.reset_adjustments()

    def f(self, x=None, u=None, factor=0):

        x, u = super().f(x, u)

        i_ac = self.p_tref/u[1]
        i_re = self.p[5]*(self.v_tref - u[1]) + self.q_tref/self.v_tref

        # Current Priority Block
        if np.sqrt(i_ac**2 + i_re**2) < self.p[6]:
            i_pref = i_ac
            i_qref = i_re
        else:
            if u[1] < self.v_tmin:
                i_qref = min(np.abs(i_re), self.p[6])
                i_pref = np.sqrt(self.p[6]**2 - i_qref**2)
            else:
                i_pref = min(np.abs(i_ac), self.p[6])
                i_qref = np.sqrt(self.p[6]**2 - i_pref**2)

        # PI Block
        if np.equal(u, self.u_0).all():
            v_pa = self.v_pa_adj
            v_qa = self.v_qa_adj
        else:
            v_pa = self.p[2]*(self.p[3] + self.step_int)/self.p[3]*(i_pref - u[3]/u[1]) + self.v_pa_adj
            v_qa = self.p[2]*(self.p[3] + self.step_int)/self.p[3]*(u[4]/u[1] - i_qref) + self.v_qa_adj

        if not factor:
            self.v_pa_adj = v_pa - self.p[2] * (i_pref - u[3] / u[1])
            self.v_qa_adj = v_qa - self.p[2] * (u[4] / u[1] - i_qref)

            self.last_v_pa = v_pa
            self.last_v_qa = v_qa
        else:
            v_pa = factor*(v_pa - self.last_v_pa) + self.last_v_pa
            v_qa = factor*(v_qa - self.last_v_qa) + self.last_v_qa

        f1 = (-v_pa - x[0])/self.p[4]
        f2 = (-v_qa - x[1])/self.p[4]

        return np.array([f1, f2])

    def g(self, x=None, u=None):

        x, u = super().g(x, u)

        # Limits of x (-1 <= x <= 1)
        x = np.clip(x, a_max=1.1, a_min=-1)

        g1 = (self.p[0]*u[1]*(x[0] - u[1]) + self.p[1]*u[1]*x[1])/(self.p[0]**2 + self.p[1]**2)
        g2 = (self.p[1]*u[1]*(x[0] - u[1]) - self.p[0]*u[1]*x[1])/(self.p[0]**2 + self.p[1]**2)

        return np.array([g1, g2])

    def reset_adjustments(self):
        i = (self.u_0[3] - 1j * self.u_0[4]) / self.u_0[1]

        e = self.u_0[1] + i * (self.p[0] + 1j * self.p[1])
        vd = np.real(e)
        vq = np.imag(e)

        self.x_0 = np.array([vd, vq])

        self.v_pa_adj = -vd
        self.v_qa_adj = -vq
