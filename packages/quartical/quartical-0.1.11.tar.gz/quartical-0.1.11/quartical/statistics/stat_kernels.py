import numpy as np
from numba import jit, prange
from quartical.utils.numba import coerce_literal
from quartical.utils.callables import filter_kwargs
from quartical.gains.general.generics import qcgjit_parallel
from quartical.gains.general.convenience import get_dims, get_row
import quartical.gains.general.factories as factories


def compute_mean_presolve_chisq(*args, **kwargs):
    return filter_kwargs(_compute_mean_presolve_chisq)(*args, **kwargs)


@jit(nopython=True, fastmath=True, parallel=True, cache=True, nogil=True)
def _compute_mean_presolve_chisq(data, model, weights, flags):

    n_rows, n_chan, n_dir, n_corr = model.shape

    chisq = 0
    counts = 0

    for row in prange(n_rows):
        tmp = np.empty((n_corr,), dtype=np.complex128)
        for chan in range(n_chan):
            tmp[:] = data[row, chan]
            for dir in range(n_dir):
                for corr in range(n_corr):
                    tmp[corr] -= model[row, chan, dir, corr]
            for corr in range(n_corr):
                if flags[row, chan] != 1:
                    w = weights[row, chan, corr]
                    r = tmp[corr]
                    chisq += (r.conjugate() * w * r).real
                    counts += 1

    if counts:
        chisq /= counts
    else:
        chisq = np.nan

    return np.array([[chisq]], dtype=np.float64)


def compute_mean_postsolve_chisq(*args, **kwargs):
    return filter_kwargs(_compute_mean_postsolve_chisq)(*args, **kwargs)


@qcgjit_parallel
def _compute_mean_postsolve_chisq(
    data,
    model,
    weights,
    flags,
    gains,
    a1,
    a2,
    t_map_arr,
    f_map_arr,
    d_map_arr,
    row_map,
    row_weights,
    corr_mode
):

    coerce_literal(_compute_mean_postsolve_chisq, ["corr_mode"])

    imul_rweight = factories.imul_rweight_factory(corr_mode, row_weights)
    v1_imul_v2 = factories.v1_imul_v2_factory(corr_mode)
    v1_imul_v2ct = factories.v1_imul_v2ct_factory(corr_mode)
    isub = factories.isub_factory(corr_mode)
    iunpack = factories.iunpack_factory(corr_mode)
    valloc = factories.valloc_factory(corr_mode)

    def impl(
        data,
        model,
        weights,
        flags,
        gains,
        a1,
        a2,
        t_map_arr,
        f_map_arr,
        d_map_arr,
        row_map,
        row_weights,
        corr_mode
    ):

        n_rows, n_chan, n_dir, n_corr = get_dims(model, row_map)
        n_gains = len(gains)

        t_map_arr_g = t_map_arr[0]
        f_map_arr_g = f_map_arr[0]

        chisq = 0
        counts = 0

        for row_ind in prange(n_rows):

            row = get_row(row_ind, row_map)
            a1_m, a2_m = a1[row], a2[row]
            r = valloc(np.complex128)  # Hold data.
            v = valloc(np.complex128)  # Hold GMGH.

            for f in range(n_chan):

                if flags[row, f]:
                    continue

                iunpack(r, data[row, f])
                m = model[row, f]
                w = weights[row, f]

                for d in range(n_dir):

                    iunpack(v, m[d])

                    for g in range(n_gains - 1, -1, -1):

                        t_m = t_map_arr_g[row_ind, g]
                        f_m = f_map_arr_g[f, g]
                        d_m = d_map_arr[g, d]  # Broadcast dir.

                        gain = gains[g][t_m, f_m]
                        gain_p = gain[a1_m, d_m]
                        gain_q = gain[a2_m, d_m]

                        v1_imul_v2(gain_p, v, v)
                        v1_imul_v2ct(v, gain_q, v)

                    imul_rweight(v, v, row_weights, row_ind)
                    isub(r, v)

                for c in range(n_corr):
                    chisq += (r[c].conjugate() * w[c] * r[c]).real
                    counts += 1

        if counts:
            chisq /= counts
        else:
            chisq = np.nan

        return np.array([[chisq]], dtype=np.float64)

    return impl
