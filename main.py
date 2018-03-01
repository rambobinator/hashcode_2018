class Car:

    def __init__(self, pos=(0,0)):
        self.pos = pos
        self.ride = None
        self.ride_history = []

class Ride:

    def __init__(self, _from=(0,0), to=(0,0), start=0, end=0):
        self._from = _from
        self.to = to
        self.start = start
        self.end = end
        self.duration = self.get_distance_from(to)
        self.max_duration = (end - start)
        self.ended = False
        self.score = 0

    def get_distance_from(self, pos):
        a, b = self._from
        x, y = pos
        return (a - x) + (b - y)

class City:

    def __init__(self, car_list, ride_list, steps, bonus):
        self.car_list = car_list
        self.ride_list = ride_list
        self.steps = steps
        self.current_step = 0
        self.remaining_steps = steps
        self.bonus = bonus

    def get_best_ride_index(self, car_pos):
        tmp_dist = None
        ret_index = None
        car = self.car_list[car_pos]
        for i, ride in enumerate(self.ride_list):
            if ride.ended:
                continue
            dist = ride.get_distance_from(car.pos)
            dist += ride.duration
            if dist > self.remaining_steps:
                continue
            if (tmp_dist is None or ((dist < tmp_dist) and (dist > -1))):
                tmp_dist = dist
                ret_index = i
        return ret_index

    def assign_rides(self):
        for i, car in enumerate(self.car_list):
            if car.ride is None:
                best_ride_index = self.get_best_ride_index(i)
                if best_ride_index is None:
                    continue
                next_ride = self.ride_list[best_ride_index]
                if next_ride.start > self.current_step:
                    self.ride_list[best_ride_index].score += self.bonus
                self.ride_list[best_ride_index].score += next_ride.duration
                self.ride_list[best_ride_index].ended = True
                self.car_list[i].ride = next_ride
                self.car_list[i].ride_history.append(str(best_ride_index))

    def update(self):
        for i, car in enumerate(self.car_list):
            if car.ride is not None:
                self.car_list[i].ride.duration -= 1
                current_ride = self.car_list[i].ride
                if current_ride.duration <= 0:
                    self.car_list[i].ride = None
                    self.car_list[i].pos = current_ride.to
        self.remaining_steps -= 1
        self.current_step += 1

    def dump(self):
        ret = []
        for car in self.car_list:
            ret.append("{} {}".format(len(car.ride_history), " ".join(car.ride_history)))
        return '\n'.join(ret)

    def display_debug(self):
        print("STEP {} (remaining: {}):".format(self.current_step, self.remaining_steps))
        for car in self.car_list:
            if car.ride:
                print(car.ride._from, car.ride.duration)
            else:
                print("Nan")

    def run(self):
        while (self.current_step < self.steps):
            #self.display_debug()
            self.assign_rides()
            self.update()
        print("SCORE: {}".format(sum([ride.score for ride in self.ride_list])))
        return self.dump()


def run(filename):
    with open(filename) as f:
        _, _, cars, _, bonus, steps = map(int, next(f)[:-1].split())
        car_list = [Car() for i in range(0, cars)]
        ride_list = []
        for l in f:
            a, b, x, y, s, f = map(int, l[:-1].split())
            ride_list.append(Ride((a, b), (x, y), s, f))
        city = City(car_list, ride_list, steps, bonus)
        return city.run()


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 2:
        for filename in sys.argv[1:]:
            with open("{}out".format(filename[:-2]), 'w') as f:
                f.write(run(filename))
    else:
        print("No file !")
