#Phase 1
 
#Inserting Modules
import math
from vpython import *
import random
 
#Universal Constants
GRAV_CONSTANT = 1
DENSITY_STAR = 1
DENSITY_PARTICLE = 0.05
DEL_T = 0.05
COLOR_TRACK = 0

#let there be light
distant_light(direction=vector(1,0,0), color = vector(0.878, 0.208, 0.133))
distant_light(direction=vector(-1,0,0), color = vector(0.878, 0.208, 0.133))
distant_light(direction=vector(0,1,0), color = vector(0.878, 0.208, 0.133))
distant_light(direction=vector(0,-1,0), color = vector(0.878, 0.208, 0.133))
distant_light(direction=vector(0,0,1), color = vector(0.878, 0.208, 0.133))
distant_light(direction=vector(0,0,-1), color = vector(0.878, 0.208, 0.133))
 
#Defining Assembly Elements
def rand_posvec():
    radius = random.gauss(5000, 500)
    angle = 2 * math.pi * random.random()
    z_bounce = 20 * random.random() - 10
    return (vector(radius * math.cos(angle), radius * math.sin(angle), z_bounce), angle)
 
def rand_velvec(iangle):
    avg_mass = DENSITY_STAR * (4/3) * math.pow(500, 3)
    avg_velocity = math.sqrt(2 * GRAV_CONSTANT * avg_mass / 5000)
    velocity = random.gauss(avg_velocity, 20)
    angle = random.gauss(iangle + (math.pi/2), 0.05)
    return vector(velocity * math.cos(angle), velocity * math.sin(angle), 0)
 
def dust_particles(n):
    particles = [''] * n
    for i in range(n):
        a = random.random() * 10 + 70
        particles[i] = sphere(pos = rand_posvec()[0], radius = a, color = color.cyan)
        particles[i].iangle = rand_posvec()[1]
        particles[i].velocity = rand_velvec(particles[i].iangle)
        particles[i].acceleration = vector(0, 0, 0)
        particles[i].a1 = vector(0, 0, 0)
        particles[i].a2 = vector(0, 0, 0)
    return particles
 
def star_particles():
    star = sphere(pos = vector(0, 0, 0), radius = 400 + 200 * random.random(), color = vector(0.878, 0.208, 0.133))
    star.velocity = vector(0, 0, 0)
    return star
 
#Acceleration Control
def star_acceleration(i):
    star_mass = (4/3) * math.pow(Type_Star.radius, 3) * DENSITY_STAR
    Type_Debs[i].a1 = -((GRAV_CONSTANT * star_mass)/ math.pow(mag(Type_Debs[i].pos), 3)) * Type_Debs[i].pos
 
def debs_acceleration(i):
    Type_Debs[i].a2 = vector(0, 0, 0)
    for j in range(len(Type_Debs)):
        if (j == i) or (Type_Debs[j].visible == False):
            continue
        else:
            j_mass = (4/3) * math.pow(Type_Debs[j].radius, 3) * DENSITY_PARTICLE
            r = Type_Debs[j].pos - Type_Debs[i].pos
            Type_Debs[i].a2 += ((GRAV_CONSTANT * j_mass)/ math.pow(mag(r), 3)) * r
        
Type_Debs = dust_particles(125)
Type_Star = star_particles()

def zero_out(i):
    Type_Debs[i].radius = 0
    Type_Debs[i].velocity = vector(0, 0, 0)
    Type_Debs[i].visible = False
    

#Collision Control
def star_merge(i):
    global COLOR_TRACK
    new_radius = math.pow(math.pow(Type_Star.radius, 3) + math.pow(Type_Debs[i].radius, 3), 1/3)
    Type_Star.radius = new_radius
    if COLOR_TRACK <= 10:
        Type_Star.color += vector(0, 0.066, 0)
        print(Type_Star.color)
    elif COLOR_TRACK <= 20:
        Type_Star.color += vector(0.012, 0.012, 0.083)
        print(Type_Star.color)
            
    else:
        pass
    COLOR_TRACK += 1


def particle_merge(i):
    a = []
    for j in range(len(Type_Debs)):
        if (j == i) or (Type_Debs[j].visible == False):
            continue
        elif mag(Type_Debs[i].pos - Type_Debs[j].pos) < 150:
            new_radius = math.pow(math.pow(Type_Debs[j].radius, 3) + math.pow(Type_Debs[i].radius, 3), 1/3)
            i_mass = (4/3) * math.pi * DENSITY_PARTICLE * Type_Debs[i].radius * Type_Debs[i].radius
            j_mass = (4/3) * math.pi * DENSITY_PARTICLE * Type_Debs[j].radius * Type_Debs[j].radius
            v = (i_mass * Type_Debs[i].velocity + j_mass * Type_Debs[j].velocity)/(i_mass + j_mass)
            p = (i_mass * Type_Debs[i].pos + j_mass * Type_Debs[j].pos)/(i_mass + j_mass)
            Type_Debs[i].velocity = v
            Type_Debs[i].radius = new_radius
            Type_Debs[i].color = color.green
            a.append(j)
        else:
            continue

    for i in a:
        zero_out(i)

    return a
            
#Main Loop 
while True:
    
    for i in range(len(Type_Debs)):
        if Type_Debs[i].visible == True:
            a1 = []
            a2 = []
            star_acceleration(i)
            debs_acceleration(i)
            Type_Debs[i].pos += Type_Debs[i].velocity * DEL_T
            Type_Debs[i].acceleration = Type_Debs[i].a1 + Type_Debs[i].a2
            Type_Debs[i].velocity += Type_Debs[i].acceleration * DEL_T
            if mag(Type_Debs[i].pos) < Type_Star.radius:
                star_merge(i)
                a1.append(i)
                zero_out(i)
            else:
                pass

            a2.extend(particle_merge(i))
            
    del_list = a1 + a2
    del_list.sort(reverse = True)
    for i in del_list:
        del Type_Debs[i]
    
