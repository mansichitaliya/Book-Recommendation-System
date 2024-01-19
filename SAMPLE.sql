-- CREATE DATABASE IF NOT EXISTS 'geeklogin' DEFAULT CHARACTER SET utf8 COLLATE utf8_general_cli;

CREATE DATABASE IF NOT EXISTS bookrecsys
DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8_general_ci;
USE bookrecsys;
CREATE TABLE IF NOT EXISTS `userdata`
(
`id` int(11) NOT NULL AUTO_INCREMENT,
`username` varchar(255) NOT NULL,
`password` varchar(255) NOT NULL,
`email` varchar(100) NOT NULL,
`location` varchar(255) NOT NULL,
`age` varchar(255) NOT NULL,
PRIMARY KEY (`id`)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8; 
