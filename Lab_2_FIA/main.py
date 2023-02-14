import tkinter
import math
import Boid
from utils import *

def initialise_canvas(window, screen_size):
    canvas = tkinter.Canvas(window, width=800, height=600)
    canvas.pack()
    window.resizable(False, False)
    return canvas


def create_boids(canvas, no_of_boids):
    list_of_boids = []
    for n in range(no_of_boids):
        boid = Boid.Boid("boid" + str(n))
        list_of_boids.append(boid)
        boid.draw_boid(canvas)
    return list_of_boids


def separation(nearest_neighbour, boid):
    # move 1: move away from nearest - separation
    # calculate angle between boid and nearest boid, then angle it in the opposite direction
    if nearest_neighbour is not None and boid.euclidean_distance(nearest_neighbour) < 35:
        direction = Vector([nearest_neighbour.x - boid.x, nearest_neighbour.y - boid.y])
        angle = direction.data[1] / direction.data[0]
        boid.angle -= math.atan(angle)


def alignment(neighbours, boid):
    # move 2: orient towards the neighbours - alignment
    # calculate average angle of neighbours and move in that direction
    average_neighbour_vector = Vector([0.0, 0.0])
    if neighbours:
        for neighbour_boid in neighbours:
            average_neighbour_vector += Vector(
                [math.cos(neighbour_boid.angle), math.sin(neighbour_boid.angle)])
        average_neighbour_vector /= len(neighbours)
        boid.angle -= (math.atan2(average_neighbour_vector.data[1],
                                  average_neighbour_vector.data[0]) - boid.angle) / 100.0
        boid.angle = math.atan2(average_neighbour_vector.data[1], average_neighbour_vector.data[0])


def cohesion(neighbours, boid):
    # move 3: move together - cohesion
    if neighbours:
        avg_pos = Vector([0.0, 0.0])
        for neighbour_boid in neighbours:
            avg_pos += Vector([neighbour_boid.x, neighbour_boid.y])
        avg_pos /= len(neighbours)
        delta_pos = avg_pos - Vector([boid.x, boid.y])
        angle = np.arctan2(delta_pos.data[1], delta_pos.data[0])
        boid.angle -= angle / 20.0


def boid_behaviours(canvas, list_of_boids, screen_size):
    # find neighbours
    for boid in list_of_boids:
        neighbours = []
        for b in list_of_boids:
            # if b is nearby current boid, then it is a neighbour and make sure neighbor boid is not
            # current boid
            if boid.euclidean_distance(b) < 75 and (not boid.euclidean_distance(b) == 0):
                neighbours.append(b)
        nearest_neighbour = None
        # finding nearest neighbour
        if neighbours:
            shortest_distance = 999999999
            for neighbour_boid in neighbours:
                d = boid.euclidean_distance(neighbour_boid)
                if d < shortest_distance:
                    shortest_distance = d
                    nearest_neighbour = neighbour_boid

        separation(nearest_neighbour, boid)
        alignment(neighbours, boid)
        cohesion(neighbours, boid)

    for boid in list_of_boids:
        boid.flock(canvas, screen_size)
    canvas.after(100, boid_behaviours, canvas, list_of_boids, screen_size)


def main():
    screen_size = 1000
    no_of_boids =80
    window = tkinter.Tk()
    canvas = initialise_canvas(window, screen_size)
    list_of_boids = create_boids(canvas, no_of_boids)
    boid_behaviours(canvas, list_of_boids, screen_size)
    window.mainloop()


main()