
class Donkey:
    def __init__(self, name, age, donkey_energy, donkey_speed, life_time, grass_in_basement):
        self.name:str = name
        self.age:int = age
        self.donkey_energy:float = donkey_energy
        self.donkey_speed:float = donkey_speed
        self.life_time:float = life_time
        self.alive:bool = True
        self.grass_in_basement = grass_in_basement
        self.damage_stars:float = self.calculate_damage_per_trip()
        self.damage_constellations:float = self.calculate_damage_per_trip(True)
        self.health: str = self.calculate_donkey_health()

    def calculate_damage_per_trip(self, is_constellation:bool = False):
        damage:float = 0
        match self.age:
            case age if 0 <= age < 5:
                damage = 0.01
                if is_constellation: damage =0.02
            case v if 5 <= v < 10:
                damage = 0.02
                if is_constellation: damage =0.03
            case v if 10 <= v < 15:
                damage = 0.03
                if is_constellation: damage =0.04
            case _:
                damage = 0.04
                if is_constellation: damage =0.05
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

    def eat_grass(self, ):
        if self.grass_in_basement <= 0:
            return "No hay hierba en el sótano para que el burro coma."

    def dead(self):
        self.alive = False
        self.damage_stars = 0

    def journey_through_stars(self, distance:float, time_to_eat:int = 0):
        if not self.alive:
            return "El burro está muerto y no puede viajar."

        self.life_time -= distance
        self.donkey_energy *= self.damage_stars
        self.health = self.calculate_donkey_health()

        if self.life_time <= 0 or self.donkey_energy <= 0:
            self.dead()
            return "El burro ha muerto durante el viaje."

        time_of_stance = 2 * time_to_eat

        if self.donkey_energy < 50:
            self.eat_grass()
            time_investigate = time_to_eat
        else:
            time_investigate = time_of_stance