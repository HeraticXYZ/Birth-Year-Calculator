# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 15:53:38 2019

Author: HeraticXYZ

This program is used to predict exact birth years of ancestors with incomplete
family information. All internal values should be rounded to 6 decimal places,
all values returned to the user should be rounded to 4 decimal places to avoid
rounding problems that present themselves when returning values rounded to 6
decimal places.
"""

import math
import copy
import operator
import matplotlib.pyplot as plt

# Discrete probability functions
"""
Based on fertility graph: Given chance at age range a woman gets pregnant each month. Let's say about 6 [this number is to be changed until the expected value is about 30] months each year are dedicated to making children. Each chance is raised to the power of 6 and assigned to the relevant year. Then each value is adjusted to make the fertility function smoother (a middle value is picked, then "slopes" are added).
"""
births = {
             14:0.02,
             15:0.05,
             16:0.1,
             17:0.2,
             18:0.4,
             19:0.6,
             20:0.9,
             21:0.93,
             22:0.95,
             23:0.97,
             24:0.99,
             25:0.999929,
             26:0.999908,
             27:0.999887,
             28:0.999396,
             29:0.998906,
             30:0.998415,
             31:0.997925,
             32:0.997434,
             33:0.995501,
             34:0.993568,
             35:0.991635,
             36:0.989702,
             37:0.987769,
             38:0.976472,
             39:0.965174,
             40:0.953876,
             41:0.942578,
             42:0.931280,
             43:0.798006,
             44:0.664732,
             45:0.531457,
             46:0.398183,
             47:0.264908,
             48:0.176605,
             49:0.088303,
             50:0.02,
             51:0.0105,
             52:0.01,
             53:0.005
         }


male_births = {
                15:0.3,
                16:0.5,
                17:0.9,
                18:0.9,
                19:0.95,
                20:0.95,
                21:0.999993,
                22:0.999992,
                23:0.999971,
                24:0.999950,
                25:0.999929,
                26:0.999908,
                27:0.999887,
                28:0.999396,
                29:0.998906,
                30:0.998415,
                31:0.997925,
                32:0.997434,
                33:0.995501,
                34:0.993568,
                35:0.991635,
                36:0.989702,
                37:0.987769,
                38:0.976472,
                39:0.965174,
                40:0.953876,
                41:0.942578,
                42:0.931280,
                43:0.798006,
                44:0.664732,
                45:0.531457,
                46:0.398183,
                47:0.333333,
                48:0.30,
                49:0.25,
                50:0.22,
                51:0.20,
                52:0.18,
                53:0.15,
                54:0.12,
                55:0.10,
                56:0.08,
                57:0.06,
                59:0.05, 
                60:0.05,
                61:0.05,
                62:0.05,
                63:0.05,
                64:0.05,
                65:0.05,
                66:0.05,
                67:0.05, 
                68:0.05,
                69:0.05,
                70:0.05,     
         }


# old test before GEDCOM reading developed
"""
tree = {'agueda c':[[], [], {}, 'F'],
        'andrea bc':[['agueda c'], [], {}, 'F'],
        'vicente rb':[['andrea bc'], [], {1790:1.0}, 'M'],
        'ynes rb':[['andrea bc'], [], {1796:1.0}, 'F'],
        'antonia rb':[['andrea bc'], [], {1800:1.0}, 'F'],
        'juana francisca rb':[['andrea bc'], [], {1804:1.0}, 'F'],
        'manuel bc':[['agueda c'], [], {}, 'M'],
        'juan bs':[['manuel bc'], [], {1789:1.0}, 'M'],
        'eusebio bs':[['manuel bc'], [], {1791:1.0}, 'M'],
        'juana bs':[['manuel bc'], [], {1793:1.0}, 'F'],
        'antonia bs':[['manuel bc'], [], {1796:1.0}, 'F'],
        'damian bs':[['manuel bc'], [], {1800:1.0}, 'M'],
        'petrona bs':[['manuel bc'], [], {1803:1.0}, 'F'],
        'candelaria bs':[['manuel bc'], [], {1805:1.0}, 'F'],
        'domingo bs':[['manuel bc'], [], {1812:1.0}, 'M'],
        'jorge bc':[['agueda c'], [], {}, 'M'],
        'tomas br':[['jorge bc'], [], {1790:1.0}, 'M'],
        'jose manuel br':[['jorge bc'], [], {1796:1.0}, 'M'],
        'andres br':[['jorge bc'], [], {1797:1.0}, 'M'],
        'francisco br':[['jorge bc'], [], {1799:1.0}, 'M'],
        'roberto br':[['jorge bc'], [], {1803:1.0}, 'M'],
        'miguel bc':[['agueda c'], [], {1762:1.0}, 'M'],
        'fermin bc':[['agueda c'], [], {}, 'M'],
        'felix bv':[['fermin bc'], [], {1794:1.0}, 'M'],
        'barbara bv':[['fermin bc'], [], {1796:1.0}, 'F'],
        'manuel bv':[['fermin bc'], [], {1798:1.0}, 'M'],
        'juana bv':[['fermin bc'], [], {1799:1.0}, 'F'],
        'catalina bv':[['fermin bc'], [], {1802:1.0}, 'F'],
        'toribio br':[['fermin bc'], [], {1803:1.0}, 'M'],
        'juana francisca bv':[['fermin bc'], [], {1810:1.0}, 'F'],
        'clemente bc':[['agueda c'], [], {}, 'M'],
        'catalina bm':[['clemente bc'], [], {1795:1.0}, 'F'],
        'manuela bm':[['clemente bc'], [], {1797:1.0}, 'F'],
        'francisco bm':[['clemente bc'], [], {1798:1.0}, 'M'],
        'pedro bc':[['agueda c'], [], {}, 'M'],
        'miguel pbv':[['pedro bc'], [], {1792:1.0}, 'M'],
        'norberta pbv':[['pedro bc'], [], {1794:1.0}, 'F'],
        'juan pbv':[['pedro bc'], [], {1796:1.0}, 'M'],
        'maria jose pbv':[['pedro bc'], [], {1798:1.0}, 'F'],
        'maria antonia pbv':[['pedro bc'], [], {1800:1.0}, 'F'],
        'sebastian pbv':[['pedro bc'], [], {1803:1.0}, 'M'],
        'fernando pbv':[['pedro bc'], [], {1805:1.0}, 'M'],
        'damian pbv':[['pedro bc'], [], {1807:1.0}, 'M'],
        'tomasa pbv':[['pedro bc'], [], {1810:1.0}, 'F'],
        'juan eva pbv':[['pedro bc'], [], {1812:1.0}, 'M'],
        'hipolito bc':[['agueda c'], [], {}, 'M'],
        'ysabel hbv':[['hipolito bc'], [], {1791:1.0}, 'F'],
        'antolino hbv':[['hipolito bc'], [], {1797:1.0}, 'M'],
        'juan hbv':[['hipolito bc'], [], {1800:1.0}, 'M'],
        'jose bc':[['agueda c'], [], {}, 'M'],
        'vicente bm':[['jose bc'], [], {1796:1.0}, 'M'],
        'barbara ba':[['jose bc'], [], {1801:1.0}, 'F'],
        'carmen ba':[['jose bc'], [], {1803:1.0}, 'F'],
        'manuel antonio ba':[['jose bc'], [], {1805:1.0}, 'M'],
        'felipa cruz ba':[['jose bc'], [], {1813:1.0}, 'F'],
        'juan santos ba':[['jose bc'], [], {1818:1.0}, 'M'],
        'josefa gabriela ba':[['jose bc'], [], {1821:1.0}, 'F'],
        'maria gracia ba':[['jose bc'], [], {1823:1.0}, 'F'],
        'lucas bc':[['agueda c'], [], {}, 'M'],
        'ramon lbv':[['lucas bc'], [], {1801:1.0}, 'M'],
        'micaela lbv':[['lucas bc'], [], {1804:1.0}, 'F'],
        'marcelina lbv':[['lucas bc'], [], {1806:1.0}, 'F'],
        'maria camila lbv':[['lucas bc'], [], {1808:1.0}, 'F'],
        'marcos lbv':[['lucas bc'], [], {1813:1.0}, 'M'],
        'basilio lbv':[['lucas bc'], [], {}, 'M'],
        'domingo bd':[['basilio lbv'], [], {1850:1.0}, 'M'],
        'leon bc':[['agueda c'], [], {1788:1.0}, 'M'],
        'catalina bc':[['agueda c'], [], {1790:1.0}, 'F'],
        }
