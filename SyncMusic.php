<?php
	$locale='en_US.UTF-8';  
	setlocale(LC_ALL,$locale);  
	putenv('LC_ALL='.$locale);
	syncMusic();
	function syncMusic()
	{
		$cmd = "python3 ./ShareNetEaseMusic.py";
		//$cmd = "python3 /var/www/html/Norcy.github.io/isee.py ".$objectName." ".$type." ".$year." ".$mouth." ".$date." 2>&1";
		var_dump(shell_exec($cmd));
	    	//shell_exec($cmd);
	}
?>