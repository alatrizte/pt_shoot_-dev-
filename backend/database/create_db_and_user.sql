-- Para ejecutar este archivo escribir en una terminal: sudo mysql < create_db_and_user.sql
-- Crea la base de datos 'plan_shoot' - El nombre se puede cambiar por otro -
CREATE DATABASE IF NOT EXISTS plan_shoot;

-- Crear un usuario con contraseña
CREATE USER IF NOT EXISTS 'primero'@'localhost' IDENTIFIED BY '1_Direccion';

-- Crear la tabla de users
USE plan_shoot;
CREATE TABLE IF NOT EXISTS users (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
                                    user_name VARCHAR(50) NOT NULL, 
                                    user_mail VARCHAR(128) NOT NULL, 
                                    user_pass VARCHAR(128) NOT NULL,
                                    key_confirm VARCHAR (8)
                                    );
CREATE TABLE IF NOT EXISTS projects (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
                                    user_id INT NOT NULL, 
                                    ci_project VARCHAR(8) NOT NULL, 
                                    name_project VARCHAR(255) NOT NULL,
                                    FOREIGN KEY (user_id) REFERENCES users(id)
                                    );
-- Otorgar todos los privilegios al usuario en la base de datos
GRANT ALL PRIVILEGES ON plan_shoot.* TO 'primero'@'localhost';

-- Aplicar los cambios de privilegios
FLUSH PRIVILEGES;
