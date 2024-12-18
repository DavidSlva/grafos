# datos.py

N = [1, 2, 3, 4, 5, 6] # Buques
M = [1, 2, 3] # Sitios de atraque

# Llegada Real
a_i = {
    1:4, 2:3, 3:5, 4:5, 5:6, 6:11
} 

# Llegada planificada
A_i = {
    1:4, 2:3, 3:1, 4:7, 5:9, 6:12
}

# Salida planificada
e_i = {
    1:7, 2:5, 3:5, 4:9, 5:10, 6:14
}


H_ik = { 
    (1,1): 6, (1,2): 4, (1,3): 3.0,
    (2,1): 1.4, (2,2): 2.5, (2,3): 4.0,
    (3,1): 3.3, (3,2): 1.1, (3,3): 3.0,
    (4,1): 4.0, (4,2): 2.0, (4,3): 3,
    (5,1): 3, (5,2): 3.0, (5,3): 2.0,
    (6,1): 3, (6,2): 4.0, (6,3): 2 
}

h_ik = { 
    (1,1): 6.5, (1,2): 4.5, (1,3): 3.0,
    (2,1): 2.2, (2,2): 2.5, (2,3): 4.0,
    (3,1): 3.3, (3,2): 1.1, (3,3): 3.0,
    (4,1): 4.0, (4,2): 2.0, (4,3): 3.5,
    (5,1): 3.1, (5,2): 3.0, (5,3): 2.0,
    (6,1): 3.2, (6,2): 4.0, (6,3): 2.9 
}

b_ik = { 
    (1,1): 1, (1,2): 0, (1,3): 0,
    (2,1): 0, (2,2): 1, (2,3): 0,
    (3,1): 0, (3,2): 0, (3,3): 1,
    (4,1): 0, (4,2): 1, (4,3): 0,
    (5,1): 0, (5,2): 0, (5,3): 1,
    (6,1): 0, (6,2): 1, (6,3): 0 
}

L_i = {
    1:200, 2:100, 3:150, 4:100, 5:90, 6:300
}

g_k = {
    1:0, 2:300, 3:600
}

c1 = 18
c2 = 50
c3 = 80

mu_i = {
    1:100, 2:6, 3:2, 4:1, 5:9, 6:12
}

M_i = {
    1: [1,2,3],
    2: [1,2],
    3: [1,2,3],
    4: [1,2,3],
    5: [1,3],
    6: [1,2,3]
}

ventanas_bloqueo = {
        (1,1): [(0, 23)],
        (1,2): [(0, 25)],
        (1,3): [(4,7),(9,11),(12,20),(40,50)],
        (2,1): [],
        (2,2): [],
        (2,3): [],
        (3,1): [],
        (3,2): [],
        (3,3): [],
        (4,1): [],
        (4,2): [],
        (4,3): [],
        (5,1): [],
        (5,2): [],
        (5,3): [],
        (6,1): [],
        (6,2): [],
        (6,3): [(10,15)]
    }

# Constante grande
B = 10000
