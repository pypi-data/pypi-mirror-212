from quartical.gains.gain import Gain, gain_spec_tup, param_spec_tup
from quartical.gains.amplitude.kernel import amplitude_solver, amplitude_args
import numpy as np


class Amplitude(Gain):

    solver = amplitude_solver
    term_args = amplitude_args

    def __init__(self, term_name, term_opts, data_xds, coords, tipc, fipc):

        Gain.__init__(self, term_name, term_opts, data_xds, coords, tipc, fipc)

        parameterisable = ["XX", "YY", "RR", "LL"]

        self.parameterised_corr = \
            [ct for ct in self.corr_types if ct in parameterisable]
        self.n_param = len(self.parameterised_corr)

        self.gain_chunk_spec = gain_spec_tup(self.n_tipc_g,
                                             self.n_fipc_g,
                                             (self.n_ant,),
                                             (self.n_dir,),
                                             (self.n_corr,))
        self.param_chunk_spec = param_spec_tup(self.n_tipc_g,
                                               self.n_fipc_g,
                                               (self.n_ant,),
                                               (self.n_dir,),
                                               (self.n_param,))
        self.gain_axes = ("gain_t", "gain_f", "ant", "dir", "corr")
        self.param_axes = ("param_t", "param_f", "ant", "dir", "param")

    def make_xds(self):

        xds = Gain.make_xds(self)

        param_template = ["amplitude_{}"]

        param_labels = [pt.format(ct) for ct in self.parameterised_corr
                        for pt in param_template]

        xds = xds.assign_coords({"param": np.array(param_labels),
                                 "param_t": self.param_times,
                                 "param_f": self.param_freqs})
        xds = xds.assign_attrs({"GAIN_SPEC": self.gain_chunk_spec,
                                "PARAM_SPEC": self.param_chunk_spec,
                                "GAIN_AXES": self.gain_axes,
                                "PARAM_AXES": self.param_axes})

        return xds

    @staticmethod
    def init_term(
        gain, param, term_ind, term_spec, term_opts, ref_ant, **kwargs
    ):
        """Initialise the gains (and parameters)."""

        Gain.init_term(
            gain, param, term_ind, term_spec, term_opts, ref_ant, **kwargs
        )

        param[:] = 1  # Amplitudes start at unity. TODO: Estimate?