"""

"""
alvarez_tree = {
    'petrona':[[], [], {}],
    'antonio':[['petrona'], [], {1817:1.0}],
    'julian':[['petrona'], [], {1822:1.0}],
    'tomasa':[['petrona'], [], {1827:1.0}],
    'marcelina':[['petrona'], [], {1831:1.0}],
    'guillermo':[['petrona'], [], {1841:1.0}],
    'concepcion':[['petrona'], [], {1843:1.0}],
    'cristina':[['petrona'], [], {1845:1.0}],
}
"""

def logify(func):
    log_func = {}
    for year in func:
        log_func[year] = math.log(func[year])
    return log_func

def unlogify(log_func):
    func = {}
    for year in log_func:
        func[year] = math.exp(log_func[year])
    return func

def scale(func, coeff):
    """
    Multiplies all values within the function by a coefficient.
    """
    scaled_func = {}
    for year in func:
        scaled_func[year] = func[year]*coeff
    return scaled_func

def log_scale(log_func, coeff):
    """
    Multiplies all values within a log function by a coefficient.
    """
    scaled_func = {}
    log_coeff = -math.log(coeff)
    for year in log_func:
        scaled_func[year] = log_func[year] + log_coeff
    return scaled_func

def integrate(func):
    """
    Sums all values found in a function, rescaled functions should return 1.0 
    """
    total = 0.0
    for year in func:
        total += func[year]
    return total

def log_integrate(log_func):
    """
    Sums all values found in a log_function
    """
    total = 0.0
    for year in log_func:
        total += math.exp(log_func[year])
    return total

def rescale(func, cycles):
    """
    Scales a function by the reciprocal of its integral, so that its integral
    equals 1 and it becomes a proper probability function.
    """
    new_func = copy.deepcopy(func)
    for i in range(cycles):
        coeff = 1.0 / integrate(new_func)
        new_func = scale(new_func, coeff)
    return new_func

def log_rescale(func, cycles):
    new_func = copy.deepcopy(func)
    for i in range(cycles):
        coeff = log_integrate(new_func)
        new_func = log_scale(new_func, coeff)
    return new_func

def unifunc(y1, y2):
    unifunc = {}
    for year in range(y1, y2+1):
        unifunc[year] = 1
    return rescale(unifunc, 2)

# def log unifunc(y1, y2):
# male_births = unifunc(16, 80)

neg_births = {}
for age in births:
    neg_births[-age] = births[age]

births = rescale(births, 2)
neg_births = rescale(neg_births, 2)

neg_male_births = {}
for age in male_births:
    neg_male_births[-age] = male_births[age]

male_births = rescale(male_births, 2)
neg_male_births = rescale(neg_male_births, 2)

births = logify(births)
neg_births = logify(neg_births)
male_births = logify(male_births)
neg_male_births = logify(neg_male_births)

# print(log_integrate(births))

def combine(func1, func2):
    """
    Multiplies function2 into function1, restricting their distributions to
    one that complies with each original function. Rescaling the result
    conditions the function on the fact that all input functions must happen.
    """
    func3 = {}
    for year in func1:
        if year in func2:
            func3[year] = func1[year]*func2[year]
    return func3

def log_combine(func1, func2):
    func3 = {}
    for year in func1:
        if year in func2:
            func3[year] = func1[year] + func2[year]
    return func3

# artifact of ancient development
"""
def shift_func(func, s):
    shifted = {}
    for year in func:
        shifted[year + s] = func[year]
    return shifted
