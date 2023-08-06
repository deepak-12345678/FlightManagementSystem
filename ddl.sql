create database ticketBook;
use ticketBook;
CREATE TABLE `django_session` (`session_key` varchar(40) NOT NULL PRIMARY KEY, `session_data` longtext NOT NULL, `expire_date` datetime(6) NOT NULL);
CREATE INDEX `django_session_expire_date_a5c62663` ON `django_session` (`expire_date`);
CREATE TABLE `django_content_type` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(100) NOT NULL, `app_label` varchar(100) NOT NULL, `model` varchar(100) NOT NULL);
ALTER TABLE `django_content_type` ADD CONSTRAINT `django_content_type_app_label_model_76bd3d3b_uniq` UNIQUE (`app_label`, `model`);
CREATE TABLE `auth_permission` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(50) NOT NULL, `content_type_id` integer NOT NULL, `codename` varchar(100) NOT NULL);
CREATE TABLE `auth_group` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(80) NOT NULL UNIQUE);
CREATE TABLE `auth_group_permissions` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `group_id` integer NOT NULL, `permission_id` integer NOT NULL);
ALTER TABLE `auth_permission` ADD CONSTRAINT `auth_permission_content_type_id_codename_01ab375a_uniq` UNIQUE (`content_type_id`, `codename`);
ALTER TABLE `auth_permission` ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);
ALTER TABLE `auth_group_permissions` ADD CONSTRAINT `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` UNIQUE (`group_id`, `permission_id`);
ALTER TABLE `auth_group_permissions` ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);
ALTER TABLE `auth_group_permissions` ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);
--
-- Create model Passenger
--
CREATE TABLE `passengers` (`password` varchar(100) NOT NULL, `email` varchar(254) NOT NULL PRIMARY KEY, `date_of_birth` date NULL, `name` varchar(100) NOT NULL);
CREATE TABLE `passengers_groups` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `passenger_id` varchar(254) NOT NULL, `group_id` integer NOT NULL);
CREATE TABLE `passengers_user_permissions` (`id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY, `passenger_id` varchar(254) NOT NULL, `permission_id` integer NOT NULL);
--
-- Create model Booking
--
CREATE TABLE `bookings` (`booking_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `status` varchar(20) NOT NULL, `created_at` datetime(6) NOT NULL);
--
-- Create model Flight
--
CREATE TABLE `flights` (`flight_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(100) NOT NULL, `start_time` datetime(6) NOT NULL, `end_time` datetime(6) NOT NULL, `source` varchar(100) NOT NULL, `destination` varchar(100) NOT NULL);
--
-- Create model Cancellation
--
CREATE TABLE `cancellations` (`booking_id` integer NOT NULL PRIMARY KEY, `created_at` datetime(6) NOT NULL, `reason` longtext NOT NULL);
--
-- Create model SMS
--
CREATE TABLE `sms` (`sms_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `body` longtext NOT NULL, `created_at` datetime(6) NOT NULL, `recepient_id` varchar(254) NOT NULL);
--
-- Create model Seat
--
CREATE TABLE `seats` (`seat_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `seat_type` varchar(100) NOT NULL, `flight_id` integer NOT NULL);
--
-- Create model Email
--
CREATE TABLE `emails` (`em_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `subject` varchar(100) NOT NULL, `body` longtext NOT NULL, `created_at` datetime(6) NOT NULL, `recepient_id` varchar(254) NOT NULL);
--
-- Add field seat to booking
--
ALTER TABLE `bookings` ADD COLUMN `seat_id` integer NOT NULL , ADD CONSTRAINT `bookings_seat_id_05dfaa38_fk_seats_seat_id` FOREIGN KEY (`seat_id`) REFERENCES `seats`(`seat_id`);
--
-- Add field user to booking
--
ALTER TABLE `bookings` ADD COLUMN `user_id` varchar(254) NOT NULL , ADD CONSTRAINT `bookings_user_id_6e734b08_fk_passengers_email` FOREIGN KEY (`user_id`) REFERENCES `passengers`(`email`);
ALTER TABLE `passengers_groups` ADD CONSTRAINT `passengers_groups_passenger_id_group_id_a079617a_uniq` UNIQUE (`passenger_id`, `group_id`);
ALTER TABLE `passengers_groups` ADD CONSTRAINT `passengers_groups_passenger_id_b4628fce_fk_passengers_email` FOREIGN KEY (`passenger_id`) REFERENCES `passengers` (`email`);
ALTER TABLE `passengers_groups` ADD CONSTRAINT `passengers_groups_group_id_b8a400c5_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);
ALTER TABLE `passengers_user_permissions` ADD CONSTRAINT `passengers_user_permissi_passenger_id_permission__25761e5b_uniq` UNIQUE (`passenger_id`, `permission_id`);
ALTER TABLE `passengers_user_permissions` ADD CONSTRAINT `passengers_user_perm_passenger_id_626f4e15_fk_passenger` FOREIGN KEY (`passenger_id`) REFERENCES `passengers` (`email`);
ALTER TABLE `passengers_user_permissions` ADD CONSTRAINT `passengers_user_perm_permission_id_8d4b1bf7_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);
ALTER TABLE `cancellations` ADD CONSTRAINT `cancellations_booking_id_a4cfa381_fk_bookings_booking_id` FOREIGN KEY (`booking_id`) REFERENCES `bookings` (`booking_id`);
ALTER TABLE `sms` ADD CONSTRAINT `sms_recepient_id_65c69568_fk_passengers_email` FOREIGN KEY (`recepient_id`) REFERENCES `passengers` (`email`);
ALTER TABLE `seats` ADD CONSTRAINT `seats_flight_id_e61b3bde_fk_flights_flight_id` FOREIGN KEY (`flight_id`) REFERENCES `flights` (`flight_id`);
ALTER TABLE `emails` ADD CONSTRAINT `emails_recepient_id_88069420_fk_passengers_email` FOREIGN KEY (`recepient_id`) REFERENCES `passengers` (`email`);


