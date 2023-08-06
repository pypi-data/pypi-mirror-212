#Copyright 2023 Federica Castino
#Licensed under GNU LGPL-3.0-or-later

from numpy import argmin, argsort, sqrt, sum, where, empty


class Target:
    """
    A class used to identify the Pareto optimal solution closest
    to a target percentage change in one of the objective functions.
    """

    def __init__(self):
        pass

    @staticmethod
    def rel_change(v):
        """
        Calculate relative change w.r.t. minimum value of objective

        :param v: values of objective function at each pareto opt. solution
        :type v: numpy.ndarray
        :return: relative change w.r.t. minimum value of v
        :rtype: numpy.ndarray
        """
        return 100 * ((v - min(v)) / min(v))

    def solution_found_with_target(self, x, v):
        """
        Identify solution closest to x% increase in objective v

        :param x: target percentage change
        :type x: float
        :param v: values of objective function at each pareto opt. solution
        :type v: numpy.ndarray
        :return: index of identified solution
        :rtype: numpy.int64
        """
        return argmin(abs(self.rel_change(v) - x))


class GRA:
    """
    A class used to identify the Pareto optimal solution
    using the Gray Relational Analysis (GRA).
    """

    def __init__(self):
        pass

    @staticmethod
    def norm_gra_min(v):
        """
        Normalize values of objective function to be minimized

        :param v: values of objective function
        :type v: numpy.ndarray
        :return: normalized v
        :rtype: numpy.ndarray
        """

        return (max(v) - v) / (max(v) - min(v))

    @staticmethod
    def dist_gra(v):
        """
        Calculate distance as defined in Gray Relational Analysis (GRA)

        :param v: values of i^th objective
        :type v: numpy.ndarray
        :return: distances from maximum value of v
        :rtype: numpy.ndarray
        """

        return abs(max(v) - v)

    @staticmethod
    def grc(distances, n_sol):
        """
        Calculate Gray Relational Coefficient (GRC)

        :param distances: distances from maximum value of v
        :type distances: numpy.ndarray
        :param n_sol: number of Pareto optimal solutions
        :type n_sol: int
        :return: GRC for each solution
        :rtype: numpy.ndarray
        """

        args = empty(len(distances), dtype=object)
        for i in range(len(args)):
            args[i] = (min(distances[i]) + max(distances[i])) / (distances[i] + max(distances[i]))
        return (1 / n_sol) * (sum(args, axis=0))

    @staticmethod
    def pref_gra(grc):
        """
        Identify solution with the largest Gray Relational Coefficient (GRC)

        :param grc: values of Gray Relational Coefficient for each solution
        :type grc: numpy.ndarray
        :return: index of solution maximizing GRC
        :rtype: int
        """

        return where(grc == max(grc))[0].item(0)

    def solution_found_by_gra(self, pobj):
        """
        Select a single solution among the Pareto optimal solutions using
        Gray Relational Analysis (GRA)

        :param pobj: values of objective functions
        :type pobj: numpy.ndarray
        :return: index of identified solution
        :rtype: int
        """
        number_objectives = len(pobj)
        normalized_pobj = empty(number_objectives, dtype=object)
        dist_to_reference = empty(number_objectives, dtype=object)

        for i in range(number_objectives):
            normalized_pobj[i] = self.norm_gra_min(pobj[i])
            dist_to_reference[i] = self.dist_gra(normalized_pobj[i])

        grc = self.grc(dist_to_reference, len(pobj[0]))
        return self.pref_gra(grc)


