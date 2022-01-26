CREATE TABLE `metrics` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `collect_tms` varchar(50) NOT NULL,
  `cache_item_count` bigint NOT NULL,
  `cache_item_size` varchar(20) NOT NULL,
  `items_bytype` varchar(500) NOT NULL,
  `hit_bytes` bigint NOT NULL,
  `hit_requests` bigint NOT NULL,
  `miss_bytes` bigint NOT NULL,
  `miss_requests` bigint NOT NULL,
  `total_bytes` bigint NOT NULL,
  `total_requests` bigint NOT NULL
) ENGINE='InnoDB';