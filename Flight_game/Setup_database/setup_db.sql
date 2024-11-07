-- Drop existing tables if they exist
DROP TABLE IF EXISTS User_Flight_Log;
DROP TABLE IF EXISTS Checkpoint;
DROP TABLE IF EXISTS Flight;
DROP TABLE IF EXISTS Weather;
DROP TABLE IF EXISTS Airport;
DROP TABLE IF EXISTS Country;
DROP TABLE IF EXISTS User;

-- Country and Airport tables were imported from the sql script provided.
-- Table: Weather
CREATE TABLE Weather (
                         id INT AUTO_INCREMENT PRIMARY KEY,
                         `condition` VARCHAR(50) NOT NULL,
                         temperature DECIMAL(5, 2),
                         wind_speed DECIMAL(5, 2),
                         humidity INT,
                         visibility DECIMAL(5, 2)
);

-- Table: User
CREATE TABLE User (
                      id INT AUTO_INCREMENT PRIMARY KEY,
                      username VARCHAR(255) NOT NULL UNIQUE,
                      checkpoint_id INT,
                      FOREIGN KEY (checkpoint_id) REFERENCES Checkpoint(id) ON DELETE SET NULL
);

-- Table: User_Flight_Log
CREATE TABLE User_Flight_Log (
                                 id INT AUTO_INCREMENT PRIMARY KEY,
                                 user_id INT,
                                 flight_id INT,
                                 weather_id INT,
                                 flight_time TIME,
                                 completion_status VARCHAR(50),
                                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                 FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
                                 FOREIGN KEY (flight_id) REFERENCES Flight(id) ON DELETE CASCADE,
                                 FOREIGN KEY (weather_id) REFERENCES Weather(id) ON DELETE SET NULL
);

-- Table: Flight
CREATE TABLE Flight (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        departure_airport_id INT,
                        arrival_airport_id INT,
                        scheduled_departure_time DATETIME,
                        scheduled_arrival_time DATETIME,
                        FOREIGN KEY (departure_airport_id) REFERENCES Airport(id) ON DELETE CASCADE,
                        FOREIGN KEY (arrival_airport_id) REFERENCES Airport(id) ON DELETE CASCADE
);

-- Table: Checkpoint
CREATE TABLE Checkpoint (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            user_flight_id INT,
                            weather_id INT,
                            checkpoint_time TIMESTAMP,
                            location_coordinates VARCHAR(255),
                            status VARCHAR(50),
                            FOREIGN KEY (user_flight_id) REFERENCES User_Flight_Log(id) ON DELETE CASCADE,
                            FOREIGN KEY (weather_id) REFERENCES Weather(id) ON DELETE SET NULL
);

ALTER DATABASE flight_sim CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- Updated oct 6/2024

Alter table user rename column checkpoint_id to fuel_consumed;
ALTER TABLE User DROP FOREIGN KEY fk_checkpoint_id;
ALTER TABLE User MODIFY fuel_consumed INT DEFAULT 500;
-- updated oct 7/2024.
-- for the new feature updates on the game where
-- ever user created or existed has a fuel capacity of certain level,
-- which can be gained more by completing the levels and reduced when user fails to complete a challenge