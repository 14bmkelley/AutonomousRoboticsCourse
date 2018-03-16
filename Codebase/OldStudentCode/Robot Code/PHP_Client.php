#!/usr/bin/php

<?php
/*************************************************************************
* Name: php_test.php
* Desc: Opens port 334411 on localhost and waits for connections
* Credit: Source adapted from python server on http://stackoverflow.com/questions/25787944/python-socket-server-to-php-client-socket
*       Changes made to xmit data, then echo the response
* Intent: test pyserver.py. Act as a template for setting up sockets and interfacing
*         with pyserver
* Author: adanowit@calpoly.edu
*************************************************************************/

error_reporting(E_ALL);

//  Allow the script to hang around waiting for connections.
set_time_limit(0);

// Turn on implicit output flushing so we see what we're getting as it comes in.
ob_implicit_flush();

// Set timeout in seconds
$timeout = 3;  

// Create a TCP/IP client socket.
$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);

if ($socket === false) 
{
	$result2 = "Error: socket_create() failed: reason: " .socket_strerror(socket_last_error()). "\n";
}

// Server data
$host = '127.0.0.1';
$port = 334411;

$error = NULL;
$attempts = 0;
$timeout *= 1000;  // adjust because we sleeping in 1 millisecond increments
$connected = FALSE;

while (!($connected = socket_connect($socket, $host, $port)) && ($attempts++ < $timeout)) 
{
	$error = socket_last_error();
        if ($error != SOCKET_EINPROGRESS && $error != SOCKET_EALREADY) 
        {
            echo "Error Connecting Socket: ".socket_strerror($error) . "\n";
            socket_close($socket);
            return NULL;
        }
        usleep(1000);
}

if (!$connected) 
{
	echo "Error Connecting Socket: Connect Timed Out After " . $timeout/1000 . " seconds. ".socket_strerror(socket_last_error()) . "\n";
        socket_close($socket);
        return NULL;
}


echo '<html>
	<head>
		<title>
			Reading IMU and GPS Sensors
		</title>
	</head>
	<body>
		<form action="" method="get">
		
			<input  type="submit" name="Get_IMU" value="Get IMU Data">
			<input  type="submit" name="Get_GPS" value="Get GPS Data">

		</form>
	</body>
</html>';


if(isset($_GET['Get_IMU']))	//IMU Button
{
	
	//Pack an array with the sequence of commands we want to issue

		 $output= array(
				'cmd1' => array('type' => 'IMU', 'cmd' => "EULER"),
				'cmd2' => array('type' => 'IMU', 'cmd' => 'CALIB'));


	//Issue each command and print the response
	foreach ($output as $cmd => $cmd_string){
		$json_out = json_encode($cmd_string);
		echo $cmd_string . "\n";
		socket_write($socket, $json_out, strlen ($json_out)) or die("Could not write output\n");

		// Get the response from the server - our current telemetry
		$resultLength = socket_read($socket, 1024) or die("Could not read server response\n");

		$result4 = $resultLength;

		echo $result4."\n";
		}
}

if(isset($_GET['Get_GPS']))	//GPS Button
{
		
	//Pack an array with the sequence of commands we want to issue

		 $output= array(
				'cmd1' => array('type' => 'GPS', 'cmd' => "LAT"),
				'cmd2' => array('type' => 'GPS', 'cmd' => 'LONG'));


	//Issue each command and print the response
	foreach ($output as $cmd => $cmd_string){
		$json_out = json_encode($cmd_string);
		//echo $cmd_string . "\n";
		socket_write($socket, $json_out, strlen ($json_out)) or die("Could not write output\n");

		// Get the response from the server - our current telemetry
		$resultLength = socket_read($socket, 1024) or die("Could not read server response\n");

		$result4 = json_decode($resultLength, true);

		echo $result4['resp'] ."\n";
		}
}



/*	//Tell the server that we're done
	$end_cmd = json_encode("end_session");
	socket_write($socket, $end_cmd, strlen($end_cmd)) ;

	// close the socket
	socket_close($socket);
	
	*/	//Dont end session or close socket since we need to keep readin sensors. 
	
?>