"""

def apply_func(func, app_func):
    new_func = {}
    for y1 in func:
        for y2 in app_func:
            if y1+y2 in new_func:
                new_func[y1+y2] += func[y1]*app_func[y2]
            else:
                new_func[y1+y2] = func[y1]*app_func[y2]
    return rescale(new_func, 2)

def log_apply_func(func, app_func):
    new_func = {}
    for y1 in func:
        for y2 in app_func:
            if y1+y2 in new_func:
                new_func[y1+y2] += math.exp(func[y1]+app_func[y2])
            else:
                new_func[y1+y2] = math.exp(func[y1]+app_func[y2])
    return logify(rescale(new_func, 2))

def exp_val(func):
    is_log = False
    for year in func:
        if func[year] < 0:
            is_log = True
    if is_log:
        exp_val = 0
        for year in func:
            exp_val += round(year*math.exp(func[year]), 6)
        return round(exp_val, 4)
    else:
        exp_val = 0
        for year in func:
            exp_val += round(year*func[year], 6)
        return round(exp_val, 4)


"""
def build_children(tree):
    print('Fixing some things...')
    for person in tree:
        for cand in tree:
            if person in tree[cand][0]:
                tree[person][1].append(cand)
    return tree
"""

# old shake function
"""
def shake(unshaken_tree, cycles):
    tree = copy.deepcopy(unshaken_tree)
    for i in range(cycles):
        for person in tree:
            if tree[person][2] != {}:
                base_func = tree[person][2]
                exp_base_func = apply_func(base_func, neg_births)
                for parent in tree[person][0]:
                    if unshaken_tree[parent][2] != {}:
                        break
                    if tree[parent][2] == {}:
                        tree[parent][2] = exp_base_func
                    else:
                        tree[parent][2] = rescale(combine(tree[parent][2], exp_base_func), 2)
                exp_base_func = apply_func(base_func, births)
                for child in tree[person][1]:
                    if unshaken_tree[child][2] != {}:
                        break
                    child_func = tree[child][2]
                    if child_func == {}:
                        tree[child][2] = exp_base_func
                    else:
                        tree[child][2] = rescale(combine(tree[child][2], exp_base_func), 2)
                    exp_birth = round(exp_val(tree[child][2]))
                    weight = 0.0
                    if exp_birth in child_func:
                        weight = child_func[exp_birth]
                    #prevents siblings born on same year
                    for sibling in tree[person][1]:
                        if sibling != child and exp_birth in tree[sibling][2]:
                            tree[sibling][2][exp_birth] *= 1.0 - weight**2
                        if sibling != child and exp_birth-1 in tree[sibling][2]:
                            tree[sibling][2][exp_birth-1] *= 1.0 - weight**2/2.0
                        if sibling != child and exp_birth+1 in tree[sibling][2]:
                            tree[sibling][2][exp_birth+1] *= 1.0 - weight**2/2.0
        if (i+1)%(cycles/10) == 0:
            print(str(round(100*(i+1)/cycles))+'% complete')
    return tree