class TOPSIS:
    """
    A class used to identify the Pareto optimal solution
    using the Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS).
    """

    def __init__(self):
        pass

    @staticmethod
    def norm_topsis(w, v):
        """
        Normalize and weight values of objective function

        :param w: relative weight assigned to objective v
        :type w: float
        :param v: values of objective function
        :type v: numpy.ndarray
        :return: normalized and weighted values of v
        :rtype: numpy.ndarray
        """
        norm_v = v / (sqrt(sum(v * v)))
        return w * norm_v

    @staticmethod
    def dist_pis_topsis(v):
        """
        Calcluate distance of each solution to the Positive Ideal Solution (PIS)

        :param v: values of objective function
        :type v: numpy.ndarray
        :return: distances form PIS
        :rtype: numpy.ndarray
        """
        args = empty(len(v), dtype=object)
        for i in range(len(args)):
            args[i] = (v[i] - min(v[i])) ** 2
        return sqrt(sum(args, axis=0))

    @staticmethod
    def dist_nis_topsis(v):
        """
        Calcluate distance of each solution to the Negative Ideal Solution (NIS)

        :param v: values of objective function
        :type v: numpy.ndarray
        :return: distances form NIS
        :rtype: numpy.ndarray
        """
        args = empty(len(v), dtype=object)
        for i in range(len(args)):
            args[i] = (v[i] - max(v[i])) ** 2
        return sqrt(sum(args, axis=0))

    @staticmethod
    def closeness(dist_nis, dist_pis):
        """
        Calculate Closeness parameter

        :param dist_nis: distances form negative ideal solution
        :type dist_nis: numpy.ndarray
        :param dist_pis: distances from positive ideal solution
        :type dist_pis: numpy.ndarray
        :return: closeness parameters for each solution
        :rtype: numpy.ndarray
        """
        return dist_nis / (dist_nis + dist_pis)

    @staticmethod
    def pref_topsis(c):
        """
        Identify solution with largest value of the closeness parameter

        :param c: closeness parameter
        :type c: numpy.ndarray
        :return: index of identified solution
        :rtype: int
        """
        return where(c == max(c))[0].item(0)

    def solution_found_by_topsis(self, pobj, weights):
        """
        Select a single solution among the Pareto optimal solutions using
        Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS)

        :param pobj: values of optimization objective functions
        :type pobj: numpy.ndarray
        :param weights: relative weights of objective functions
        :type weights: list
        :return: index of solution found using TOPSIS
        :rtype: int
        """
        number_objectives = len(pobj)
        normalized_pobj = empty(number_objectives, dtype=object)

        for i in range(number_objectives):
            normalized_pobj[i] = self.norm_topsis(weights[i], pobj[i])

        distance_pis = self.dist_pis_topsis(normalized_pobj)
        distance_nis = self.dist_nis_topsis(normalized_pobj)

        c = self.closeness(distance_nis, distance_pis)
        return self.pref_topsis(c)


