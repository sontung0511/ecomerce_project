-- phpMyAdmin SQL Dump
-- version 4.8.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Dec 13, 2018 at 03:36 AM
-- Server version: 10.1.34-MariaDB
-- PHP Version: 7.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ecommerce1`
--

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `categoryID` mediumint(9) NOT NULL,
  `categoryName` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`categoryID`, `categoryName`) VALUES
(3, 'Phone'),
(4, 'Speakers'),
(5, 'Desktop PC'),
(7, 'Monitor'),
(9, 'Laptop');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `orderID` mediumint(9) NOT NULL,
  `userID` mediumint(9) NOT NULL,
  `statusID` mediumint(9) NOT NULL,
  `totalPrice` decimal(10,2) NOT NULL DEFAULT '0.00',
  `date_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `orders_detail`
--

CREATE TABLE `orders_detail` (
  `orderID` mediumint(9) NOT NULL,
  `productID` mediumint(9) NOT NULL,
  `quantity` decimal(5,0) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `payment`
--

CREATE TABLE `payment` (
  `paymentID` mediumint(9) NOT NULL,
  `userID` mediumint(9) NOT NULL,
  `orderID` mediumint(9) NOT NULL,
  `totalPrice` decimal(20,0) DEFAULT NULL,
  `shippingMethod` varchar(25) NOT NULL,
  `datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `productID` mediumint(9) NOT NULL,
  `categoryID` mediumint(9) NOT NULL,
  `productName` varchar(50) NOT NULL,
  `description` varchar(300) NOT NULL,
  `image` varchar(50) NOT NULL,
  `price` decimal(6,2) NOT NULL,
  `quantity` decimal(5,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`productID`, `categoryID`, `productName`, `description`, `image`, `price`, `quantity`) VALUES
(6, 3, 'Google Pixel', 'Meet Pixel. Possibilities by you. Phone by Google. The power of Google, at your fingertips. Every touch, every interaction, every moment, made easy. ', '/static/profile_pics/36ef602bedda249a.png', '1149.00', '4'),
(7, 3, 'Samsung Galaxy s9', 'Introducing the revolutionary Galaxy S9. The phone that reimagines the camera. And in doing so reimagines everything you can do, too.', '/static/profile_pics/e37931c3e1f9cae8.jpg', '999.00', '3'),
(8, 9, 'MacBook Pro', 'The new MacBook Pro is faster and more powerful than before, yet remarkably thinner and lighter.1 It has the brightest, most colorful Mac notebook display ever. And it introduces the revolutionary Touch Bar—a Multi-Touch– enabled strip of glass built into the keyboard for instant access to what you ', '/static/profile_pics/02e11ed537ba4b72.jpg', '2199.00', '3'),
(9, 9, 'Alienware AW15R3 15\"', 'The new Alienware 15 is for consumers looking for a gaming notebook that prioritizes gaming performance with balanced portability features and specs. Engineered with incredible, all new NVIDIA 10-series graphics, overclocked processors and VR capability to tilt the game in your favor.', '/static/profile_pics/ee245c85aac2fdc2.jpg', '2199.00', '2'),
(10, 3, 'Iphone X', 'iPhone x features an all-screen design with a 5.8-Inch super Retina HD display with HDR and true tone. Face ID lets you unlock and use Apple pay with just a glance. Powered by A11 Bionic, the most powerful and smartest chip ever in a smartphone. Supports augmented reality experiences in games and ap', '/static/profile_pics/fd76e4f56b2b1b88.jpg', '1099.00', '2'),
(11, 7, 'Dell u2415', '24-inch WUXGA Monitor (1920x1200) at 60Hz, 16:10 Aspect Ratio. HDMI, Mini DP, DP, Audio line out, USB 3.0 with USB 3.0 Upstream Port. Temperature Range Operating:0° to 40°C (32° to 104°F)', '/static/profile_pics/5c26e387a980ce3d.jpg', '219.00', '4'),
(13, 4, 'Sonos Play:3', 'Wirelessly stream your entire music library, favorite music services, and thousands of radio stations to any room. Place the SONOS PLAY:3 Wireless Hi-Fi System vertically or horizontally, mount it on a wall or hide on a shelf. Set up simply, and expand until every room in your home is packed with mu', '/static/profile_pics/a593ec0bca13fe76.jpg', '599.00', '2'),
(14, 4, 'Bose SoundTouch 10 ', 'The SoundTouch 10 wireless speaker makes it easy to stream the music you love. It fits just about anywhere (it’s the perfect companion for bedrooms and dorm rooms) and delivers full, rich sound that belies its size. It works with your home Wi-Fi or Bluetooth devices to stream millions of songs from ', '/static/profile_pics/311a27d63b481dfe.jpg', '169.00', '3'),
(15, 3, 'Huawei P20', 'The Huawei P20 Pro isn’t one of those underwhelming phones that get churned out annually with a negligible upgrade – this device is something special. Super-stylish and packed with features, this flagship smartphone has been created with an OLED screen, a bezel-less design and a glass back, while th', '/static/profile_pics/594a0f06458306de.jpg', '716.00', '12'),
(16, 7, 'LG 38UC99-W', 'The LG 38UC99 UltraWide 21:9 curved monitor is the ultimate large screen monitor for work and for play. The graceful curve of the he world\'s first 38-inch curved IPS monitor helps create an immersive viewing experience. Combine the elegant design with the 3840 x 1600 UltraWide Quad Plus definition (', '/static/profile_pics/eaef83a15761c105.jpg', '899.00', '5');

-- --------------------------------------------------------

--
-- Table structure for table `role`
--

CREATE TABLE `role` (
  `roleID` mediumint(9) NOT NULL,
  `roleName` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `role`
--

INSERT INTO `role` (`roleID`, `roleName`) VALUES
(1, 'user'),
(2, 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `status`
--

CREATE TABLE `status` (
  `statusID` mediumint(9) NOT NULL,
  `statusName` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `status`
--

INSERT INTO `status` (`statusID`, `statusName`) VALUES
(1, 'pending'),
(2, 'checkout'),
(3, 'canceled');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `userID` mediumint(9) NOT NULL,
  `username` varchar(25) NOT NULL,
  `passwords` longtext NOT NULL,
  `roleID` mediumint(9) NOT NULL,
  `TimeStamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`userID`, `username`, `passwords`, `roleID`, `TimeStamp`) VALUES
(1, 'user1', '$2b$12$dgWU4ISskRSAWUFaUPeTue/KvaqPOOOTHh0X/KSjgstICc2VZBD4G', 1, '2018-12-01 16:04:07'),
(2, 'user2', '$2b$12$dzL12Xir9/bC1mQ8wU0us.niVTjzclO.ylcXJEYCMnnnLkN7HH71K', 1, '2018-12-01 16:04:20'),
(3, 'user3', '$2b$12$n3XK6ixDBQ43RmjAuwbUV.zXV4TCHdVjPystI/FofKVL7pPv2api2', 1, '2018-12-01 16:04:29'),
(4, 'user4', '$2b$12$U.SBdBngb5jjoqzWDk5t0.BHDvVZvyc4N3S9eO8JhGYpCSzL23S66', 1, '2018-12-01 16:04:39'),
(5, 'admin', '$2b$12$hcXrS/A7APD7FHQfZKKZweTx50x1mfH7FxQQRnAsozs8cbqNiTQdu', 2, '2018-12-01 16:05:09'),
(6, 'user6', '$2b$12$4uEyH6/rhsJxrS.GgQQ9ZOf9n911IeLRSwUIJNS8yggZZ.RFrGIS.', 1, '2018-12-04 23:40:10'),
(7, 'user', '$2b$12$pa8UcgP5R/YQA9ahLHthueRVycH15cYTL6Rugr6QjuUQQ/jxGHrcy', 1, '2018-12-13 00:57:51');

-- --------------------------------------------------------

--
-- Table structure for table `user_info`
--

CREATE TABLE `user_info` (
  `infoID` mediumint(9) NOT NULL,
  `userID` mediumint(9) NOT NULL,
  `nickname` varchar(50) NOT NULL,
  `fullname` varchar(50) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `address` varchar(30) NOT NULL,
  `city` varchar(20) NOT NULL,
  `state` char(2) NOT NULL,
  `zipCode` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user_info`
--

INSERT INTO `user_info` (`infoID`, `userID`, `nickname`, `fullname`, `phone`, `address`, `city`, `state`, `zipCode`) VALUES
(1, 1, '', 'Luu Dinh Van', '7085068356', '7800 Nashville Ave', 'Burbank', 'IL', '60459'),
(2, 1, '', 'Luu Van', '7085068356', '9516 South Kolin Ave', 'Oak Lawn', 'IL', '60652');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`categoryID`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`orderID`),
  ADD KEY `orders_FK1` (`userID`),
  ADD KEY `orders_FK2` (`statusID`);

--
-- Indexes for table `orders_detail`
--
ALTER TABLE `orders_detail`
  ADD KEY `ordersDetail_FK1` (`orderID`),
  ADD KEY `ordersDetail_FK2` (`productID`);

--
-- Indexes for table `payment`
--
ALTER TABLE `payment`
  ADD PRIMARY KEY (`paymentID`),
  ADD KEY `payment_FK1` (`orderID`),
  ADD KEY `payment_FK2` (`userID`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`productID`),
  ADD KEY `product_FK1` (`categoryID`);

--
-- Indexes for table `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`roleID`);

--
-- Indexes for table `status`
--
ALTER TABLE `status`
  ADD PRIMARY KEY (`statusID`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`userID`),
  ADD KEY `users_FK1` (`roleID`);

--
-- Indexes for table `user_info`
--
ALTER TABLE `user_info`
  ADD PRIMARY KEY (`infoID`),
  ADD KEY `BelongTo_FK1` (`userID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `categoryID` mediumint(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `orderID` mediumint(9) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `payment`
--
ALTER TABLE `payment`
  MODIFY `paymentID` mediumint(9) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `productID` mediumint(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `role`
--
ALTER TABLE `role`
  MODIFY `roleID` mediumint(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `status`
--
ALTER TABLE `status`
  MODIFY `statusID` mediumint(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `userID` mediumint(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `user_info`
--
ALTER TABLE `user_info`
  MODIFY `infoID` mediumint(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_FK1` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `orders_FK2` FOREIGN KEY (`statusID`) REFERENCES `status` (`statusID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `orders_detail`
--
ALTER TABLE `orders_detail`
  ADD CONSTRAINT `ordersDetail_FK1` FOREIGN KEY (`orderID`) REFERENCES `orders` (`orderID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ordersDetail_FK2` FOREIGN KEY (`productID`) REFERENCES `product` (`productID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `payment`
--
ALTER TABLE `payment`
  ADD CONSTRAINT `payment_FK1` FOREIGN KEY (`orderID`) REFERENCES `orders` (`orderID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `payment_FK2` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `product`
--
ALTER TABLE `product`
  ADD CONSTRAINT `product_FK1` FOREIGN KEY (`categoryID`) REFERENCES `category` (`categoryID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_FK1` FOREIGN KEY (`roleID`) REFERENCES `role` (`roleID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `user_info`
--
ALTER TABLE `user_info`
  ADD CONSTRAINT `BelongTo_FK1` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
