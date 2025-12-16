-- إنشاء جداول API
-- تأكد من تشغيلها بالترتيب

-- 1. جدول Doctor (الأطباء)
CREATE TABLE IF NOT EXISTS `api_doctor` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `user_id` bigint NOT NULL UNIQUE,
    `specialty` varchar(150) NOT NULL DEFAULT 'عام',
    `bio` longtext NOT NULL,
    `schedule` longtext NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `api_doctor_user_id_unique` (`user_id`),
    CONSTRAINT `api_doctor_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. جدول Patient (المرضى) - إذا لم يكن موجوداً
CREATE TABLE IF NOT EXISTS `api_patient` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `user_id` bigint NOT NULL UNIQUE,
    `phone` varchar(30) DEFAULT NULL,
    `dob` date DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `api_patient_user_id_unique` (`user_id`),
    CONSTRAINT `api_patient_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. جدول TestType (أنواع الفحوصات)
CREATE TABLE IF NOT EXISTS `api_testtype` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `name` varchar(200) NOT NULL,
    `description` longtext NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. جدول Result (النتائج)
CREATE TABLE IF NOT EXISTS `api_result` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `patient_id` bigint NOT NULL,
    `test_type_id` bigint DEFAULT NULL,
    `value` longtext NOT NULL,
    `notes` longtext NOT NULL,
    `created_at` datetime(6) NOT NULL,
    PRIMARY KEY (`id`),
    KEY `api_result_patient_id_idx` (`patient_id`),
    KEY `api_result_test_type_id_idx` (`test_type_id`),
    CONSTRAINT `api_result_patient_id_fk` FOREIGN KEY (`patient_id`) REFERENCES `api_patient` (`id`) ON DELETE CASCADE,
    CONSTRAINT `api_result_test_type_id_fk` FOREIGN KEY (`test_type_id`) REFERENCES `api_testtype` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. جدول File (الملفات)
CREATE TABLE IF NOT EXISTS `api_file` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `result_id` bigint NOT NULL,
    `file` varchar(100) NOT NULL,
    `uploaded_at` datetime(6) NOT NULL,
    PRIMARY KEY (`id`),
    KEY `api_file_result_id_idx` (`result_id`),
    CONSTRAINT `api_file_result_id_fk` FOREIGN KEY (`result_id`) REFERENCES `api_result` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. جدول Appointment (المواعيد)
CREATE TABLE IF NOT EXISTS `api_appointment` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `patient_id` bigint NOT NULL,
    `doctor_id` bigint NOT NULL,
    `date` datetime(6) NOT NULL,
    `status` varchar(20) NOT NULL DEFAULT 'pending',
    `notes` longtext NOT NULL,
    `created_at` datetime(6) NOT NULL,
    PRIMARY KEY (`id`),
    KEY `api_appointment_patient_id_idx` (`patient_id`),
    KEY `api_appointment_doctor_id_idx` (`doctor_id`),
    KEY `api_appointment_date_idx` (`date`),
    CONSTRAINT `api_appointment_patient_id_fk` FOREIGN KEY (`patient_id`) REFERENCES `api_patient` (`id`) ON DELETE CASCADE,
    CONSTRAINT `api_appointment_doctor_id_fk` FOREIGN KEY (`doctor_id`) REFERENCES `api_doctor` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. جدول Message (الرسائل)
CREATE TABLE IF NOT EXISTS `api_message` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `sender_id` bigint NOT NULL,
    `recipient_id` bigint NOT NULL,
    `subject` varchar(255) NOT NULL,
    `body` longtext NOT NULL,
    `is_read` tinyint(1) NOT NULL DEFAULT 0,
    `created_at` datetime(6) NOT NULL,
    PRIMARY KEY (`id`),
    KEY `api_message_sender_id_idx` (`sender_id`),
    KEY `api_message_recipient_id_idx` (`recipient_id`),
    KEY `api_message_created_at_idx` (`created_at`),
    CONSTRAINT `api_message_sender_id_fk` FOREIGN KEY (`sender_id`) REFERENCES `accounts_customuser` (`id`) ON DELETE CASCADE,
    CONSTRAINT `api_message_recipient_id_fk` FOREIGN KEY (`recipient_id`) REFERENCES `accounts_customuser` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- تم إنشاء جميع الجداول بنجاح!
