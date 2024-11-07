# Hurdles level based on weather conditions
level_hurdles = {
    1: [
        {"description": "Mild turbulence ahead. Do you adjust your speed (1) or maintain current speed (2)?", "correct_option": 1, "result": "Successfully adjusted speed to navigate turbulence.", "complexity": 20},
        {"description": "The weather is clear, but there's a minor mechanical issue. Do you continue flying (1) or check your instruments (2)?", "correct_option": 2, "result": "You identified the issue and fixed it.", "complexity": 10},
        {"description": "A slight wind from the north. Do you adjust your course (1) or maintain your heading (2)?", "correct_option": 1, "result": "You successfully adjusted the course to compensate for the wind.", "complexity": 15},
        {"description": "You receive a radio call for potential hazards. Do you respond (1) or continue without checking (2)?", "correct_option": 1, "result": "Communication established. You avoided hazards.", "complexity": 10},
        {"description": "Clear skies but sudden headwinds. Do you increase thrust (1) or maintain current speed (2)?", "correct_option": 1, "result": "Increased thrust and stabilized the flight.", "complexity": 20}
    ],
    2: [
        {"description": "Moderate turbulence is shaking the plane. Do you climb higher (1) or descend (2)?", "correct_option": 2, "result": "Successfully descended to avoid turbulence.", "complexity": 30},
        {"description": "A rainstorm is approaching. Do you fly around it (1) or go through it (2)?", "correct_option": 1, "result": "You safely navigated around the storm.", "complexity": 25},
        {"description": "Crosswinds are intensifying. Do you adjust the rudder (1) or keep it steady (2)?", "correct_option": 1, "result": "Correctly adjusted the rudder to counter crosswinds.", "complexity": 30},
        {"description": "Visibility is reduced by rain. Do you slow down (1) or maintain speed (2)?", "correct_option": 1, "result": "You slowed down and maintained control.", "complexity": 20},
        {"description": "You spot heavy clouds ahead. Do you fly above them (1) or navigate below them (2)?", "correct_option": 2, "result": "Safely flew below the clouds.", "complexity": 25}
    ],
    3: [
        {"description": "Strong winds from the east are pushing the plane off course. Do you adjust heading (1) or increase speed (2)?", "correct_option": 1, "result": "You adjusted heading and stayed on course.", "complexity": 35},
        {"description": "Heavy rain is limiting visibility. Do you rely on instruments (1) or reduce altitude (2)?", "correct_option": 1, "result": "You used instruments and safely continued the flight.", "complexity": 40},
        {"description": "The temperature is dropping rapidly. Do you activate de-icing (1) or continue as normal (2)?", "correct_option": 1, "result": "You activated de-icing and avoided potential hazards.", "complexity": 40},
        {"description": "Sudden gusts of wind are causing turbulence. Do you change altitude (1) or slow down (2)?", "correct_option": 1, "result": "You changed altitude and stabilized the flight.", "complexity": 35},
        {"description": "Lightning is striking near your path. Do you alter your route (1) or maintain heading (2)?", "correct_option": 1, "result": "You altered your route and avoided danger.", "complexity": 50}
    ],
    4: [
        {"description": "A severe snowstorm is ahead. Do you fly over it (1) or try to fly around it (2)?", "correct_option": 2, "result": "You successfully flew around the snowstorm.", "complexity": 60},
        {"description": "Heavy snow and strong winds are reducing visibility. Do you rely entirely on instruments (1) or reduce speed (2)?", "correct_option": 1, "result": "You relied on instruments and safely navigated the conditions.", "complexity": 55},
        {"description": "The temperature is extremely low, and ice is forming. Do you climb to a warmer altitude (1) or activate de-icing (2)?", "correct_option": 2, "result": "You activated de-icing and prevented ice buildup.", "complexity": 50},
        {"description": "Blizzard conditions are making it hard to see. Do you decrease altitude (1) or maintain heading (2)?", "correct_option": 1, "result": "You decreased altitude and maintained control.", "complexity": 55},
        {"description": "Sudden wind shear is causing instability. Do you adjust the flaps (1) or increase thrust (2)?", "correct_option": 1, "result": "You adjusted the flaps and stabilized the plane.", "complexity": 60}
    ]
}

# Based on the weather level, choose hurdles for the player
def get_hurdles_for_level(level):
    if level == 1:
        return level_hurdles.get(level,1)
    elif level == 2:
        return level_hurdles.get(level,2)
    elif level == 3:
        return level_hurdles.get(level,3)
    elif level == 4:
        return level_hurdles.get(level,4)
    return []