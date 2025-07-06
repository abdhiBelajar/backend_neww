-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jul 06, 2025 at 12:59 PM
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
-- Database: `db_kesehatan`
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

INSERT INTO `doctors` (`id_dokter`, `nomor_str`, `nama_dokter`, `spesialis`) VALUES
(1, '12', 'ega', 'bedah otak');

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

-- --------------------------------------------------------

--
-- Table structure for table `health_centers`
--

CREATE TABLE `health_centers` (
  `kode_faskes` int NOT NULL,
  `nama_puskesmas` varchar(255) NOT NULL,
  `alamat` varchar(255) NOT NULL,
  `jam_operasional` datetime DEFAULT NULL,
  `nomor_kontak` text,
  `id_dokter` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `health_centers`
--

INSERT INTO `health_centers` (`kode_faskes`, `nama_puskesmas`, `alamat`, `jam_operasional`, `nomor_kontak`, `id_dokter`) VALUES
(1, 'sukses', 'jl.udayana', '2025-07-03 00:08:36', '0184612411234', 1),
(2, 'Puskesmas B', 'sibang kaje', '2024-06-01 08:00:00', '08123456139', 1);

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

INSERT INTO `queues` (`id_antrian`, `id_reservasi`, `nomor_antrian`, `waktu_antrian`) VALUES
(4, 4, 1, '10:00:00'),
(5, 6, 1, '10:00:00');

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

INSERT INTO `reservations` (`id_reservasi`, `id_user`, `id_puskesmas`, `id_layanan`, `id_antrian`, `tanggal_reservasi`, `status`) VALUES
(4, 1, 1, 1, 4, '2024-06-01 10:00:00', 'confirmed'),
(5, 3, 1, 1, 4, '2024-06-01 10:00:00', 'confirmed'),
(6, 3, 2, 1, NULL, '2024-06-01 10:00:00', 'pending'),
(7, 3, 2, 1, NULL, '2024-06-01 10:00:00', 'pending');

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

INSERT INTO `services` (`id_layanan`, `nama_layanan`, `deskripsi`, `tarif`) VALUES
(1, 'tht', 'tengorokan-hidung-telinga', '5000000.00');

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

INSERT INTO `users` (`id_user`, `username`, `password`, `tipe_user`) VALUES
(1, 'admin', 'scrypt:32768:8:1$Wa0gv7C04EMnOpWL$39857f789200ccfa6d6adcab5f53891507020beef9987b2a36673e71e1d7cfbbef3a963695629c3f1d1e2047b3ae365e0e90eb3d9fd0a0f4e05340dc187eb002', 'admin'),
(2, 'teststaff', 'scrypt:32768:8:1$okmG3NG1bf1vW7L5$38aab616fe8ba6d54614f4f1b43c2eedcf3c6160c833e33aa1a8f56a384d3e4bfb169fb6e0b73462d35df9ae55137393f18e00b4530c6b890c3434c365f79690', 'staff'),
(3, 'testpatien', 'scrypt:32768:8:1$D6SCeirmDOWnlLcp$a70d619962c99c7bc1a8f322f47356e03dfd8db5017949fff28316cfca0e85ceb8c9e888d6b8c2f6764cc16c32ffb1b7ef7265d3627b16110c1096cb85c53619', 'patien');

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
  ADD PRIMARY KEY (`kode_faskes`),
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
  MODIFY `id_dokter` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `doctor_schedules`
--
ALTER TABLE `doctor_schedules`
  MODIFY `id_jadwal` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `health_centers`
--
ALTER TABLE `health_centers`
  MODIFY `kode_faskes` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `id_notifikasi` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `queues`
--
ALTER TABLE `queues`
  MODIFY `id_antrian` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `reservations`
--
ALTER TABLE `reservations`
  MODIFY `id_reservasi` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `services`
--
ALTER TABLE `services`
  MODIFY `id_layanan` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id_user` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `doctor_schedules`
--
ALTER TABLE `doctor_schedules`
  ADD CONSTRAINT `doctor_schedules_ibfk_1` FOREIGN KEY (`nomor_str`) REFERENCES `doctors` (`nomor_str`);

--
-- Constraints for table `health_centers`
--
ALTER TABLE `health_centers`
  ADD CONSTRAINT `health_centers_ibfk_1` FOREIGN KEY (`id_dokter`) REFERENCES `doctors` (`id_dokter`);

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`);

--
-- Constraints for table `queues`
--
ALTER TABLE `queues`
  ADD CONSTRAINT `queues_ibfk_1` FOREIGN KEY (`id_reservasi`) REFERENCES `reservations` (`id_reservasi`);

--
-- Constraints for table `reservations`
--
ALTER TABLE `reservations`
  ADD CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`id_antrian`) REFERENCES `queues` (`id_antrian`),
  ADD CONSTRAINT `reservations_ibfk_2` FOREIGN KEY (`id_puskesmas`) REFERENCES `health_centers` (`kode_faskes`),
  ADD CONSTRAINT `reservations_ibfk_3` FOREIGN KEY (`id_layanan`) REFERENCES `services` (`id_layanan`),
  ADD CONSTRAINT `reservations_ibfk_4` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
