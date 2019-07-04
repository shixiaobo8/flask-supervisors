-- MySQL dump 10.13  Distrib 5.7.26, for Linux (x86_64)
--
-- Host: localhost    Database: xj_omsa
-- ------------------------------------------------------
-- Server version	5.7.26-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('52fbd425208c');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services_developers`
--

DROP TABLE IF EXISTS `services_developers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services_developers` (
  `service_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  KEY `service_id` (`service_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `services_developers_ibfk_1` FOREIGN KEY (`service_id`) REFERENCES `sv_services` (`id`),
  CONSTRAINT `services_developers_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `sv_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services_developers`
--

LOCK TABLES `services_developers` WRITE;
/*!40000 ALTER TABLE `services_developers` DISABLE KEYS */;
INSERT INTO `services_developers` VALUES (4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(11,1),(12,1),(13,1),(14,1),(15,1);
/*!40000 ALTER TABLE `services_developers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services_hosts`
--

DROP TABLE IF EXISTS `services_hosts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `services_hosts` (
  `service_id` int(11) NOT NULL,
  `host_id` int(11) NOT NULL,
  PRIMARY KEY (`service_id`,`host_id`),
  KEY `host_id` (`host_id`),
  CONSTRAINT `services_hosts_ibfk_1` FOREIGN KEY (`host_id`) REFERENCES `sv_hosts` (`id`),
  CONSTRAINT `services_hosts_ibfk_2` FOREIGN KEY (`service_id`) REFERENCES `sv_services` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services_hosts`
--

LOCK TABLES `services_hosts` WRITE;
/*!40000 ALTER TABLE `services_hosts` DISABLE KEYS */;
INSERT INTO `services_hosts` VALUES (4,30),(4,31),(5,32),(5,33),(6,34),(6,35),(7,36),(8,36),(7,37),(8,37),(9,38),(9,39),(10,40),(10,41),(11,42),(11,43),(12,44),(12,45),(13,46),(13,47),(14,48),(15,48),(14,49),(15,49);
/*!40000 ALTER TABLE `services_hosts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sv_hosts`
--

DROP TABLE IF EXISTS `sv_hosts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sv_hosts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(120) COLLATE utf8_unicode_ci NOT NULL COMMENT '主机名称',
  `sv_port` tinyint(1) DEFAULT NULL COMMENT '主机ssh端口',
  `is_del` tinyint(1) DEFAULT NULL COMMENT '逻辑删除',
  `sv_node_id` int(11) DEFAULT NULL COMMENT '关联节点,多对一',
  `host_inner_ip` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '主机内网ip',
  `host_public_ip` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '主机公网ip',
  `ali_instance_id` varchar(120) COLLATE utf8_unicode_ci NOT NULL COMMENT '阿里云实例id',
  `host_info` varchar(120) COLLATE utf8_unicode_ci NOT NULL COMMENT '主机信息',
  PRIMARY KEY (`id`),
  UNIQUE KEY `hostname` (`hostname`),
  UNIQUE KEY `ali_instance_id` (`ali_instance_id`),
  KEY `sv_node_id` (`sv_node_id`),
  KEY `ix_sv_hosts_host_inner_ip` (`host_inner_ip`),
  KEY `ix_sv_hosts_host_public_ip` (`host_public_ip`),
  CONSTRAINT `sv_hosts_ibfk_2` FOREIGN KEY (`sv_node_id`) REFERENCES `sv_nodes` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sv_hosts`
--

LOCK TABLES `sv_hosts` WRITE;
/*!40000 ALTER TABLE `sv_hosts` DISABLE KEYS */;
INSERT INTO `sv_hosts` VALUES (29,'resmgr-dps',22,0,1,'172.19.0.11','','i-wz947i94k3xwcgm8sb4p','CentOS  7.6 64位/4c/4096\nM'),(30,'usercenter002',22,0,1,'172.19.0.9','','i-wz9798ltehzplpqtaokj','CentOS  7.6 64位/4c/4096\nM'),(31,'usercenter001',22,0,1,'172.19.0.10','','i-wz9798ltehzplpqtaoki','CentOS  7.6 64位/4c/4096\nM'),(32,'uss002',22,0,1,'172.19.0.7','','i-wz90p2k5or2bw1beazst','CentOS  7.6 64位/4c/4096\nM'),(33,'uss001',22,0,1,'172.19.0.8','','i-wz90p2k5or2bw1beazss','CentOS  7.6 64位/4c/4096\nM'),(34,'msgcenter001',22,0,1,'172.19.0.6','','i-wz92i73koztp07jjsllr','CentOS  7.6 64位/4c/4096\nM'),(35,'msgcenter002',22,0,1,'172.19.0.5','','i-wz92i73koztp07jjslls','CentOS  7.6 64位/4c/4096\nM'),(36,'mediaproxy-push001',22,0,1,'172.19.0.4','','i-wz9cfujsdt5f8se15qq3','CentOS  7.6 64位/4c/4096\nM'),(37,'mediaproxy-push002',22,0,1,'172.19.0.3','','i-wz9cfujsdt5f8se15qq4','CentOS  7.6 64位/4c/4096\nM'),(38,'buddy001',22,0,1,'172.19.0.2','','i-wz91p5e96ps9kgdknvjs','CentOS  7.6 64位/4c/4096\nM'),(39,'buddy002',22,0,1,'172.19.0.1','','i-wz91p5e96ps9kgdknvjt','CentOS  7.6 64位/4c/4096\nM'),(40,'group001',22,0,1,'172.19.0.251','','i-wz92i73koztp05kiojfv','CentOS  7.6 64位/4c/4096\nM'),(41,'group002',22,0,1,'172.19.0.252','','i-wz92i73koztp05kiojfw','CentOS  7.6 64位/4c/4096\nM'),(42,'regionv2001',22,0,1,'172.19.0.249','','i-wz9hsugal67fdoqs27ve','CentOS  7.6 64位/4c/4096\nM'),(43,'regionv2002',22,0,1,'172.19.0.250','','i-wz9hsugal67fdoqs27vf','CentOS  7.6 64位/4c/4096\nM'),(44,'region002',22,0,1,'172.19.0.247','120.79.175.139','i-wz90f3ft5gqsopan4fuc','CentOS  7.6 64位/4c/8192\nM'),(45,'region001',22,0,1,'172.19.0.248','172.19.0.247','i-wz90f3ft5gqsopan4fub','CentOS  7.6 64位/4c/8192\nM'),(46,'gateway002',22,0,1,'172.19.0.246','39.108.215.36','i-wz93ap2p1nffteau8669','CentOS  7.6 64位/4c/8192\nM'),(47,'gateway001',22,0,1,'172.19.0.245','47.107.76.62','i-wz93ap2p1nffteau8668','CentOS  7.6 64位/4c/8192\nM'),(48,'nav_upload001',22,0,1,'172.19.0.244','47.106.233.71','i-wz9fhdzbks7wosgzqip6','CentOS  7.6 64位/4c/4096\nM'),(49,'nav_upload002',22,0,1,'172.19.0.243','47.106.240.43','i-wz9fhdzbks7wosgzqip7','CentOS  7.6 64位/4c/4096\nM'),(50,'IM-Cache-redis003',22,0,1,'172.19.0.240','47.107.90.78','i-wz92lvtw1kaa4gue48xa','CentOS  7.6 64位/4c/16384\nM'),(51,'IM-Cache-redis002',22,0,1,'172.19.0.242','47.106.177.128','i-wz92lvtw1kaa4gue48x9','CentOS  7.6 64位/4c/16384\nM'),(52,'IM-Cache-redis001',22,0,1,'172.19.0.241','47.106.180.192','i-wz92lvtw1kaa4gue48x8','CentOS  7.6 64位/4c/16384\nM'),(69,'linux-jumpserver',22,0,1,'172.19.0.13','120.76.57.171','i-wz9i1da6brgtva63chah','CentOS  7.6 64位/4c/8192M'),(70,'IM-Storage-mongo003',22,0,1,'172.19.0.239','47.106.148.255','i-wz9cxsilfrh7pgsntkxy','CentOS  7.6 64位/8c/16384\nM'),(71,'IM-Storage-mongo002',22,0,1,'172.19.0.238','47.106.148.171','i-wz9cxsilfrh7pgsntkxx','CentOS  7.6 64位/8c/16384\nM'),(72,'IM-Storage-mongo001',22,0,1,'172.19.0.237','120.79.140.150','i-wz9cxsilfrh7pgsntkxw','CentOS  7.6 64位/8c/16384\nM'),(73,'IM-Storage-mysql1',22,0,1,'172.19.0.236','120.79.198.82','i-wz9eumzz9ehized66k62','CentOS  7.6 64位/4c/8192\nM'),(74,'IM-Stroage-mysql2',22,0,1,'172.19.0.235','120.79.175.139','i-wz9eumzz9ehized66k61','CentOS  7.6 64位/4c/8192\nM'),(75,'resmgr-nginx-php',22,0,1,'172.19.0.12','','i-wz947i94k3xwcgm8sb83','CentOS  7.6 64位/4c/4096\nM'),(76,'mysql1',22,0,2,'172.18.21.62','120.79.85.13','i-wz9gglwrfdrwui0jbwle','CentOS  7.6 64位/2c/8192\nM'),(77,'mysql2',22,0,2,'172.18.21.61','120.79.135.250','i-wz9gglwrfdrwui0jbwlc','CentOS  7.6 64位/2c/8192\nM'),(78,'mongo1',22,0,2,'172.18.21.60','120.79.92.51','i-wz9gglwrfdrwui0jbwlb','CentOS  7.6 64位/2c/8192\nM'),(79,'mongo2',22,0,2,'172.18.21.59','120.79.15.62','i-wz9gglwrfdrwui0jbwld','CentOS  7.6 64位/2c/8192\nM'),(80,'mongo3',22,0,2,'172.18.21.58','120.79.10.163','i-wz9gglwrfdrwui0jbwlf','CentOS  7.6 64位/2c/8192\nM'),(81,'redis1',22,0,2,'172.18.21.45','120.79.23.213','i-wz96lf5qxtmkbqoz5iye','CentOS  7.6 64位/4c/8192\nM'),(82,'redis2',22,0,2,'172.18.21.50','119.23.27.216','i-wz96lf5qxtmkbqoz5iy5','CentOS  7.6 64位/4c/8192\nM'),(83,'redis3',22,0,2,'172.18.21.48','47.106.105.43','i-wz96lf5qxtmkbqoz5iy6','CentOS  7.6 64位/4c/8192\nM'),(84,'nav_buddy_mediaproxy_1',22,0,2,'172.18.21.52','119.23.11.181','i-wz96lf5qxtmkbqoz5iy9','CentOS  7.6 64位/4c/8192\nM'),(85,'nav_buddy_mediaproxy_2',22,0,2,'172.18.21.55','120.79.246.15','i-wz96lf5qxtmkbqoz5iyd','CentOS  7.6 64位/4c/8192\nM'),(86,'region_upload_1',22,0,2,'172.18.21.47','120.77.146.7','i-wz96lf5qxtmkbqoz5iyb','CentOS  7.6 64位/4c/8192\nM'),(87,'region_upload_2',22,0,2,'172.18.21.54','120.79.245.190','i-wz96lf5qxtmkbqoz5iy8','CentOS  7.6 64位/4c/8192\nM'),(88,'region_gateway_group_1',22,0,2,'172.18.21.53','120.78.90.242','i-wz96lf5qxtmkbqoz5iyc','CentOS  7.6 64位/4c/8192\nM'),(89,'region_gateway_group_2',22,0,2,'172.18.21.57','39.108.175.129','i-wz96lf5qxtmkbqoz5iy7','CentOS  7.6 64位/4c/8192\nM'),(90,'msgcenter_uss_1',22,0,2,'172.18.21.46','47.106.107.72','i-wz96lf5qxtmkbqoz5iy3','CentOS  7.6 64位/4c/8192\nM'),(91,'msgcenter_uss_2',22,0,2,'172.18.21.51','120.78.151.245','i-wz96lf5qxtmkbqoz5iy1','CentOS  7.6 64位/4c/8192\nM'),(92,'regionv2_usercenter_1',22,0,2,'172.18.21.44','119.23.12.9','i-wz96lf5qxtmkbqoz5iy4','CentOS  7.6 64位/4c/8192\nM'),(93,'regionv2_usercenter_2',22,0,2,'172.18.21.49','112.74.41.124','i-wz96lf5qxtmkbqoz5iya','CentOS  7.6 64位/4c/8192\nM'),(94,'resmgr_nginx_php_push_jumpserver',22,0,2,'172.18.21.56','120.79.10.234','i-wz96lf5qxtmkbqoz5iy2','CentOS  7.6 64位/4c/8192\nM'),(95,'test-grafana-prometheus',22,0,2,'172.18.21.63','','i-wz92v3pf7ycf2r66g61a','CentOS  7.6 64位/4c/8192M');
/*!40000 ALTER TABLE `sv_hosts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sv_navs`
--

DROP TABLE IF EXISTS `sv_navs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sv_navs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `navTitle` varchar(120) COLLATE utf8_unicode_ci NOT NULL COMMENT '一级导航栏标题',
  `navUrl` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '一级导航栏url',
  `navType` tinyint(1) DEFAULT NULL COMMENT '导航栏分类,默认为后台导航栏',
  `is_del` tinyint(1) DEFAULT NULL COMMENT '逻辑删除',
  `role_id` int(11) DEFAULT NULL COMMENT '关联角色,多对一',
  PRIMARY KEY (`id`),
  UNIQUE KEY `navTitle` (`navTitle`),
  KEY `role_id` (`role_id`),
  KEY `ix_sv_navs_navUrl` (`navUrl`),
  CONSTRAINT `sv_navs_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `sv_roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sv_navs`
--

LOCK TABLES `sv_navs` WRITE;
/*!40000 ALTER TABLE `sv_navs` DISABLE KEYS */;
INSERT INTO `sv_navs` VALUES (7,'服务器管理','',0,0,1),(8,'线上监控','',0,0,1),(9,'资源管理','',0,0,1);
/*!40000 ALTER TABLE `sv_navs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sv_nodes`
--

DROP TABLE IF EXISTS `sv_nodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sv_nodes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nodeName` varchar(120) COLLATE utf8_unicode_ci NOT NULL COMMENT '节点名称',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sv_nodes_nodeName` (`nodeName`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sv_nodes`
--

LOCK TABLES `sv_nodes` WRITE;
/*!40000 ALTER TABLE `sv_nodes` DISABLE KEYS */;
INSERT INTO `sv_nodes` VALUES (1,'正式环境'),(2,'测试环境');
/*!40000 ALTER TABLE `sv_nodes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sv_roles`
--

DROP TABLE IF EXISTS `sv_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sv_roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `roleName` varchar(120) COLLATE utf8_unicode_ci NOT NULL COMMENT '角色名称',
  `sv_userGroup_Id` int(11) DEFAULT NULL COMMENT '用户组权限外键',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sv_roles_roleName` (`roleName`),
  KEY `sv_userGroup_Id` (`sv_userGroup_Id`),
  CONSTRAINT `sv_roles_ibfk_1` FOREIGN KEY (`sv_userGroup_Id`) REFERENCES `sv_userGroups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sv_roles`
--

LOCK TABLES `sv_roles` WRITE;
/*!40000 ALTER TABLE `sv_roles` DISABLE KEYS */;
INSERT INTO `sv_roles` VALUES (1,'普通用户',NULL),(2,'管理员',NULL),(3,'其他用户',NULL),(4,'特殊用户',NULL);
/*!40000 ALTER TABLE `sv_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sv_services`
--

DROP TABLE IF EXISTS `sv_services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sv_services` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `service_name` varchar(120) COLLATE utf8_unicode_ci NOT NULL COMMENT '服务名称',
  `service_start_cmd` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '服务启动命令',
  `is_del` tinyint(1) DEFAULT NULL COMMENT '逻辑删除',
  `service_deploy_dir` varchar(120) COLLATE utf8_unicode_ci NOT NULL COMMENT '服务部署路径',
  `service_detail` varchar(120) COLLATE utf8_unicode_ci NOT NULL COMMENT '服务详情描述',
  `service_ports` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '服务端口号',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sv_services_service_name` (`service_name`),
  KEY `ix_sv_services_service_start_cmd` (`service_start_cmd`),
  KEY `ix_sv_services_service_deploy_dir` (`service_deploy_dir`),
  KEY `ix_sv_services_service_detail` (`service_detail`),
  KEY `ix_sv_services_service_ports` (`service_ports`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sv_services`
--

LOCK TABLES `sv_services` WRITE;
/*!40000 ALTER TABLE `sv_services` DISABLE KEYS */;
INSERT INTO `sv_services` VALUES (4,'usercenter','/im/usercenter/tools/op/start.sh',0,'','用户中心服务','51007'),(5,'uss','/im/uss/tools/op/start.sh',0,'','用户会话服务','51009'),(6,'msgcenter','/im/msgcenter/tools/op/start.sh',0,'','消息中心服务','51004'),(7,'mediaproxy','/im/mediaproxy/tools/op/start.sh',0,'','媒体网关服务','51013'),(8,'push','/im/push/tools/op/start.sh',0,'','推送服务','51005'),(9,'buddysys','/im/buddysys/tools/op/start.sh',0,'','关系链服务','51003'),(10,'group_service','/im/group_service/tools/op/start.sh',0,'','群聊服务','51002'),(11,'region_serverv2','/im/region_serverv2/tools/op/start.sh',0,'','单聊以及附属服务','51016'),(12,'region_server','/im/region_server/tools/op/start.sh',0,'','长连接网关服务','51001'),(13,'region_gateway','/im/region_gateway/tools/op/start.sh',0,'','短连接网关服务','51020'),(14,'upload_server','/im/upload_server/tools/op/start.sh',0,'','上报服务','58512,51012'),(15,'navigate_server','/im/navigate_server/tools/op/start.sh',0,'','导航服务','51008');
/*!40000 ALTER TABLE `sv_services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sv_subnavs`
--

DROP TABLE IF EXISTS `sv_subnavs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sv_subnavs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(120) COLLATE utf8_unicode_ci NOT NULL COMMENT '二级导航栏标题',
  `nav_url` varchar(200) COLLATE utf8_unicode_ci NOT NULL COMMENT '二级导航栏url',
  `nav_Id` int(11) DEFAULT NULL COMMENT '关联一级导航栏,多对一',
  `is_del` tinyint(1) DEFAULT NULL COMMENT '逻辑删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_sv_subnavs_nav_url` (`nav_url`),
  UNIQUE KEY `ix_sv_subnavs_title` (`title`),
  KEY `nav_Id` (`nav_Id`),
  CONSTRAINT `sv_subnavs_ibfk_1` FOREIGN KEY (`nav_Id`) REFERENCES `sv_navs` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sv_subnavs`
--

LOCK TABLES `sv_subnavs` WRITE;
/*!40000 ALTER TABLE `sv_subnavs` DISABLE KEYS */;
INSERT INTO `sv_subnavs` VALUES (1,'发布管理','/server/ci-cd',7,0),(2,'线上业务管理','/server/serviceList',7,0),(3,'仪表盘状态','/service/dashborad2',8,0),(4,'服务器列表','/server/serverList',7,0),(5,' ansible主机管理','/server/ansible/manage',7,0),(6,'supervisor集群监控','/monitor/supervisors/status',8,0),(7,'app版本管理','/server/appVersion.html',7,0);
/*!40000 ALTER TABLE `sv_subnavs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sv_userGroups`
--

DROP TABLE IF EXISTS `sv_userGroups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sv_userGroups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sv_userGroups`
--

LOCK TABLES `sv_userGroups` WRITE;
/*!40000 ALTER TABLE `sv_userGroups` DISABLE KEYS */;
/*!40000 ALTER TABLE `sv_userGroups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sv_users`
--

DROP TABLE IF EXISTS `sv_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sv_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(80) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '用户名',
  `avatar` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '头像',
  `email` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '邮箱',
  `weixin_name` varchar(120) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '微信昵称',
  `phone` varchar(11) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '手机号',
  `is_del` tinyint(1) DEFAULT NULL COMMENT '逻辑删除',
  `join_date` datetime DEFAULT NULL,
  `last_modify` datetime DEFAULT NULL,
  `password_hash` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `userGroup_Id` int(11) DEFAULT NULL COMMENT '关联一级用户组,多对一',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `weixin_name` (`weixin_name`),
  KEY `userGroup_Id` (`userGroup_Id`),
  CONSTRAINT `sv_users_ibfk_1` FOREIGN KEY (`userGroup_Id`) REFERENCES `sv_userGroups` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sv_users`
--

LOCK TABLES `sv_users` WRITE;
/*!40000 ALTER TABLE `sv_users` DISABLE KEYS */;
INSERT INTO `sv_users` VALUES (1,'shiyiguo','img\\users\\shiyiguo\\292-11012511135849.jpg','shixiaobo8@163.com','shiyiguo001','13148744969',0,'2019-06-15 18:20:56','2019-06-27 10:54:37','123456',NULL);
/*!40000 ALTER TABLE `sv_users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-07-04 13:25:32
