# coding=gbk
import math
import random
from operator import itemgetter

from design_calculation import data_list
from optimize.KO_loss import KO_loss
from optimize.compRotorin import compRotorin


class Gene:
    """
    This is a class to represent individual(Gene) in GA algorithom
    each object of this class have two attribute: data, size
    """

    def __init__(self, **data):
        self.__dict__.update(data)
        self.size = len(data['data'])  # length of gene


class GA:
    """
    This is a class of GA algorithm.
    """

    def __init__(self, parameter):
        """
        Initialize the pop of GA algorithom and evaluate the pop by computing its' fitness value.
        The data structure of pop is composed of several individuals which has the form like that:

        {'Gene':a object of class Gene, 'fitness': 1.02(for example)}
        Representation of Gene is a list: [b s0 u0 sita0 s1 u1 sita1 s2 u2 sita2]

        """
        # parameter = [CXPB, MUTPB, NGEN, popsize, low, up]
        self.parameter = parameter

        low = self.parameter[4]
        up = self.parameter[5]

        self.bound = []
        self.bound.append(low)
        self.bound.append(up)

        pop = []
        for i in range(self.parameter[3]):
            geneinfo = []
            for pos in range(len(low)):
                geneinfo.append(self.bound[0][pos] + random.randint(0, 50) * (
                        self.bound[1][pos] - self.bound[0][pos]) / 50)  # initialise popluation

            fitness = self.evaluate(geneinfo)  # evaluate each chromosome
            pop.append({'Gene': Gene(data=geneinfo), 'fitness': fitness})  # store the chromosome and its fitness

        self.pop = pop
        self.bestindividual = self.selectBest(self.pop)  # store the best chromosome in the population
        # print(self.bestindividual)

    # The parameters here need to be changed
    def evaluate(self, geneinfo):
        """
        fitness function
        """
        num = Zr
        Stator_alpha2_tmp = [0 for i in range(num)]
        P1_tmp = [0 for i in range(num)]
        Ma1_tmp = [0 for i in range(num)]
        Rotor_alpha2_tmp = [0 for i in range(num)]
        P2_tmp = [0 for i in range(num)]
        Ma2_tmp = [0 for i in range(num)]
        for i in range(num):
            Stator_alpha2_tmp[i] = geneinfo[i]  # ��Ҷ����������
            P1_tmp[i] = geneinfo[i + num]  # ��Ҷ����ѹ��
            Ma1_tmp[i] = geneinfo[i + num * 2]  # ��Ҷ���������
            Rotor_alpha2_tmp[i] = geneinfo[i + num * 3]  # ��Ҷ����������
            P2_tmp[i] = geneinfo[i + num * 4]  # ��Ҷ����ѹ��
            Ma2_tmp[i] = geneinfo[i + num * 5]  # ��Ҷ���������
        y = 0
        for i in range(num):
            rs_hub = Stator_rhub + l1 / (num - 1) * i - 0.5 * l1 / (num - 1)  # ��Ҷÿһ����վ��Ҷ���뾶
            rs_tip = Stator_rhub + l1 / (num - 1) * i + 0.5 * l1 / (num - 1)  # ��Ҷÿһ����վ��Ҷ���뾶
            rr_hub = Rotor_rhub + l2 / (num - 1) * i - 0.5 * l2 / (num - 1)  # ��Ҷÿһ����վ��Ҷ���뾶
            rr_tip = Rotor_rtip + l2 / (num - 1) * i + 0.5 * l2 / (num - 1)  # ��Ҷÿһ����վ��Ҷ���뾶
            Beta1, Mar_in, Pr_in, Tr_in = compRotorin(Stator_alpha1, Stator_alpha2_tmp[i], k, Re, ia, Stator_cons,
                                                      Stator_tD,
                                                      Stator_Bz[i], Stator_tmax[i], Pt0, P1_tmp[i], Tt0, Ma0,
                                                      Ma1_tmp[i], rs_hub, rs_tip,
                                                      n)  # �ĸģ��滻�˺����Ҷ����ز��������������ǡ����������������ѹ���������¶�
            # if i == 0 | i == num:
            # y += 2 * (100 - (KO_loss(Stator_alpha1, Stator_alpha2_tmp[i], k, Re, ia, Stator_cons, o, Stator_Bz[i],
            # Stator_tmax[i], Pt0, P1_tmp[i], Tt0, Ma0, Ma1_tmp[i], rs_hub, rs_tip) +
            # KO_loss(Beta1, Rotor_alpha2_tmp[i], k, Re, ia, Rotor_cons, o, Rotor_Bz[i], Rotor_tmax[i],
            # Pr_in, P2_tmp[i], Tr_in, Mar_in, Ma2_tmp[i], rr_hub, rr_tip)) * 50)
            # else:
            y = y + 100 - (KO_loss(Stator_alpha1, Stator_alpha2_tmp[i], k, Re, ia, Stator_cons, Stator_tD,
                                   Stator_Bz[i],
                                   Stator_tmax[i], Pt0, P1_tmp[i], Tt0, Ma0, Ma1_tmp[i], rs_hub, rs_tip) +
                           KO_loss(Beta1, Rotor_alpha2_tmp[i], k, Re, ia, Rotor_cons, Stator_tD, Rotor_Bz[i],
                                   Rotor_tmax[i],
                                   Pr_in,
                                   P2_tmp[i], Tr_in, Mar_in, Ma2_tmp[i], rr_hub, rr_tip)) * 50

            # y=y+100-20
        # y = y / (num+2)  ע�Ͳ���Ϊ����һ�ּ��㷽�����Ŵ��˶˱ڸ�������վ�ı��أ���Ϊ�˱ڸ�������ʧ�Ƚϴ�
        y = y / num
        return y

    def selectBest(self, pop):
        """
        select the best individual from pop
        """
        s_inds = sorted(pop, key=itemgetter("fitness"), reverse=True)  # from large to small, return a pop
        # pos = 0
        # while math.isnan(s_inds[pos]['fitness']):
        #     pos = pos + 1
        # return s_inds[pos]
        return s_inds[0]

    def selection(self, individuals, kk):
        """
        select some good individuals from pop, note that good individuals have greater probability to be choosen
        for example: a fitness list like that:[5, 4, 3, 2, 1], sum is 15,
        [-----|----|---|--|-]
        012345|6789|101112|1314|15
        we randomly choose a value in [0, 15],
        it belongs to first scale with greatest probability
        """
        s_inds = sorted(individuals, key=itemgetter("fitness"),
                        reverse=True)  # sort the pop by the reference of fitness
        sum_fits = sum(ind['fitness'] for ind in individuals)  # sum up the fitness of the whole pop

        chosen = []
        for i in range(kk):
            u = random.random() * sum_fits  # randomly produce a num in the range of [0, sum_fits], as threshold
            sum_ = 0
            for ind in s_inds:
                sum_ += ind['fitness']  # sum up the fitness
                if sum_ >= u:
                    # when the sum of fitness is bigger than u, choose the one, which means u is in the range of
                    # [sum(1,2,...,n-1),sum(1,2,...,n)] and is time to choose the one ,namely n-th individual in the pop
                    chosen.append(ind)
                    break
        # from small to large, due to list.pop() method get the last element
        chosen = sorted(chosen, key=itemgetter("fitness"), reverse=False)
        return chosen

    def crossoperate(self, offspring):
        """
        cross operation
        here we use two points crossoperate
        for example: gene1: [5, 2, 4, 7], gene2: [3, 6, 9, 2], if pos1=1, pos2=2
        5 | 2 | 4  7
        3 | 6 | 9  2
        =
        3 | 2 | 9  2
        5 | 6 | 4  7
        """
        dim = len(offspring[0]['Gene'].data)

        geninfo1 = offspring[0]['Gene'].data  # Gene's data of first offspring chosen from the selected pop
        geninfo2 = offspring[1]['Gene'].data  # Gene's data of second offspring chosen from the selected pop

        if dim == 1:
            pos1 = 1
            pos2 = 1
        else:
            pos1 = random.randrange(1, dim)  # select a position in the range from 0 to dim-1,
            pos2 = random.randrange(1, dim)

        newoff1 = Gene(data=[])  # offspring1 produced by cross operation
        newoff2 = Gene(data=[])  # offspring2 produced by cross operation
        temp1 = []
        temp2 = []
        for i in range(dim):
            if min(pos1, pos2) <= i < max(pos1, pos2):
                temp2.append(geninfo2[i])
                temp1.append(geninfo1[i])
            else:
                temp2.append(geninfo1[i])
                temp1.append(geninfo2[i])
        newoff1.data = temp1
        newoff2.data = temp2

        return newoff1, newoff2

    def mutation(self, crossoff, bound):
        """
        mutation operation
        """
        dim = len(crossoff.data)

        if dim == 1:
            pos = 0
        else:
            pos = random.randrange(0, dim)  # chose a position in crossoff to perform mutation.

        crossoff.data[pos] = bound[0][pos] + random.randint(0, 50) * (bound[1][pos] - bound[0][pos]) / 50
        return crossoff

    def GA_main(self):
        """
        main frame work of GA
        """
        global generation
        size = self.parameter[3]
        # print("Start of evolution")

        # Begin the evolution
        for g in range(NGEN):

            # print("############### Generation {} ###############".format(g))
            generation = g

            # Apply selection based on their converted fitness
            selectpop = self.selection(self.pop, size)
            # print(self.pop)
            # print(selectpop)

            nextoff = []
            while len(nextoff) != size:
                # Apply crossover and mutation on the offspring

                # Select two individuals
                offspring = [selectpop.pop() for _ in range(2)]

                if random.random() < CXPB:  # cross two individuals with probability CXPB
                    crossoff1, crossoff2 = self.crossoperate(offspring)
                    if random.random() < MUTPB:  # mutate an individual with probability MUTPB
                        muteoff1 = self.mutation(crossoff1, self.bound)
                        muteoff2 = self.mutation(crossoff2, self.bound)
                        fit_muteoff1 = self.evaluate(muteoff1.data)  # Evaluate the individuals
                        fit_muteoff2 = self.evaluate(muteoff2.data)  # Evaluate the individuals
                        nextoff.append({'Gene': muteoff1, 'fitness': fit_muteoff1})
                        nextoff.append({'Gene': muteoff2, 'fitness': fit_muteoff2})
                    else:
                        fit_crossoff1 = self.evaluate(crossoff1.data)  # Evaluate the individuals
                        fit_crossoff2 = self.evaluate(crossoff2.data)
                        nextoff.append({'Gene': crossoff1, 'fitness': fit_crossoff1})
                        nextoff.append({'Gene': crossoff2, 'fitness': fit_crossoff2})
                else:
                    nextoff.extend(offspring)

            # The population is entirely replaced by the offspring
            self.pop = nextoff

            # Gather all the fitnesses in one list and print the stats
            fits = [ind['fitness'] for ind in self.pop]

            best_ind = self.selectBest(self.pop)

            if best_ind['fitness'] > self.bestindividual['fitness']:
                self.bestindividual = best_ind

            # print("Best individual found is {}, {}".format(self.bestindividual['Gene'].data,
            #                                                self.bestindividual['fitness']))  # ��ʷ���
            # print("  Max fitness of current pop: {}".format(max(fits)))  # Ŀǰ���

        # print("------ End of (successful) evolution ------")


