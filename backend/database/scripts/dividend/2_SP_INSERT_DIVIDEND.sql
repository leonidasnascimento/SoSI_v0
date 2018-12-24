CREATE TABLE `dividend` (
  `CODE` varchar(10) NOT NULL,
  `COMPANY` varchar(255) NOT NULL,
  `SECTOR` varchar(255) NOT NULL,
  `SECOND_SECTOR` varchar(255) DEFAULT NULL,
  `STOCK_PRICE` decimal(20,6) NOT NULL,
  `STOCK_TYPE` varchar(2) NOT NULL,
  `VALUATION` decimal(20,6) NOT NULL,
  `STOCK_AVAILABLE_AMOUNT` decimal(20,6) NOT NULL,
  `AVG_21_NEGOCIATION` decimal(20,6) NOT NULL,
  `DIVIDEND_PERIOD` decimal(2,0) NOT NULL,
  `DIVIDEND_LAST_PRICE` decimal(20,6) NOT NULL,
  `DIVIDEND_TOTAL_VALUE_SHARED` decimal(20,6) NOT NULL,
  `NET_PROFIT` decimal(20,6) NOT NULL,
  `DIVIDEND_YELD` decimal(7,6) NOT NULL,
  `AVG_PAYOUT_12_MONTHS` decimal(7,6) NOT NULL,
  `AVG_PAYOUT_5_YEARS` decimal(7,6) NOT NULL,
  `MAJOR_SHARE_HOLDER` varchar(255) NOT NULL,
  PRIMARY KEY (`CODE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
