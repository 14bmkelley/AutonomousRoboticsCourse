<?php
error_reporting(E_ALL);

//  Allow the script to hang around waiting for connections.
set_time_limit(0);

// Turn on implicit output flushing so we see what we're getting as it comes in.
ob_implicit_flush();

// Set timeout in seconds
$timeout = 3;

gettelemetry('yourrobot@duckdns.org');

function gettelemetry($host)
{
	// Create a TCP/IP client socket.
	$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);

	if ($socket === false) 
	{
		$result2 = "Error: socket_create() failed: reason: " .socket_strerror(socket_last_error()). "\n";
	}

	// Server data
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
 	           return array("lat"=>"0","lon"=>"0","heading"=>"0","online"=>"0");
	        }
	        usleep(1000);
	}

	if (!$connected) 
	{
		echo "Error Connecting Socket: Connect Timed Out After " . $timeout/1000 . " seconds. ".socket_strerror(socket_last_error()) . "\n";
 	       socket_close($socket);
	        return array("lat"=>"0","lon"=>"0","heading"=>"0","online"=>"0");
	}

	// Get latitude
	$json_out = json_encode(array('type' => 'game', 'cmd' => 'sendlat', 'arg'=>''));
	socket_write($socket, $json_out, strlen ($json_out)) or die("Could not write output\n");
	// Get the response from the server - our current telemetry
	$lat = socket_read($socket, 1024) or die("Could not read server response\n");
	echo $lat."\n";

	// Get longitude
	$json_out = json_encode(array('type' => 'game', 'cmd' => 'sendlon', 'arg'=>''));
	socket_write($socket, $json_out, strlen ($json_out)) or die("Could not write output\n");
	// Get the response from the server - our current telemetry
	$lat = socket_read($socket, 1024) or die("Could not read server response\n");
	echo $lon."\n";

	// Get heading
	$json_out = json_encode(array('type' => 'game', 'cmd' => 'sendheading', 'arg'=>''));
	socket_write($socket, $json_out, strlen ($json_out)) or die("Could not write output\n");
	// Get the response from the server - our current telemetry
	$heading = socket_read($socket, 1024) or die("Could not read server response\n");
	echo $heading."\n";


	//Tell the server that we're done
	$end_cmd = json_encode("end_session");
	socket_write($socket, $end_cmd, strlen($end_cmd)) ;

	// close the socket
	socket_close($socket);
	
	return array("lat"=>$lat,"lon"=>$lon,"heading"=>$heading,"online"=>"1");
}

function haversineGreatCircleDistance($latitudeFrom, $longitudeFrom, $latitudeTo, $longitudeTo, $earthRadius = 6371000)
{
  // convert from degrees to radians
  $latFrom = deg2rad($latitudeFrom);
  $lonFrom = deg2rad($longitudeFrom);
  $latTo = deg2rad($latitudeTo);
  $lonTo = deg2rad($longitudeTo);

  $latDelta = $latTo - $latFrom;
  $lonDelta = $lonTo - $lonFrom;

  $angle = 2 * asin(sqrt(pow(sin($latDelta / 2), 2) +
    cos($latFrom) * cos($latTo) * pow(sin($lonDelta / 2), 2)));
  return $angle * $earthRadius;
}


?>
