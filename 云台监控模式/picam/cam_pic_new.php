<?php

define('BASE_DIR', dirname(__FILE__));
require_once(BASE_DIR.'/config.php');

if (isset($_GET["pDelay"]))
   {
      $preview_delay = $_GET["pDelay"];
   } else {
      $preview_delay = 10000;
   }

//writeLog("mjpeg stream with $preview_delay delay");

// 用于分离多部分
$boundary = "PIderman";

// 从标准头文件开始
header ("Content-type: multipart/x-mixed-replace; boundary=$boundary");
header ("Cache-Control: no-cache");
header ("Pragma: no-cache");
header ("Connection: close");

ob_flush();		// 推出我们已经拥有的内容(尽快将标题发送到浏览器)

set_time_limit(0); // 设置此参数使PHP在长数据流中不会超时


while(true) 
{	
	ob_start();
	
	echo "--$boundary\r\n";
	echo "Content-type: image/jpeg\r\n";
	
	$fileContents = file_get_contents("/dev/shm/mjpeg/cam.jpg");
	$fileLength = strlen($fileContents);
	
	echo "Content-Length:" . $fileLength . "\r\n";
	echo "\r\n";
	
	echo $fileContents;
	
	echo "\r\n";
	ob_end_flush();
	
	usleep($preview_delay);
}
