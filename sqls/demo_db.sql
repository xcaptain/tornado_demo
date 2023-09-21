create database IF NOT EXISTS demo_db;

use demo_db;

CREATE TABLE IF NOT EXISTS `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(42) NOT NULL DEFAULT "",
  `password` varchar(42) NOT NULL DEFAULT "",
  `create_tm_ms` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `update_tm_ms` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_email` (`email`) USING BTREE
);
