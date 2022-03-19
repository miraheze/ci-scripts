<?php

$wgHooks['MediaWikiServices'][] = 'fixCache';

function fixCache() {
	global $wgMainCacheType;

	$wgMainCacheType = CACHE_NONE;
}

?>
