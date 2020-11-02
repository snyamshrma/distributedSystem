# setting up mysql
sudo apt-get update
sudo apt-get install mysql-server
sudo mysql_secure_installation

# creating new user
mysql -u root -p
CREATE USER 'root'@'localhost' IDENTIFIED BY 'a';
GRANT ALL PRIVILEGES ON * . * TO 'root'@'localhost';
FLUSH PRIVILEGES;

# connecting new user to database
# mysql -u root -p

# setting up rest of the requirements
pip install -r requirement.txt