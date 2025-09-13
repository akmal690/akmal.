-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 09, 2025 at 11:18 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `shop_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `id` int(100) NOT NULL,
  `name` varchar(20) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`id`, `name`, `password`) VALUES
(1, 'admin', '6216f8a75fd5bb3d5f22b6f9958cdede3fc086c2');

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `id` int(100) NOT NULL,
  `user_id` int(100) NOT NULL,
  `pid` int(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `price` int(10) NOT NULL,
  `quantity` int(10) NOT NULL,
  `image` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `fraud_attempts`
--

CREATE TABLE `fraud_attempts` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `typing_speed` float DEFAULT NULL,
  `time_on_page` int(11) DEFAULT NULL,
  `payment_type` varchar(50) DEFAULT NULL,
  `reason` text DEFAULT NULL,
  `attempt_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `fraud_attempts`
--

INSERT INTO `fraud_attempts` (`id`, `user_id`, `typing_speed`, `time_on_page`, `payment_type`, `reason`, `attempt_date`) VALUES
(1, 1, 53, 91, 'cash on delivery', 'Fraud detected', '2025-07-08 11:14:49'),
(2, 1, 0, 28, 'cash on delivery', 'Verification successful', '2025-07-08 11:15:17'),
(3, 1, 18, 17, 'paytm', 'Verification successful', '2025-07-08 11:16:25'),
(4, 1, 0, 5, 'credit card', 'Verification successful', '2025-07-08 11:16:37'),
(5, 1, 0, 5, 'credit card', 'Based on past similar attempt: Verification successful', '2025-07-08 11:16:42'),
(6, 1, 0, 17, 'cash on delivery', 'Verification successful', '2025-07-08 11:17:00'),
(7, 1, 5, 13, 'paypal', 'Verification successful', '2025-07-08 11:19:01'),
(8, 1, 5, 12, 'credit card', 'Verification successful', '2025-07-08 11:56:55'),
(9, 1, 9, 13, 'cash on delivery', 'Verification successful', '2025-07-08 11:57:46'),
(10, 1, 0, 43, 'cash on delivery', 'Verification successful', '2025-07-08 15:44:28'),
(11, 1, 0, 8, 'cash on delivery', 'Verification successful', '2025-07-08 15:46:22'),
(12, 1, 4, 30, 'cash on delivery', 'Verification successful', '2025-07-09 03:39:04'),
(13, 1, 8, 8, 'cash on delivery', 'Verification successful', '2025-07-09 04:49:23'),
(14, 1, 0, 3, 'cash on delivery', 'Verification successful', '2025-07-09 04:50:54'),
(15, 1, 28, 26, 'cash on delivery', 'Verification successful', '2025-07-09 05:28:36'),
(16, 1, 52, 78, 'cash on delivery', 'Fraud detected', '2025-07-09 05:30:35'),
(17, 1, 15, 72, 'cash on delivery', 'Fraud detected', '2025-07-09 05:31:47'),
(18, 1, 22, 47, 'cash on delivery', 'Fraud detected', '2025-07-09 05:32:34'),
(19, 1, 0, 53, 'cash on delivery', 'Verification successful', '2025-07-09 05:33:28'),
(20, 1, 5, 13, 'cash on delivery', 'Verification successful', '2025-07-09 06:56:23'),
(21, 1, 41, 74, 'cash on delivery', 'Fraud detected', '2025-07-09 06:59:54'),
(22, 1, 21, 29, 'cash on delivery', 'Verification successful', '2025-07-09 08:18:00'),
(23, 1, 26, 89, 'cash on delivery', 'Fraud detected', '2025-07-09 08:32:28'),
(24, 1, 29, 41, 'cash on delivery', 'Fraud detected', '2025-07-09 08:44:50'),
(25, 1, 32, 19, 'cash on delivery', 'Verification successful', '2025-07-09 08:46:07'),
(26, 1, 12, 10, 'cash on delivery', 'Verification successful', '2025-07-09 08:58:17');

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `id` int(100) NOT NULL,
  `user_id` int(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `number` varchar(12) NOT NULL,
  `message` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `user_id` int(100) NOT NULL,
  `name` varchar(20) NOT NULL,
  `number` varchar(10) NOT NULL,
  `email` varchar(50) NOT NULL,
  `method` varchar(50) NOT NULL,
  `address` varchar(500) NOT NULL,
  `total_products` varchar(1000) NOT NULL,
  `total_price` int(100) NOT NULL,
  `placed_on` date NOT NULL DEFAULT current_timestamp(),
  `payment_status` varchar(20) NOT NULL DEFAULT 'pending'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `user_id`, `name`, `number`, `email`, `method`, `address`, `total_products`, `total_price`, `placed_on`, `payment_status`) VALUES
