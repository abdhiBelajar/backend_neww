-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 08, 2025 at 02:38 PM
-- Server version: 8.0.30
-- PHP Version: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_health_centers`
--

-- --------------------------------------------------------

--
-- Table structure for table `doctors`
--

CREATE TABLE `doctors` (
  `id_dokter` int NOT NULL,
  `nomor_str` varchar(255) NOT NULL,
  `nama_dokter` varchar(255) NOT NULL,
  `spesialis` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `doctors`
--

-- --------------------------------------------------------

--
-- Table structure for table `doctor_schedules`
--

CREATE TABLE `doctor_schedules` (
  `id_jadwal` int NOT NULL,
  `nomor_str` varchar(255) NOT NULL,
  `hari` enum('Senin','Selasa','Rabu','Kamis','Jumat','Sabtu','Minggu') NOT NULL,
  `jam_mulai` time NOT NULL,
  `jam_selesai` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `doctor_schedules`
--

-- --------------------------------------------------------

--
-- Table structure for table `health_centers`
--

CREATE TABLE `health_centers` (
  `id_puskesmas` int NOT NULL,
  `kode_faskes` int NOT NULL,
  `nama_puskesmas` varchar(255) NOT NULL,
  `alamat` varchar(255) NOT NULL,
  `jam_operasional` json DEFAULT NULL,
  `nomor_kontak` text,
  `id_dokter` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `health_centers`
--

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `id_notifikasi` int NOT NULL,
  `id_user` bigint NOT NULL,
  `pesan` text NOT NULL,
  `tanggal_notifikasi` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `queues`
--

CREATE TABLE `queues` (
  `id_antrian` int NOT NULL,
  `id_reservasi` int NOT NULL,
  `nomor_antrian` int NOT NULL,
  `waktu_antrian` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `queues`
--

-- --------------------------------------------------------

--
-- Table structure for table `reservations`
--

CREATE TABLE `reservations` (
  `id_reservasi` int NOT NULL,
  `id_user` bigint NOT NULL,
  `id_puskesmas` int NOT NULL,
  `id_layanan` int NOT NULL,
  `id_antrian` int DEFAULT NULL,
  `tanggal_reservasi` datetime NOT NULL,
  `status` enum('pending','confirmed','cancelled') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `reservations`
--

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `id_layanan` int NOT NULL,
  `nama_layanan` varchar(255) NOT NULL,
  `deskripsi` text,
  `tarif` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `services`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id_user` bigint NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `tipe_user` enum('admin','staff','patien') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

--
-- Indexes for dumped tables
--

--
-- Indexes for table `doctors`
--
ALTER TABLE `doctors`
  ADD PRIMARY KEY (`id_dokter`),
  ADD UNIQUE KEY `nomor_str` (`nomor_str`);

--
-- Indexes for table `doctor_schedules`
--
ALTER TABLE `doctor_schedules`
  ADD PRIMARY KEY (`id_jadwal`),
  ADD KEY `nomor_str` (`nomor_str`);

--
-- Indexes for table `health_centers`
--
ALTER TABLE `health_centers`
  ADD PRIMARY KEY (`id_puskesmas`),
  ADD KEY `id_dokter` (`id_dokter`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`id_notifikasi`),
  ADD KEY `id_user` (`id_user`);

--
-- Indexes for table `queues`
--
ALTER TABLE `queues`
  ADD PRIMARY KEY (`id_antrian`),
  ADD KEY `id_reservasi` (`id_reservasi`);

--
-- Indexes for table `reservations`
--
ALTER TABLE `reservations`
  ADD PRIMARY KEY (`id_reservasi`),
  ADD KEY `id_antrian` (`id_antrian`),
  ADD KEY `id_puskesmas` (`id_puskesmas`),
  ADD KEY `id_layanan` (`id_layanan`),
  ADD KEY `id_user` (`id_user`);

--
-- Indexes for table `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`id_layanan`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `doctors`
--
ALTER TABLE `doctors`
  MODIFY `id_dokter` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `doctor_schedules`
--
ALTER TABLE `doctor_schedules`
  MODIFY `id_jadwal` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `health_centers`
--
ALTER TABLE `health_centers`
  MODIFY `id_puskesmas` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id_notifikasi` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `queues`
--
ALTER TABLE `queues`
  MODIFY `id_antrian` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `reservations`
--
ALTER TABLE `reservations`
  MODIFY `id_reservasi` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;

--
-- AUTO_INCREMENT for table `services`
--
ALTER TABLE `services`
  MODIFY `id_layanan` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id_user` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `doctor_schedules`
--
ALTER TABLE `doctor_schedules`
  ADD CONSTRAINT `doctor_schedules_ibfk_1` FOREIGN KEY (`nomor_str`) REFERENCES `doctors` (`nomor_str`) ON DELETE CASCADE;

--
-- Constraints for table `health_centers`
--
ALTER TABLE `health_centers`
  ADD CONSTRAINT `health_centers_ibfk_1` FOREIGN KEY (`id_dokter`) REFERENCES `doctors` (`id_dokter`) ON DELETE CASCADE;

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`) ON DELETE CASCADE;

--
-- Constraints for table `queues`
--
ALTER TABLE `queues`
  ADD CONSTRAINT `queues_ibfk_1` FOREIGN KEY (`id_reservasi`) REFERENCES `reservations` (`id_reservasi`) ON DELETE CASCADE;

--
-- Constraints for table `reservations`
--
ALTER TABLE `reservations`
  ADD CONSTRAINT `fk_reservations_id_puskesmas` FOREIGN KEY (`id_puskesmas`) REFERENCES `health_centers` (`id_puskesmas`) ON DELETE CASCADE,
  ADD CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`id_antrian`) REFERENCES `queues` (`id_antrian`) ON DELETE CASCADE,
  ADD CONSTRAINT `reservations_ibfk_3` FOREIGN KEY (`id_layanan`) REFERENCES `services` (`id_layanan`) ON DELETE CASCADE,
  ADD CONSTRAINT `reservations_ibfk_4` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