"""

# old shake function 2.0
"""
def pulse_return(person, tree, wave):
    for i in range(4, len(tree[person])):
        blacklist = tree[person][i][0]
        blacklist.append(person)
        pkg_func = tree[person][i][1]
        if tree[person][0] != []:
            for parent in tree[person][0]:
                if parent not in blacklist:
                    if tree[parent][3] == 'F':
                        tree[parent].append([blacklist, apply_func(pkg_func, neg_births)])
                    else:
                        tree[parent].append([blacklist, apply_func(pkg_func, neg_male_births)])
                    wave.append(parent)
        if tree[person][1] != []:
            for child in tree[person][1]:
                if child not in blacklist:
                    if tree[person][3] == 'F':
                        tree[child].append([blacklist, apply_func(pkg_func, births)])
                    else:
                        tree[child].append([blacklist, apply_func(pkg_func, male_births)])
                    wave.append(child)
        if tree[person][2] == {}:
            tree[person][2] = pkg_func
        else:
            tree[person][2] = rescale(combine(tree[person][2], pkg_func), 2)
    tree[person] = tree[person][0: 4]
    wave.remove(person)

def shake(unshaken_tree):
    print('Shaking tree...')
    tree = copy.deepcopy(unshaken_tree)
    anchors = [person for person in unshaken_tree if unshaken_tree[person][2] != {}]
    for person in anchors:
        blacklist = copy.copy(anchors)
        blacklist.remove(person)
        tree[person].append([blacklist, unshaken_tree[person][2]])
        wave = [person]
        pulse_return(person, tree, wave)
        while wave != []:
            wave_copy = copy.copy(wave)
            for head in wave_copy:
                pulse_return(head, tree, wave)
    return tree
"""

# testing manually constructed tree
"""
full_tree = build_children(tree)
final_tree = shake(full_tree)

