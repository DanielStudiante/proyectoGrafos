from time import sleep

class Donkey:
    def __init__(self, name, age, max_age, donkey_energy, grass_in_basement):
        self.name:str = name
        self.age:float = age
        self.max_age:float = max_age
        self.donkey_energy:float = donkey_energy
        self.alive:bool = True
        self.grass_in_basement = grass_in_basement
        self.damage_stars:float = self.calculate_damage_per_trip()
        self.damage_constellations:float = self.calculate_damage_per_trip(True)
        self.health: str = self.calculate_donkey_health()

    def calculate_damage_per_trip(self, is_constellation:bool = False):
        damage:float = 0
        match self.age:
            case age if 0 <= age < 891:
                damage = 0.05
                if is_constellation: damage = 0.08
            case v if 891 <= v < 1783:
                damage = 0.10
                if is_constellation: damage = 0.15
            case v if 1783 <= v < 2675:
                damage = 0.15
                if is_constellation: damage = 0.20
            case _:
                damage = 0.20
                if is_constellation: damage = 0.25
        return damage

    def calculate_donkey_health(self):
        health: str = ""
        match self.donkey_energy:
            case energy if energy > 75:
                health = "Excelente"
            case energy if 50 <= energy <= 75:
                health = "Buena"
            case energy if 25 <= energy < 50:
                health = "Mala"
            case energy if 1 <= energy < 25:
                health = "Moribundo"
            case _:
                health = "Muerto"
        return health

    def calculate_grass_profit(self):
        if self.grass_in_basement <= 0:
            return 0
        match self.health:
            case 'Excelente':
                return 1.05
            case 'Buena':
                return 1.03
            case 'Mala':
                return 1.02
            case 'Moribundo':
                return 1.01
            case _:
                return 1

    def eat_grass(self, grass_profit:float = 1.0):
        if self.grass_in_basement <= 0:
            print("No hay hierba en el sótano para que el burro coma.")
            return False
        if self.donkey_energy >= 100:
            print("El burro ya tiene energía completa y no necesita comer.")
            return False
        self.donkey_energy += 1 * grass_profit
        self.grass_in_basement -= 1
        self.health = self.calculate_donkey_health()
        return True


    def dead(self):
        self.alive = False
        self.damage_stars = 0

    def stay_of_star(self, time_to_eat_kg:float = 0, time_of_stance:float = 0):
        if not self.alive:
            return "El burro está muerto y no puede explorar."
        
        if self.donkey_energy < 50:
            time_investigate, time_to_eat  = time_of_stance * 0.5
            for _ in range(int(time_to_eat)):
                if self.eat_grass(self.calculate_grass_profit()):
                    sleep(time_to_eat_kg)
                    print("El burro ha comido 1 kg de hierba.")
                else:
                    print("El burro no pudo comer más hierba.")
                    break

        else:
            time_investigate = time_of_stance
            
            # implementar logica de investigación

    def trip(self, distance:float, time_to_eat_kg:float = 0, time_of_stance:float = 0, is_star:bool = True):
        if not self.alive:
            return "El burro está muerto y no puede viajar."

        self.age += distance
        if is_star:
            self.donkey_energy *= self.damage_stars
        else:
            self.donkey_energy *= self.damage_constellations

        if self.age >= self.max_age or self.donkey_energy <= 0:
            self.dead()
            return "El burro ha muerto durante el viaje."
        
        self.health = self.calculate_donkey_health()
        if is_star:
            self.stay_of_star(time_to_eat_kg, time_of_stance)

    def hyper_star(self, distance:float):
        if not self.alive:
            return "El burro está muerto y no puede viajar."

        self.age += distance

        if self.age >= self.max_age or self.donkey_energy <= 0:
            self.dead()
            return "El burro ha muerto durante el viaje."
        
        self.donkey_energy *= 1.5
        self.grass_in_basement *= 2

        
        self.health = self.calculate_donkey_health()