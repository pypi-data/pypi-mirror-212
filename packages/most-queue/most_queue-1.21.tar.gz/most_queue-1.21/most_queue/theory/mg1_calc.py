import math
from most_queue.sim import rand_destribution as rd
from most_queue.sim.qs_sim import QueueingSystemSimulator
import q_poisson_arrival_calc as q_calc


def get_w(l, b, num=3):
    """
    Расчет начальных моментов времени ожидания для СМО M/G/1
    :param l: интенсивность поступления заявок в СМО
    :param b: нач. моменты времени обслуживания
    :param num: число нач. моментов на выходе
    :return: начальные моменты времени ожидания
    """
    num_of_mom = min(len(b) - 1, num)
    w = [0.0] * (num_of_mom + 1)
    w[0] = 1
    for k in range(1, num_of_mom + 1):
        summ = 0
        for j in range(k):
            summ += math.factorial(k) * b[k - j] * w[j] / (math.factorial(j) * math.factorial(k + 1 - j))
        w[k] = ((l / (1 - l * b[0])) * summ)
    return w[1:]


def get_v(l, b, num=3):
    """
      Расчет начальных моментов времени пребывания для СМО M/G/1
      :param l: интенсивность поступления заявок в СМО
      :param b: нач. моменты времени обслуживания
      :param num: число нач. моментов на выходе
      :return: начальные моменты времени пребывания
    """
    num_of_mom = min(len(b) - 1, num)

    w = get_w(l, b, num_of_mom)
    v = []
    v.append(w[0] + b[0])
    if num_of_mom > 1:
        v.append(w[1] + 2 * w[0] * b[0] + b[1])
    if num_of_mom > 2:
        v.append(w[2] + 3 * w[1] * b[0] + 3 * b[1] * w[0] + b[2])

    return v


def get_p(l, b, num=100, dist_type="Gamma"):
    """
      Расчет вероятностей состояний для СМО M/G/1
      l: интенсивность поступления заявок в СМО
      b: нач. моменты времени обслуживания
      num: число вероятностей состояний на выходе
      dist_type: тип распределения времени обслуживания
    """

    if dist_type == "Gamma":
        gamma_param = rd.Gamma.get_mu_alpha(b)
        q = q_calc.get_q_Gamma(l, gamma_param[0], gamma_param[1], num)
    elif dist_type == "Uniform":
        uniform_params = rd.Uniform_dist.get_params(b)
        q = q_calc.get_q_uniform(l, uniform_params[0], uniform_params[1], num)
    elif dist_type == "Pa":
        alpha, K = rd.Pareto_dist.get_a_k(b)
        q = q_calc.get_q_Pareto(l, alpha, K, num)
    else:
        print("Error in get_p. Unknown type of distribution")
        return 0

    p = [0.0] * num
    p[0] = 1 - l * b[0]
    for i in range(1, num):
        summ = 0
        for j in range(1, i):
            summ += p[j] * q[i - j]
        p[i] = (p[i - 1] - p[0] * q[i - 1] - summ) / q[0]
    return p


if __name__ == '__main__':
    from most_queue.utils.tables import times_print, probs_print

    l = 1
    b1 = 0.9
    coev = 1.6
    num_of_jobs = 800000

    params = rd.H2_dist.get_params_by_mean_and_coev(b1, coev)
    b = rd.H2_dist.calc_theory_moments(*params, 4)
    w_ch = get_w(l, b)
    p_ch = get_p(l, b, 100)

    qs = QueueingSystemSimulator(1)
    qs.set_servers(params, "H")
    qs.set_sources(l, "M")
    qs.run(num_of_jobs)
    w_im = qs.w
    p_im = qs.get_p()

    times_print(w_im, w_ch, True)

    v_ch = get_v(l, b)
    v_im = qs.v

    times_print(v_im, v_ch, False)

    probs_print(p_im, p_ch, 10)

    params = rd.Uniform_dist.get_params_by_mean_and_coev(b1, coev)
    b = rd.Uniform_dist.calc_theory_moments(*params, 4)
    w_ch = get_w(l, b)
    p_ch = get_p(l, b, 100, dist_type="Uniform")

    qs = QueueingSystemSimulator(1)
    qs.set_servers(params, "Uniform")
    qs.set_sources(l, "M")
    qs.run(num_of_jobs)
    w_im = qs.w
    p_im = qs.get_p()

    times_print(w_im, w_ch, True)

    v_ch = get_v(l, b)
    v_im = qs.v

    times_print(v_im, v_ch, False)

    probs_print(p_im, p_ch, 10)

    a, K = rd.Pareto_dist.get_a_k_by_mean_and_coev(b1, coev)
    b = rd.Pareto_dist.calc_theory_moments(a, K, 4)
    w_ch = get_w(l, b)
    p_ch = get_p(l, b, 100, dist_type="Pa")

    qs = QueueingSystemSimulator(1)
    qs.set_servers([a, K], "Pa")
    qs.set_sources(l, "M")
    qs.run(num_of_jobs)
    w_im = qs.w
    p_im = qs.get_p()

    times_print(w_im, w_ch, True)

    v_ch = get_v(l, b)
    v_im = qs.v

    times_print(v_im, v_ch, False)

    probs_print(p_im, p_ch, 10)