generation = 0

CXPB = None
MUTPB = None
NGEN = None
popsize = None

Zr = None
n = None
Dm = None
l1 = None
l2 = None
R = None
Stator_alpha1 = None
Stator_alpha2 = None
k = None
P1 = None
T1 = None
c1 = None
Ma0 = None
Ma1 = None
Stator_rhub = None
Stator_rtip = None
Rotor_alpha2 = None
Rotor_cons = None
Rotor_Bz = None
Rotor_tmax = None
P2 = None
T2 = None
w2 = None
Ma2 = None
Rotor_rhub = None
Rotor_rtip = None

Re = None
Stator_cons = None
ia = None
Stator_tD = None  # �ĸģ��滻�˺��
Rotor_tD = None
Stator_Bz = None
Stator_tmax = None
Pt0 = None
Tt0 = None
D1m = None
D2m = None


# warning ����Ĳ�������ֵ��Ҫ����deepcopy����
# The parameters here need to be changed
def genetic_algorithm_optimize(current_z):
    global CXPB
    global MUTPB
    global NGEN
    global popsize

    global Zr
    global n
    global Dm
    global l1
    global l2
    global R
    global Stator_alpha1
    global Stator_alpha2
    global k
    global P1
    global T1
    global c1
    global Ma0
    global Ma1
    global Stator_rhub
    global Stator_rtip
    global Rotor_alpha2
    global Rotor_cons
    global Rotor_Bz
    global Rotor_tmax
    global P2
    global T2
    global w2
    global Ma2
    global Rotor_rhub
    global Rotor_rtip

    global Re
    global Stator_cons
    global ia
    global Stator_tD  # �ĸģ��滻�˺��
    global Rotor_tD  # �ĸģ��滻�˺��
    global Stator_Bz
    global Stator_Bz
    global Stator_tmax
    global Pt0
    global Tt0
    global D1m
    global D2m

    # CXPB, MUTPB, NGEN, popsize = 0.8, 0.1, 10000, 100  # popsize must be even number
    # The parameters are crossover rate, mutation rate, iteration steps and population number of each generation

    Zr = data_list.Zr  # ����վ��
    n = data_list.n  # ת��
    if data_list.blade_layout_method == 0:
        Dm = data_list.Dm1M[current_z] * 1000  # ƽ��ֱ��
        l1 = data_list.l1M[current_z] * 1000  # ��Ҷ����Ҷ��
        l2 = data_list.l2M[current_z] * 1000  # ��Ҷ����Ҷ��
    elif data_list.blade_layout_method == 1:
        D1m = data_list.Dm1M[current_z] * 1000  # �ģ���Ҷƽ��ֱ��
        D2m = data_list.Dm2M[current_z] * 1000  # �ģ���Ҷƽ��ֱ��
        l1 = data_list.l1M[current_z] * 1000  # ��Ҷ����Ҷ��
        l2 = data_list.l2M[current_z] * 1000  # ��Ҷ����Ҷ��
    # R = 286.96
    R = data_list.R  # ���峣��
    Stator_alpha1 = 90  # ��Ҷ����������
    Stator_alpha2 = data_list.alpha1i[current_z]  # ��Ҷ����������
    # k = 1.33  # �������ָ��
    k = data_list.k

    Re = 500000  # ������ŵ��
    Stator_cons = 1.2  # ��Ҷ���
    ia = -2  # ���ڹ���
    Stator_tD = data_list.Stator_r2[current_z][0] * 2000  # �ĸģ������Ǻ������βԵֱ��,ת���� mm
    Rotor_tD = data_list.Rotor_r2[current_z][0] * 2000  # �ĸģ������Ǻ������βԵֱ��,ת���� mm
    Stator_Bz = data_list.Stator_B[current_z]  # ��Ҷ�����ҳ�
    Stator_Bz = [i * 1000 for i in Stator_Bz]  # ת���� mm ��λ
    Stator_tmax = [i * 0.1 for i in Stator_Bz]  # ��Ҷ�����
    Pt0 = data_list.pt0M[current_z]  # ��Ҷ������ѹ
    Tt0 = data_list.Tt0M[current_z]  # ��Ҷ��������

    P1 = data_list.p1i[current_z]  # ��Ҷ���ھ�ѹ
    T1 = data_list.T1i[current_z]  # ��Ҷ���ھ���
    c1 = data_list.c1i[current_z]

    Ma0 = 0  # ��Ҷ���������
    Ma1 = []  # ��Ҷ���������
    if data_list.blade_layout_method == 0:
        Stator_rhub = Dm / 2 - l1 / 2  # ��ҶҶ���뾶
        Stator_rtip = Dm / 2 + l1 / 2  # ��ҶҶ���뾶
    elif data_list.blade_layout_method == 1:
        Stator_rhub = D1m / 2 - l1 / 2
        Stator_rtip = D1m / 2 + l1 / 2
    Rotor_alpha2 = [90 - data_list.Beta2i[current_z][i] for i in range(len(data_list.Beta2i[current_z]))]
    Rotor_cons = 1.5  # ��Ҷ���
    # Rotor_Bz = [0.0236, 0.0246, 0.0256, 0.0266, 0.0276]  # ��Ҷ�����ҳ�
    Rotor_Bz = data_list.Rotor_B[current_z]
    Rotor_Bz = [i * 1000 for i in Rotor_Bz]  # ת���� mm ��λ
    Rotor_tmax = []  # ��Ҷ����ȣ����ֵ�������ҳ��йأ�Ҳ�Ǵ�֮ǰ����õ��ģ�֮ǰֻ�������в��ģ�ʵ�ʲ�ͬλ�ñ���Ӧ�ò�ͬ����Ҷ����Ҷ����0.2�䵽0.04��֮ǰ�ļ���������󣬼ǵü��һ��
    P2 = data_list.p2i[current_z]  # ��Ҷ���ھ�ѹ
    T2 = data_list.T2i[current_z]  # ��Ҷ���ھ���
    w2 = data_list.w2i[current_z]  # ��Ҷ��������ٶ�
    Ma2 = []  # ��Ҷ���������
    if data_list.blade_layout_method == 0:
        Rotor_rhub = Dm / 2 - l2 / 2  # ��ҶҶ���뾶
        Rotor_rtip = Dm / 2 + l2 / 2  # ��ҶҶ���뾶
    elif data_list.blade_layout_method == 1:
        Rotor_rhub = D2m / 2 - l2 / 2
        Rotor_rtip = D2m / 2 + l2 / 2
    for i in range(Zr):
        Ma1.append(c1[i] / math.sqrt(k * R * T1[i]))
        Ma2.append(w2[i] / math.sqrt(k * R * T2[i]))
        Rotor_tmax.append(Rotor_Bz[i] * (0.2 - (0.2 - 0.04) / (Zr - 1) * i))
    low = [0 for i in range(Zr * 6)]  # 6������
    up = [0 for i in range(Zr * 6)]
    init_individual = [0 for i in range(Zr * 6)]
    for i in range(Zr):
        low[i] = Stator_alpha2[i] - 3  # ��Ҷ���������� # lower range for variables
        low[i + Zr] = P1[i] - 3e4  # ��Ҷ���ھ�ѹ
        low[i + Zr * 2] = Ma1[i] - 0.2  # ��Ҷ���������
        low[i + Zr * 3] = Rotor_alpha2[i] - 3  # ��Ҷ����������
        low[i + Zr * 4] = P2[i] - 3e4  # ��Ҷ���ھ�ѹ
        low[i + Zr * 5] = Ma2[i] - 0.2  # ��Ҷ���������

        up[i] = Stator_alpha2[i] + 3  # upper range for variables
        up[i + Zr] = P1[i] + 3e4
        up[i + Zr * 2] = Ma1[i] + 0.2
        up[i + Zr * 3] = Rotor_alpha2[i] + 3
        up[i + Zr * 4] = P2[i] + 3e4
        up[i + Zr * 5] = Ma2[i] + 0.2

        init_individual[i] = Stator_alpha2[i]
        init_individual[i + Zr] = P1[i]
        init_individual[i + Zr * 2] = Ma1[i]
        init_individual[i + Zr * 3] = Rotor_alpha2[i]
        init_individual[i + Zr * 4] = P2[i]
        init_individual[i + Zr * 5] = Ma2[i]

    parameter = [CXPB, MUTPB, NGEN, popsize, low, up]
    run = GA(parameter)
    init_fitness = run.evaluate(init_individual)
    data_list.init_fitness.append(init_fitness)
    run.GA_main()

    return run.bestindividual
