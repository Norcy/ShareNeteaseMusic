<?php
	$locale='en_US.UTF-8';  
	setlocale(LC_ALL,$locale);  
	putenv('LC_ALL='.$locale);
	syncMusic();
	function syncMusic()
	{
		$cmd0 = "killall node";
		//var_dump(shell_exec($cmd0));
		$cmd1 = "node ../NeteaseCloudMusicApi/app.js";
		var_dump(shell_exec($cmd1));
		$cmd2 = "python3 /var/www/html/ShareNeteaseMusic/ShareNetEaseMusic.py";
		//$cmd = "python3 /var/www/html/Norcy.github.io/isee.py ".$objectName." ".$type." ".$year." ".$mouth." ".$date." 2>&1";
		var_dump(shell_exec($cmd2));
		//var_dump(shell_exec($cmd0));
	    	//shell_exec($cmd);
	}
?>
