-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 20 Jan 2025 pada 06.50
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `inventory_db`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `admin`
--

INSERT INTO `admin` (`id`, `username`, `password`, `created_at`) VALUES
(1, 'sandy', '5c80565db6f29da0b01aa12522c37b32f121cbe47a861ef7f006cb22922dffa1', '2025-01-20 01:07:00');

-- --------------------------------------------------------

--
-- Struktur dari tabel `audit_log`
--

CREATE TABLE `audit_log` (
  `id` int(11) NOT NULL,
  `table_name` varchar(50) NOT NULL,
  `record_id` int(11) DEFAULT NULL,
  `action_type` enum('INSERT','UPDATE','DELETE') NOT NULL,
  `old_values` text DEFAULT NULL,
  `new_values` text DEFAULT NULL,
  `admin_id` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `audit_log`
--

INSERT INTO `audit_log` (`id`, `table_name`, `record_id`, `action_type`, `old_values`, `new_values`, `admin_id`, `timestamp`) VALUES
(1, 'categories', NULL, 'INSERT', NULL, '{\"id\": null, \"name\": \"makanan\"}', 1, '2025-01-20 01:08:01'),
(2, 'items', 1, 'INSERT', NULL, '{\"name\": \"roti\", \"quantity\": 20, \"price\": 2000.0, \"description\": \"roti\", \"category_id\": 1, \"unit\": \"pcs\"}', 1, '2025-01-20 01:08:48'),
(3, 'items', 1, 'UPDATE', '{\"name\": \"roti\", \"quantity\": 20, \"price\": \"2000.00\", \"description\": \"roti\", \"category_id\": 1, \"unit\": \"pcs\"}', '{\"name\": \"sosis\", \"quantity\": 20, \"price\": 2000.0, \"description\": \"roti\", \"category_id\": 1, \"unit\": \"pcs\"}', 1, '2025-01-20 01:09:30'),
(4, 'items', 1, 'UPDATE', '{\"name\": \"sosis\", \"quantity\": 20, \"price\": \"2000.00\", \"description\": \"roti\", \"category_id\": 1, \"unit\": \"pcs\"}', '{\"name\": \"sosis\", \"quantity\": 30, \"price\": \"2000.00\", \"description\": \"roti\", \"category_id\": 1, \"unit\": \"pcs\"}', 1, '2025-01-20 01:10:03'),
(5, 'items', 1, 'UPDATE', '{\"name\": \"sosis\", \"quantity\": 30, \"price\": \"2000.00\", \"description\": \"roti\", \"category_id\": 1, \"unit\": \"pcs\"}', '{\"name\": \"sosis\", \"quantity\": 25, \"price\": \"2000.00\", \"description\": \"roti\", \"category_id\": 1, \"unit\": \"pcs\"}', 1, '2025-01-20 01:10:26'),
(6, 'categories', NULL, 'INSERT', NULL, '{\"id\": null, \"name\": \"minuman\"}', 1, '2025-01-20 01:10:52'),
(7, 'items', 2, 'INSERT', NULL, '{\"name\": \"kopi\", \"quantity\": 15, \"price\": 2500.0, \"description\": \"kopi\", \"category_id\": 2, \"unit\": \"sacet\"}', 1, '2025-01-20 01:11:27'),
(8, 'items', 2, 'DELETE', '{\"id\": 2, \"name\": \"kopi\", \"quantity\": 15, \"price\": \"2500.00\", \"description\": \"kopi\", \"category_id\": 2, \"unit\": \"sacet\", \"is_deleted\": 0, \"created_at\": \"2025-01-20T08:11:27\", \"updated_at\": \"2025-01-20T08:11:27\", \"category_name\": \"minuman\"}', NULL, 1, '2025-01-20 01:12:08');

-- --------------------------------------------------------

--
-- Struktur dari tabel `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `categories`
--

INSERT INTO `categories` (`id`, `name`, `created_at`) VALUES
(1, 'makanan', '2025-01-20 01:08:01'),
(2, 'minuman', '2025-01-20 01:10:52');

-- --------------------------------------------------------

--
-- Struktur dari tabel `history`
--

CREATE TABLE `history` (
  `id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `admin_id` int(11) NOT NULL,
  `change_type` enum('in','out','delete') NOT NULL,
  `quantity_change` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `history`
--

INSERT INTO `history` (`id`, `item_id`, `admin_id`, `change_type`, `quantity_change`, `timestamp`) VALUES
(1, 1, 1, 'in', 10, '2025-01-20 01:10:03'),
(2, 1, 1, 'out', 5, '2025-01-20 01:10:26');

-- --------------------------------------------------------

--
-- Struktur dari tabel `items`
--

CREATE TABLE `items` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `description` text DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `unit` varchar(50) DEFAULT 'pcs',
  `is_deleted` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `items`
--

INSERT INTO `items` (`id`, `name`, `quantity`, `price`, `description`, `category_id`, `unit`, `is_deleted`, `created_at`, `updated_at`) VALUES
(1, 'sosis', 25, 2000.00, 'roti', 1, 'pcs', 0, '2025-01-20 01:08:48', '2025-01-20 01:10:26');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indeks untuk tabel `audit_log`
--
ALTER TABLE `audit_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `admin_id` (`admin_id`);

--
-- Indeks untuk tabel `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indeks untuk tabel `history`
--
ALTER TABLE `history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `item_id` (`item_id`),
  ADD KEY `admin_id` (`admin_id`);

--
-- Indeks untuk tabel `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `category_id` (`category_id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `audit_log`
--
ALTER TABLE `audit_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT untuk tabel `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `history`
--
ALTER TABLE `history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `items`
--
ALTER TABLE `items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `audit_log`
--
ALTER TABLE `audit_log`
  ADD CONSTRAINT `audit_log_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `history`
--
ALTER TABLE `history`
  ADD CONSTRAINT `history_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `history_ibfk_2` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `items`
--
ALTER TABLE `items`
  ADD CONSTRAINT `items_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