(1, 1, 'akmal', '0764514341', 'akmal22720@gmail.com', 'cash on delivery', 'flat no. 199/2, kallarichal-2, sammanturi, eastan, Sri Lanka - 22', 'paint (20000 x 1) - ', 20000, '2025-07-06', 'pending'),
(2, 1, 'akmal', '0764514341', 'akmal22720@gmail.com', 'cash on delivery', 'flat no. 199/2, kallarichal-2, sammanturi, eastan, Sri Lanka - 22', 'paint (20000 x 1) - ', 20000, '2025-07-06', 'pending'),
(4, 1, 'akmal', '0772301821', 'akmal22720@gmail.com', 'cash on delivery', 'flat no. 199/2, kallarichal-2, sammanturi, eastan, Sri Lanka - 22', 'oil pains (18999 x 1) - ', 18999, '2025-07-09', 'completed'),
(5, 1, 'akmal', '0772301821', 'akmal22720@gmail.com', 'cash on delivery', 'flat no. abxbcxxcn, xbx, dgvdcxx c, EASTERN, Sri Lanka - 59', 'paint (20000 x 1) - ', 20000, '2025-07-09', 'pending'),
(7, 1, 'akmal', '0772301821', 'akmal723@gmail.com', 'cash on delivery', 'flat no. 20/2, kalacal-2, sammanturi, EASTERN, Sri Lanka - 56', 'paint (20000 x 1) - ', 20000, '2025-07-09', 'pending');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `details` varchar(500) NOT NULL,
  `price` int(10) NOT NULL,
  `image_01` varchar(100) NOT NULL,
  `image_02` varchar(100) NOT NULL,
  `image_03` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `details`, `price`, `image_01`, `image_02`, `image_03`) VALUES
(0, 'scotdriver', ' using good for hand', 1300, '10.jpeg', '1010.webp', '101010.webp'),
(1, 'oil pains', 'best', 18999, '22.webp', '2.jpeg', '222.webp'),
(2, 'paint', 'good ', 20000, '1.jpeg', '11.png', '111.jpeg'),
(3, 'cement', 'stong', 2700, '7.jpg', '77.jpeg', '777.jpg'),
(4, 'sink', 'super good', 11999, '6.jpeg', '666.jpg', '66.webp'),
(5, 'spar', '99+couler', 1999, '3.jpeg', '33.jpeg', '333.jpg'),
(6, 'mortar', 'worondi', 2000, '5.png', '55.jpeg', '555.jpeg'),
(7, 'door lock', 'safe ', 10000, '8.jpeg', '88.jpeg', '888.webp');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`) VALUES
(1, 'akmal', 'akmal22720@gmail.com', 'd26d38e1b40c51aa346b6a5a0ccd598bf030566d'),
(2, 'afsan', 'afsan2006@gmail.com', '456d7a498ea50747a913c00d9f5ba827c32ca099');

-- --------------------------------------------------------

--
-- Table structure for table `wishlist`
--

CREATE TABLE `wishlist` (
  `id` int(100) NOT NULL,
  `user_id` int(100) NOT NULL,
  `pid` int(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `price` int(100) NOT NULL,
  `image` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `fraud_attempts`
--
ALTER TABLE `fraud_attempts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `fraud_attempts`
--
ALTER TABLE `fraud_attempts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `fraud_attempts`
--
ALTER TABLE `fraud_attempts`
  ADD CONSTRAINT `fraud_attempts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
