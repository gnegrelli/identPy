import numpy as np

from identpy.Model import Model


class DFIG(Model):

    def __init__(self, x_0=0, u_0=0, u=0, method=None, step_int=0.001, v_tref=1.0105, p_tref=0.982, q_tref=0.057595,
                 v_tmin=0.9):
        super(DFIG, self).__init__(x_0, u_0, u, method)

        self.step_int = step_int
        self.v_tref = v_tref
        self.p_tref = p_tref
        self.q_tref = q_tref
        self.v_tmin = v_tmin

        self.v_pa_adj = 0
        self.v_qa_adj = 0

        self.last_v_pas = 0
        self.last_v_qas = 0

        self.parameters = {
            'R': 'Equivalent Resistance',
            'X': 'Equivalent Reactance',
            'k_I': 'PI Gain',
            'T_I': 'PI Time Constant',
            'T_V': 'Delay Time Constant',
            'k_VC': 'Voltage Controller Gain',
            'i_max': 'Maximum Current',
        }

        self.inputs = {
            'v_T': 'Terminal Voltage Magnitude',
            'i_P': 'Current Active Component',
            'i_Q': 'Current Reactive Component',
        }

        self.outputs = {
            'P_e': 'Active Power',
            'Q_e': 'Reactive Power',
        }

    def update_parameters(self, p):
        super(DFIG, self).update_parameters(p)
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
                i_qref = min(np.abs(i_re), self.p[6])*i_re/np.abs(i_re)
                i_pref = np.sqrt(self.p[6]**2 - i_qref**2)
            else:
                i_pref = min(np.abs(i_ac), self.p[6])*i_ac/np.abs(i_ac)
                i_qref = np.sqrt(self.p[6]**2 - i_pref**2)

        # PI Block
        if np.equal(u, self.u_0).all():
            v_pa = self.v_pa_adj
            v_qa = self.v_qa_adj
        else:
            v_pa = self.p[2]*(self.p[3] + self.step_int)/self.p[3]*(i_pref - u[3]/u[1]) + self.v_pa_adj
            v_qa = self.p[2]*(self.p[3] + self.step_int)/self.p[3]*(u[4]/u[1] - i_qref) + self.v_qa_adj

        if factor == 0:
            self.v_pa_adj = v_pa - self.p[2] * (i_pref - u[3] / u[1])
            self.v_qa_adj = v_qa - self.p[2] * (u[4] / u[1] - i_qref)

        v_pas = -np.cos(u[2])*v_pa - np.sin(u[2])*v_qa
        v_qas = np.sin(u[2])*v_pa - np.cos(u[2])*v_qa

        if not factor:
            self.last_v_pas = v_pas
            self.last_v_qas = v_qas
        else:
            v_pas = factor*(v_pas - self.last_v_pas) + self.last_v_pas
            v_qas = factor*(v_qas - self.last_v_qas) + self.last_v_qas

        f1 = (v_pas - x[0])/self.p[4]
        f2 = (v_qas - x[1])/self.p[4]

        return np.array([f1, f2])

    def g(self, x=None, u=None):

        x, u = super().g(x, u)

        # TODO: Check calculation of vtd and vtq. Which angle should I use.
        vtd = u[1]*np.cos(u[2])
        vtq = u[1]*np.sin(u[2])

        # TODO: Limits of x should enter here (-1 <= x <= 1)

        g1 = (self.p[0]*(vtd*x[0] + vtq*x[1] - u[1]**2) + self.p[1]*(vtd*x[1] - vtq*x[0]))/(self.p[0]**2 + self.p[1]**2)
        g2 = (self.p[1]*(vtd*x[0] + vtq*x[1] - u[1]**2) - self.p[0]*(vtd*x[1] - vtq*x[0]))/(self.p[0]**2 + self.p[1]**2)

        return np.array([g1, g2])

    def reset_adjustments(self):
        v = self.u_0[1]*np.cos(self.u_0[2]) + 1j*self.u_0[1]*np.sin(self.u_0[2])
        i = np.conj(self.u_0[3] + 1j*self.u_0[4])/np.conj(v)

        e = v + i*(self.p[0] + 1j*self.p[1])
        vd = np.real(e)
        vq = np.imag(e)

        ej = np.array([[-np.cos(self.u_0[2]), -np.sin(self.u_0[2])], [np.sin(self.u_0[2]), -np.cos(self.u_0[2])]])

        va = np.linalg.solve(ej, np.array([[vd], [vq]]))

        self.v_pa_adj = va[0][0]
        self.v_qa_adj = va[1][0]