for person in final_tree:
    pfunc = final_tree[person][2]
    if len(pfunc) != 1:
        print(person)
        year = round(exp_val(pfunc))
        print(str(year) + ' | ' + str(round(100*pfunc[year])) + '%')
        #print(final_tree[person][2])
    if person == 'agueda c':
        fig = plt.figure(figsize=(10, 6))
        plt.plot(*zip(*sorted(pfunc.items())))
        fig.savefig('agueda_cruz.png')
"""

# proves order of expansions does not matter
"""
tree1 = apply_func(births, births)
tree1 = apply_func(tree1, neg_births)

tree2 = apply_func(births, neg_births)
tree2 = apply_func(tree2, births)

print(tree1)
print(tree2)
"""

# print(final_tree['agueda c'][2])
# print(integrate(final_tree['agueda c'][2]))


"""
fem_births = rescale(fertility)
print(exp_val(fem_births))


#print(integrate(rescale(fem_births)))
om = fem_births
am = fem_births

omm = rescale(apply_func(fem_births, om))

amm = rescale(apply_func(fem_births, am))
ammm = rescale(apply_func(fem_births, amm))

ommxammm = rescale(combine(omm, ammm))

print(exp_val(omm))
print(exp_val(ammm))
old = exp_val(ommxammm)
print(old)
print(round(old))
print(round(old/2))
print(round(old/3))

"""

# func2 = shift_func(fem_births, 5)
# func3 = rescale(combine(func1, func2))
# ext_func = apply_func(func3, func1)

# print(integrate(func1))
# print(exp_val(func1))
# print(ext_func)
# print(exp_val(ext_func))

# gedcom section

print("Female gen gap: "+str(exp_val(births)))
print("Male gen gap: "+str(exp_val(male_births)))

gedcom_file = open('Alvarez Family Tree.ged', 'r')
gedcom = gedcom_file.read()
gedcom = gedcom.split('\n')
# list of line-strings
focus = input("What is your focus ID? P")
focus = 'P'+focus

def return_info(gedcom, ID):
    saving = False
    complete = False
    info = []
    for line in gedcom:
        if line == '0 @'+ID+'@ INDI ':
            saving = True
            info.append(line)
            continue
        if saving:
            if line[0] != '0':
                info.append(line)
            else:
                saving = False
                complete = True
        if complete:
            break
    return info

def return_keys(info):
    # format: parent_key, [spouses]
    parent_key = ''
    spouses = []
    for line in info:
        if line[2:6] == 'FAMC':
            parent_key = line[7:]
        if line[2:6] == 'FAMS':
            spouses.append(line[7:])
    return [parent_key, spouses]

def return_ids(keys, gedcom):
    parents = []
    children = []
    for pkg in enumerate(gedcom):
        line = pkg[1]
        if line == '1 FAMS '+keys[0]:
            index = pkg[0]
            while gedcom[index][0] != '0':
                index -= 1
            id_line = gedcom[index]
            parents.append(id_line.split('@')[1])
        for spouse in keys[1]:
            if line == '1 FAMC '+spouse:
                index = pkg[0]
                while gedcom[index][0] != '0':
                    index -= 1
                id_line = gedcom[index]
                children.append(id_line.split('@')[1])
    return [parents, children]

def return_birth(info):
    birth = {}
    pinned = False
    for line in info:
        if line[0:6] == "1 BIRT":
            pinned = True
        if pinned:
            if line[0:6] == '2 PLAC':
                break
            elif line[0:6] == '2 DATE':
                date = line[7:].split()
                if len(date) > 1:
                    birth[int(date[-1])] = 1.0
                # birth[int(date[-1])] = 1.0
                break
    return birth

def return_sex(info):
    sex = ''
    for line in info:
        if line[0:5] == "1 SEX":
            sex = line[6]
    return sex
        
def return_name(info):
    name = ''
    for line in info:
        if line[0:6] == "1 NAME":
            name = line[7:]
    return name

def return_family(gedcom, focus):
    return return_ids(return_keys(return_info(gedcom, focus)), gedcom)

def highest_val(func):
    vals = sorted(func.items(), key=operator.itemgetter(1))
    return vals[-1]

# old Venture function
"""
def venture(gedcom, head, wave, anchors, blacklist, anchors_names):
    person = head[0]
    path = head[1]
    blacklist.append(person)
    family = return_family(gedcom, person)
    for parent in family[0]:
        info = return_info(gedcom, parent)
        birth = return_birth(info)
        sex = return_sex(info)
        if birth != {}:
            if sex == 'M':
                anchors.append([birth, path+'a'])
            else:
                anchors.append([birth, path+'c'])
            anchors_names.append(return_name(info))
        elif parent not in blacklist:
            if sex == 'M':
                wave.append([parent, path+'a'])
            else:
                wave.append([parent, path+'c'])
            blacklist.append(parent)
    for child in family[1]:
        info = return_info(gedcom, child)
        birth = return_birth(info)
        sex = return_sex(return_info(gedcom, person))
        if birth != {}:
            if sex == 'M':
                anchors.append([birth, path+'b'])
            else:
                anchors.append([birth, path+'d'])
            anchors_names.append(return_name(info))
        elif child not in blacklist:
            if sex == 'M':
                wave.append([child, path+'b'])
            else:
                wave.append([child, path+'d'])
            blacklist.append(child)
    wave.remove(head)
