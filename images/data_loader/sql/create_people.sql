DROP TABLE IF EXISTS people;

CREATE TABLE `people` (
   `id`            INT          NOT NULL AUTO_INCREMENT,
  `given_name`     VARCHAR(80)  DEFAULT NULL,
  `family_name`    VARCHAR(200) DEFAULT NULL,
  `date_of_birth`  DATE         DEFAULT NULL,
  `place_of_birth` VARCHAR(200) DEFAULT NULL
  PRIMARY KEY (`id`)
);