CREATE TABLE `price` (
    `flight_id` integer NOT NULL,
    `seat_type` varchar(100) NOT NULL,
    `cost` integer NOT NULL,
    PRIMARY KEY ("flight_id", "seat_type"),
)
insert into flights (name, start_time, end_time, source, destination) values ('Flight 1', '2019-01-01 00:00:00', '2019-01-01 00:00:00', 'Delhi', 'Mumbai');
insert into flights (name, start_time, end_time, source, destination) values ('Flight 2', '2019-01-01 00:00:00', '2019-01-01 00:00:00', 'Mumbai', 'Delhi');
insert into price(flight_id, seat_type, cost) values (1, "Economy", 1000);
insert into price(flight_id, seat_type, cost) values (1, "Business", 2000);
insert into price(flight_id, seat_type, cost) values (2, "Economy", 2000);
insert into price(flight_id, seat_type, cost) values (2, "Business", 3000);
insert into seats (flight_id, seat_type) values (1, "Economy");
insert into seats (flight_id, seat_type) values (1, "Economy");
insert into seats (flight_id, seat_type) values (1, "Economy");
insert into seats (flight_id, seat_type) values (1, "Economy");
insert into seats (flight_id, seat_type) values (1, "Economy");
insert into seats (flight_id, seat_type) values (1, "Economy");
insert into seats (flight_id, seat_type) values (1, "Economy");
insert into seats (flight_id, seat_type) values (1, "Economy");
insert into seats (flight_id, seat_type) values (1, "Business");
insert into seats (flight_id, seat_type) values (1, "Business");
insert into seats (flight_id, seat_type) values (1, "Business");
insert into seats (flight_id, seat_type) values (1, "Business");
insert into seats (flight_id, seat_type) values (1, "Business");
insert into seats (flight_id, seat_type) values (1, "Business");
insert into seats (flight_id, seat_type) values (1, "Business");
insert into seats (flight_id, seat_type) values (1, "Business");
insert into seats (flight_id, seat_type) values (2, "Economy");
insert into seats (flight_id, seat_type) values (2, "Economy");
insert into seats (flight_id, seat_type) values (2, "Economy");
insert into seats (flight_id, seat_type) values (2, "Economy");
insert into seats (flight_id, seat_type) values (2, "Economy");
insert into seats (flight_id, seat_type) values (2, "Economy");
insert into seats (flight_id, seat_type) values (2, "Economy");
insert into seats (flight_id, seat_type) values (2, "Economy");
insert into seats (flight_id, seat_type) values (2, "Business");
insert into seats (flight_id, seat_type) values (2, "Business");
insert into seats (flight_id, seat_type) values (2, "Business");
insert into seats (flight_id, seat_type) values (2, "Business");
insert into seats (flight_id, seat_type) values (2, "Business");
insert into seats (flight_id, seat_type) values (2, "Business");
insert into seats (flight_id, seat_type) values (2, "Business");
insert into seats (flight_id, seat_type) values (2, "Business");
drop procedure if exists insert_booking;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE
`insert_booking`(IN seat_id_var int, IN user_id_var varchar(254))
 MODIFIES SQL DATA
 SQL SECURITY INVOKER
BEGIN
start transaction;
set @seat_name = (select concat(seat_type, " ", seat_id%8) from seats where seat_id = seat_id_var); 
set @check = (select count(*) from bookings where seat_id = seat_id_var and status != 'Cancelled');
IF @check < 1
THEN insert into bookings (seat_id, user_id, status, created_at) values (seat_id_var, user_id_var, 'Pending', NOW()); insert into sms (recepient_id, body, created_at) values (user_id_var, concat('Your booking is pending for ', @seat_name), NOW()); insert into emails (recepient_id, subject, body, created_at) values (user_id_var, 'Booking Pending', concat('Your booking is pending for ', @seat_name), NOW());
ELSE insert into sms (recepient_id, body, created_at) values (user_id_var, 'Your booking has failed', NOW()); insert into emails (recepient_id, subject, message, created_at) values (user_id_var, 'Booking Failed', 'Your booking has failed', NOW());
END IF;
commit;
END$$