"""

# its called venture because it steps once through the tree
# picking up information along the way, encoding it into strings
# new Venture function
# Only up to 26 unidirectional branches are supported (a-z)
# a = 00, b = 01, c = 10, d = 11
# these represent crawling up or down and to/from which gender
# 0's are used as blanks
def venture(gedcom, head, wave, anchors, blacklist, anchors_names, marker):
    person = head[0]
    path = head[1]
    blacklist.append(person)
    family = return_family(gedcom, person)
    for parent in family[0]:
        info = return_info(gedcom, parent)
        birth = return_birth(info)
        sex = return_sex(info)
        if birth != {}:
            if sex == 'M':
                anchors.append([birth, 'a'+marker+path])
            else:
                anchors.append([birth, 'c'+marker+path])
            anchors_names.append(return_name(info))
        elif parent not in blacklist:
            if sex == 'M':
                wave.append([parent, 'a'+marker+path])
            else:
                wave.append([parent, 'c'+marker+path])
            blacklist.append(parent)
    for child in family[1]:
        info = return_info(gedcom, child)
        birth = return_birth(info)
        sex = return_sex(return_info(gedcom, person))
        if birth != {}:
            if sex == 'M':
                anchors.append([birth, 'b'+marker+path])
            else:
                anchors.append([birth, 'd'+marker+path])
            anchors_names.append(return_name(info))
        elif child not in blacklist:
            if sex == 'M':
                wave.append([child, 'b'+marker+path])
            else:
                wave.append([child, 'd'+marker+path])
            blacklist.append(child)
    wave.remove(head)

#00000000 branch marker is a filler like 'e'
def collect_anchors(gedcom, focus, path_cap):
    print('Locating anchors...')
    cap_copy = copy.copy(path_cap)
    anchors_names = []
    blacklist = []
    anchors = []
    wave = [[focus, '']]
    venture(gedcom, wave[0], wave, anchors, blacklist, anchors_names, '00000001')
    path_cap -= 1
    marker = 2
    print('Step 1 of '+str(cap_copy)+' complete.')
    while (wave != []) and (path_cap > 0):
        wave_copy = copy.copy(wave)
        for head in wave_copy:
            venture(gedcom, head, wave, anchors, blacklist, anchors_names, "{0:08b}".format(marker))
            marker += 1
        path_cap -= 1
        marker = 1
        print('Step '+str(cap_copy-path_cap)+' of '+str(cap_copy)+' complete.')
        # names = [return_name(return_info(gedcom, head[0])) for head in wave]
        # print(names)
    # print(anchors_names)
    return anchors

# old Forge function
"""
def forge_birth(anchors):
    print('Forging birth function...')
    sheets = []
    for anchor in anchors:
        sibtag = ''
        is_sib = False
        pclimbs = 0
        pdrops = 0
        mclimbs = 0
        mdrops = 0
        for step in anchor[1]:
            if step == 'a':
                pdrops += 1
                sibtag += '1'
            if step == 'b':
                pclimbs += 1
                sibtag += '0'
            if step == 'c':
                mdrops += 1
                sibtag += '1'
            if step == 'd':
                mclimbs += 1
                sibtag += '0'
        
        #if sibtag[-2:] == '01':
            #is_sib = True
            #pclimbs -= 1
        #anchor.pop()
        #anchor.append([climbs, drops])
        ext_func = anchor[0]
        for i in range(0, pclimbs):
            ext_func = apply_func(ext_func, neg_male_births)
        for i in range(0, pdrops):
            ext_func = apply_func(ext_func, male_births)
        for i in range(0, mclimbs):
            ext_func = apply_func(ext_func, neg_births)
        for i in range(0, mdrops):
            ext_func = apply_func(ext_func, births)
        sheets.append(ext_func)
    birth_func = sheets[0]
    #print(birth_func)
    for sheet in sheets[1:]:
        birth_func = rescale(combine(birth_func, sheet), 2)
        #print(sheet)
    return birth_func
