-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-12-27 10:43:47
-- 伺服器版本： 10.4.32-MariaDB
-- PHP 版本： 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `diagram`
--

-- --------------------------------------------------------

--
-- 資料表結構 `customer`
--

CREATE TABLE `customer` (
  `id` int(100) NOT NULL,
  `name` varchar(30) NOT NULL,
  `contact_info` varchar(30) NOT NULL,
  `address` varchar(30) DEFAULT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `customer`
--

INSERT INTO `customer` VALUES 
(1,'Alice','alice@example.com','123 Maple St','password123'),
(2,'Bob','bob@example.com','456 Oak St','password123'),
(3,'Charlie','charlie@example.com','789 Pine St','password123'),
(4,'Diana','diana@example.com','321 Birch St','password123'),
(5,'Eve','eve@example.com','654 Cedar St','password123'),
(6,'Frank','frank@example.com','987 Elm St','password123'),
(7,'Grace','grace@example.com','147 Spruce St','password123'),
(8,'Henry','henry@example.com','258 Willow St','password123'),
(9,'Ivy','ivy@example.com','369 Redwood St','password123'),
(10,'Jack','jack@example.com','741 Palm St','password123');

-- --------------------------------------------------------

--
-- 資料表結構 `deliveryperson`
--

CREATE TABLE `deliveryperson` (
  `id` int(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `vehicle_info` varchar(100) NOT NULL,
  `contact_info` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `deliveryperson`
--

INSERT INTO `deliveryperson` VALUES 
(1,'Liam','scooter','liam@example.com','delivery123'),
(2,'Noah','scooter','noah@example.com','delivery123'),
(3,'Olivia','scooter','olivia@example.com','delivery123'),
(4,'Emma','scooter','emma@example.com','delivery123'),
(5,'Ava','scooter','ava@example.com','delivery123'),
(6,'Sophia','scooter','sophia@example.com','delivery123'),
(7,'Mason','scooter','mason@example.com','delivery123'),
(8,'Lucas','scooter','lucas@example.com','delivery123'),
(9,'Logan','scooter','logan@example.com','delivery123'),
(10,'Mia','scooter','mia@example.com','delivery123');

-- --------------------------------------------------------

--
-- 資料表結構 `feedback`
--

CREATE TABLE `feedback` (
  `id` int(100) NOT NULL,
  `customer_id` int(100) NOT NULL,
  `feedback_text` varchar(30) NOT NULL,
  `rating` int(100) NOT NULL,
  `created_at` date NOT NULL,
  `deliveryperson_id` int(11) DEFAULT NULL,
  `merchant_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `feedback`
--

INSERT INTO `feedback` (`id`, `customer_id`, `feedback_text`, `rating`, `created_at`, `deliveryperson_id`, `merchant_id`) VALUES
(1, 1, '快速送達，非常滿意！', 5, '2024-12-26', 5, NULL),
(2, 2, '送貨員態度友善，但有點遲到。', 4, '2024-12-26', 4, NULL),
(3, 3, '服務很好，送貨員很專業！', 5, '2024-12-26', 3, NULL),
(4, 4, '配送速度有點慢，還好物品完好無損。', 3, '2024-12-26', 2, NULL),
(5, 5, '非常滿意，送貨員很有禮貌！', 5, '2024-12-26', 3, NULL),
(6, 1, '商品質量很好，會再來購買！', 5, '2024-12-26', NULL, 4),
(7, 2, '商店服務不錯，但價格有點高。', 4, '2024-12-26', NULL, 4),
(8, 3, '商品包裝很好，滿意的購物體驗。', 5, '2024-12-26', NULL, 3),
(9, 4, '配送時間太長，商店應該改進物流。', 3, '2024-12-26', NULL, 4),
(10, 5, '商品選擇多樣，客服回應迅速。', 4, '2024-12-26', NULL, 1);

-- --------------------------------------------------------

--
-- 資料表結構 `menuitem`
--

CREATE TABLE `menuitem` (
  `id` int(30) NOT NULL,
  `name` varchar(100) NOT NULL,
  `price` float NOT NULL,
  `description` varchar(100) NOT NULL,
  `availability_status` varchar(100) NOT NULL,
  `merchant_id` int(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `menuitem`
--

INSERT INTO `menuitem` (`id`, `name`, `price`, `description`, `availability_status`, `merchant_id`) VALUES
(1, 'Spaghetti Carbonara', 250, 'Classic Italian pasta with creamy sauce, pancetta, and Parmesan cheese.', '販售中', 1),
(3, 'Caesar Salad', 150, 'Crisp romaine lettuce with Caesar dressing, croutons, and Parmesan cheese.', '非販售', 3),
(4, 'Chicken Tikka Masala', 280, 'Tender chicken pieces in a flavorful tomato-based curry sauce.', '販售中', 1),
(5, 'Beef Burger', 220, 'Juicy beef patty with lettuce, tomato, cheese, and a soft bun.', '販售中', 3),
(6, 'Vegetable Stir Fry', 180, 'A healthy mix of seasonal vegetables stir-fried in soy sauce.', '販售中', 1);

-- --------------------------------------------------------

--
-- 資料表結構 `merchant`
--

CREATE TABLE `merchant` (
  `id` int(30) NOT NULL,
  `name` varchar(100) NOT NULL,
  `location` varchar(100) NOT NULL,
  `contact_info` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `merchant`
--

INSERT INTO `merchant` VALUES 
(1,'Nike','123 Sport Ave','nike@example.com','securepass123'),
(2,'Adidas','456 Run St','adidas@example.com','securepass123'),
(3,'Puma','789 Track Rd','puma@example.com','securepass123'),
(4,'Reebok','321 Fitness Blvd','reebok@example.com','securepass123'),
(5,'UnderArmour','654 Gym Lane','underarmour@example.com','securepass123'),
(6,'NewBalance','987 Comfort Way','newbalance@example.com','securepass123'),
(7,'Asics','147 Marathon Dr','asics@example.com','securepass123'),
(8,'Skechers','258 Walk St','skechers@example.com','securepass123'),
(9,'Columbia','369 Adventure Blvd','columbia@example.com','securepass123'),
(10,'Patagonia','741 Outdoor Ave','patagonia@example.com','securepass123');

-- --------------------------------------------------------

--
-- 資料表結構 `orde`
--

CREATE TABLE `orde` (
  `id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `merchant_id` int(100) NOT NULL,
  `delivery_person_id` int(100) NOT NULL,
  `status` varchar(100) NOT NULL,
  `delivery_address` varchar(100) NOT NULL,
  `total_price` double NOT NULL,
  `created_at` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `orde`
--

INSERT INTO `orde` (`id`, `customer_id`, `merchant_id`, `delivery_person_id`, `status`, `delivery_address`, `total_price`, `created_at`) VALUES
(1, 1, 1, 1, '已送達', 'Taipei City, 123 Main St', 500, '2024-12-26'),
(2, 2, 2, 2, '正在配送', 'Kaohsiung City, 456 Central Ave', 600, '2024-12-26'),
(3, 3, 3, 3, '已送達', 'Taichung City, 789 Park Rd', 700, '2024-12-26'),
(4, 4, 4, 4, '取消', 'Taipei City, 1011 East Blvd', 450, '2024-12-26'),
(5, 5, 5, 5, '已送達', 'Taichung City, 1213 North St', 550, '2024-12-26'),
(6, 6, 1, 1, '正在配送', 'Taipei City, 1415 South Ave', 520, '2024-12-26'),
(7, 7, 2, 2, '已送達', 'Kaohsiung City, 1617 West Rd', 650, '2024-12-26'),
(8, 8, 3, 3, '正在配送', 'Taichung City, 1819 East Rd', 480, '2024-12-26'),
(9, 9, 4, 4, '已送達', 'Taipei City, 2021 Central St', 540, '2024-12-26'),
(10, 10, 5, 5, '取消', 'Taichung City, 2223 North Ave', 590, '2024-12-26'),
(11, 11, 1, 1, '已送達', 'Taipei City, 2425 West Blvd', 600, '2024-12-26'),
(12, 12, 2, 2, '正在配送', 'Kaohsiung City, 2627 South Rd', 470, '2024-12-26'),
(13, 13, 3, 3, '已送達', 'Taichung City, 2829 Central St', 710, '2024-12-26'),
(14, 14, 4, 4, '取消', 'Taipei City, 3031 North Blvd', 500, '2024-12-27'),
(15, 15, 5, 5, '已送達', 'Taichung City, 3233 West Ave', 520, '2024-12-27'),
(16, 16, 1, 1, '正在配送', 'Taipei City, 3435 East Rd', 530, '2024-12-27'),
(17, 17, 2, 2, '已送達', 'Kaohsiung City, 3637 South St', 640, '2024-12-27'),
(18, 18, 3, 3, '正在配送', 'Taichung City, 3839 North Rd', 560, '2024-12-27'),
(19, 19, 4, 4, '已送達', 'Taipei City, 4041 West Blvd', 450, '2024-12-27'),
(20, 20, 5, 5, '取消', 'Taichung City, 4243 East St', 590, '2024-12-27');

-- --------------------------------------------------------

--
-- 資料表結構 `orderitem`
--

CREATE TABLE `orderitem` (
  `id` int(100) NOT NULL,
  `order_id` int(100) NOT NULL,
  `menu_item_id` int(100) NOT NULL,
  `quantity` int(100) NOT NULL,
  `price` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `orderitem`
--

INSERT INTO `orderitem` (`id`, `order_id`, `menu_item_id`, `quantity`, `price`) VALUES
(1, 1, 1, 2, 250),
(2, 1, 2, 1, 200),
(3, 2, 3, 1, 150),
(4, 2, 4, 2, 280),
(5, 3, 5, 1, 220),
(6, 3, 6, 1, 180),
(7, 4, 1, 3, 250),
(8, 4, 2, 1, 200),
(9, 5, 3, 2, 150),
(10, 5, 4, 1, 280),
(11, 6, 5, 2, 220),
(12, 6, 6, 1, 180),
(13, 7, 1, 1, 250),
(14, 7, 2, 1, 200),
(15, 8, 3, 2, 150),
(16, 8, 4, 1, 280),
(17, 9, 5, 1, 220),
(18, 9, 6, 2, 180),
(19, 10, 1, 1, 250),
(20, 10, 2, 2, 200),
(21, 11, 3, 1, 150);

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `deliveryperson`
--
ALTER TABLE `deliveryperson`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `menuitem`
--
ALTER TABLE `menuitem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `merchant_id` (`merchant_id`);

--
-- 資料表索引 `merchant`
--
ALTER TABLE `merchant`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `orde`
--
ALTER TABLE `orde`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `orderitem`
--
ALTER TABLE `orderitem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `customer`
--
ALTER TABLE `customer`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `deliveryperson`
--
ALTER TABLE `deliveryperson`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `feedback`
--
ALTER TABLE `feedback`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `menuitem`
--
ALTER TABLE `menuitem`
  MODIFY `id` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `merchant`
--
ALTER TABLE `merchant`
  MODIFY `id` int(30) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `orde`
--
ALTER TABLE `orde`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `orderitem`
--
ALTER TABLE `orderitem`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `menuitem`
--
ALTER TABLE `menuitem`
  ADD CONSTRAINT `merchant_id` FOREIGN KEY (`merchant_id`) REFERENCES `merchant` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- 資料表的限制式 `orderitem`
--
ALTER TABLE `orderitem`
  ADD CONSTRAINT `order_id` FOREIGN KEY (`order_id`) REFERENCES `orde` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