class VIKOR:
    """
    A class used to identify the Pareto optimal solution
    using the Viekriterijumsko Kompromisno Rangiranje (VIKOR) method.
    """

    def __init__(self):
        pass

    @staticmethod
    def dist_s_vikor(w, v):
        """
        Calculate utility measure (S)

        :param w: relative weights of optimization objectives
        :type w: list
        :param v: values of objective functions
        :type v: numpy.ndarray
        :return: values of the parameter S
        :rtype: numpy.ndarray
        """
        args = empty(len(v), dtype=object)
        for i in range(len(args)):
            args[i] = w[i] * (min(v[i]) - v[i]) / (min(v[i]) - max(v[i]))
        return sum(args, axis=0)

    @staticmethod
    def dist_r_vikor(w, v):
        """
        Calculate regret measure (R)

        :param w: relative weights of optimization objectives
        :type w: list
        :param v: values of objective functions
        :type v: numpy.ndarray
        :return: values of the parameter R
        :rtype: numpy.ndarray
        """
        out = []
        for j in range(len(v[0])):
            args = []
            for i in range(len(v)):
                args.append(w[i] * (min(v[i]) - v[i][j]) / (min(v[i]) - max(v[i])))
            out.append(max(args))
        return out

    @staticmethod
    def q_vikor(gamma, s, r):
        """
        Calculate parameter Q, combining S and R

        :param gamma: relative importance of group utility
        :type gamma: float
        :param s: values of the parameter S
        :type s: numpy.ndarray
        :param r: values of the parameter R
        :type r: numpy.ndarray
        :return: values of the parameter Q
        :rtype: numpy.ndarray
        """
        arg1 = (s - min(s)) / (max(s) - min(s))
        arg2 = (r - min(r)) / (max(r) - min(r))
        return gamma * arg1 + (1 - gamma) * arg2

    @staticmethod
    def pref_vikor(q, dist_s, dist_r):
        """
        Rank solutions and use conditions of
        acceptable advantage and stability

        :param q: values of the parameter Q
        :type q: numpy.ndarray
        :param dist_s: values of the parameter Q
        :type dist_s: numpy.ndarray
        :param dist_r: values of the parameter Q
        :type dist_r: numpy.ndarray
        :return: index/indices of recommended solution(s)
        :rtype: list
        """

        rank_q = argsort(q)
        rec_sol_index = []

        # First condition: acceptable advantage

        advantage = dist_r[rank_q[1]] - dist_r[rank_q[0]]
        limit = 1 / (len(q) - 1)
        rec_sol_index.append(rank_q[0])

        if advantage >= limit:
            print(rank_q[0], ': this is the only recommended solution')

        else:

            # print(rank_Q[0], ': one of the recommended solutions')
            for i in range(len(q) - 2):
                d = i + 2
                advantage = dist_r[rank_q[d - 1]] - dist_r[rank_q[0]]
                limit = 1 / (d - 1)

                if advantage < limit:

                    rec_sol_index.append(rank_q[d - 1])
                    # print(rank_Q[d-1], ': : one of the recommended solutions')
                else:
                    break
                    # print(rank_Q[d], ': previous solution is last recommended solution')

        # Second condition: acceptable stability

        if len(rec_sol_index) == 1:
            if dist_r[rank_q[0]] == min(dist_r) and dist_s[rank_q[0]] == min(dist_s):
                print('stable solution -> this is the only recommended solution')
            else:
                rec_sol_index.append(rank_q[1])
                # print('unstable solution -> two solutions are recommended')

        # print('The preferred optimal solution(s) is(are) with index:', rec_sol_index)
        return rec_sol_index

    @staticmethod
    def single_vikor(pobj, weights, set_sol_selected_by_vikor):
        """
        Select a single solution among the set of solutions
        identified with the VIKOR method

        :param pobj: values of objective function
        :type pobj: numpy.ndarray
        :param weights: relative importance of optimization objectives
        :type weights: list
        :param set_sol_selected_by_vikor: indices of solutions selected by VIKOR
        :type set_sol_selected_by_vikor: list
        :return: index of selected solution
        :rtype: int
        """
        index_min_weight = weights.index(min(weights))
        return pobj[index_min_weight].tolist().index(min(pobj[index_min_weight][set_sol_selected_by_vikor]))

    def solution_found_by_vikor(self, pobj, gamma, weights):
        """
        Select a set of solutions among the Pareto optimal solutions using
        the Viekriterijumsko Kompromisno Rangiranje (VIKOR) method

        :param pobj: values of objective function
        :type pobj: numpy.ndarray
        :param gamma: relative importance of group utility
        :type gamma: float
        :param weights: relative importance of optimization objectives
        :type weights: list
        :return: set of solutions, single solution selected by VIKOR
        :rtype: list, int
        """

        distance_s = self.dist_s_vikor(weights, pobj)
        distance_r = self.dist_r_vikor(weights, pobj)
        q = self.q_vikor(gamma, distance_s, distance_r)
        set_sol_selected_by_vikor = self.pref_vikor(q, distance_s, distance_r)
        single_sol_found_by_vikor = self.single_vikor(pobj, weights, set_sol_selected_by_vikor)

        return set_sol_selected_by_vikor, single_sol_found_by_vikor


class VikorTarget:
    """
    A class used to identify the Pareto optimal solution
    using the Viekriterijumsko Kompromisno Rangiranje (VIKOR) method,
    while constraining the increase in one of the objectives
    """

    def __init__(self):
        pass

    @staticmethod
    def solution_found_by_vikor_target(pobj, gamma, weights, index_limited_obj, x):
        """
        Select a solution with VIKOR.
        If the resulting change in one of the objectives is larger than a threshold,
        then pick the solution closest to such threshold instead.

        :param pobj: values of objective function
        :type pobj: numpy.ndarray
        :param gamma: relative importance of group utility
        :type gamma: float
        :param weights: relative importance of optimization objectives
        :type weights: list
        :param index_limited_obj: index of the objective to be constrained
        :type index_limited_obj: int
        :param x: target/threshold relative change of objective
        :type x: float
        :return: index of selected solution
        :rtype: int
        """

        set_solutions, single_selected_solution = VIKOR.solution_found_by_vikor(VIKOR(), pobj, gamma, weights)
        relative_change = Target.rel_change(pobj[index_limited_obj])

        if relative_change[single_selected_solution] > x:
            single_selected_solution = Target.solution_found_with_target(Target(), x, pobj[index_limited_obj])

        return single_selected_solution