"""

"""
def cross_cancel(siblings):
    #Input is list of dicts, output is list of modified dicts
    master_func = {}
    for sib in siblings:
        inverse = {}
        for year in sib:
            inverse[year] = math.log(1.0-math.exp(sib[year]))
        if master_func == {}:
            master_func = inverse
        else:
            master_func = combine()
"""

def fill_blanks(anchor, path_cap):
    diff = path_cap - len(anchor[1])/9
    while diff > 0:
        anchor[1] = 'e00000000'+anchor[1]
        diff -= 1
    return None

# new forge function
def forge(anchors, path_cap, ex_func):
    print('Forging...')
    for anchor in anchors:
        fill_blanks(anchor, path_cap)
        print(anchor)
    for i in range(2*path_cap):
        if i%2 == 0:
            print(str(len(anchors))+' anchors left.')
        branches = []
        for anchor in anchors:
            cur = anchor[1][0]
            if cur.isalpha():
                if cur == 'a':
                    anchor[0] = log_apply_func(anchor[0], male_births)
                if cur == 'b':
                    anchor[0] = log_apply_func(anchor[0], neg_male_births)
                if cur == 'c':
                    anchor[0] = log_apply_func(anchor[0], births)
                if cur == 'd':
                    anchor[0] = log_apply_func(anchor[0], neg_births)
                anchor[1] = anchor[1][1:]
            else:
                # the first element of branches shall be branchmarkers
                # print(anchor[1])
                grouped = False
                if anchor[1][:8] != '00000000':
                    for branch in branches:
                        if branch[0][1] == anchor[1]:
                            branch.append(copy.copy(anchor))
                            grouped = True
                if not grouped:
                    branches.append([copy.copy(anchor)])
        if branches != []:
            anchors = []
            for branch in branches:
                # FUTURE IDEA:
                # group sibling funcs together
                # run cross_cancel on it
                node = branch[0]
                node[1] = node[1][8:]
                del branch[0]
                for anchor in branch:
                    node[0] = log_combine(node[0], anchor[0])
                node[0] = log_rescale(node[0], 2)
                anchors.append(node)
            branches = []
    if ex_func == {}:
        final_func = anchors[0][0]
    else:
        final_func = log_rescale(log_combine(anchors[0][0], ex_func), 2)
    print('Forged.')
    return unlogify(final_func)

def snipe(gedcom, focus, ex_func, path_cap):
    return forge(collect_anchors(gedcom, focus, path_cap), path_cap, ex_func)

# allows for preprocessing of random variables, such as knowledge
# of being born before or after a particular year. Default is empty
ex_func = {}
# ex_func = unifunc(1700, 1804)

focus_name = return_name(return_info(gedcom, focus))
focus_name = focus_name.replace('/', '')
print(focus_name)
focus_func = snipe(gedcom, focus, ex_func, 5)

# print(focus_func)
h_val = highest_val(focus_func)
print('Most likely year of birth: '+str(h_val[0])+' with a '+str(round(h_val[1]*100, 2))+'% chance.')

fig = plt.figure(figsize=(10, 6))
plt.title('Birth Function for '+focus_name)
plt.plot(*zip(*sorted(focus_func.items())))
fig.savefig(focus+'_birthfunction')

"""
file = open('data.txt','w')

for pair in focus_func.items():
    file.write(str(pair)+'\n')
 
file.close()

import smooth
"""

while True:
    year = int(input('Specify a year: '))
    if (year in focus_func):
        chance = round(focus_func[year]*100, 2)
        print('Chance of being correct year: '+str(chance)+'%')
    else:
        print('Chance of being correct year: Negligible')

# print(return_birth(return_info(gedcom, focus)))
# test = return_family(gedcom, focus)

# print(test)
