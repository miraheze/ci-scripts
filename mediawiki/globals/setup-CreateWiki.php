<?php

use Miraheze\CreateWiki\WikiInitialize;

$wgWikimediaJenkinsCI = true;

if ( file_exists( "$IP/extensions/CreateWiki/includes/WikiInitialize.php" ) ) {
	define( 'CW_DB', 'wikidb' );

	require_once "$IP/extensions/CreateWiki/includes/WikiInitialize.php";

	$wgHooks['MediaWikiServices'][] = 'wfLoadConfiguration';
}

function wfLoadConfiguration() {
	global $wgCreateWikiCacheDirectory, $wgConf, $wgWikiInitialize,
		$wgVirtualDomainsMapping;

	$wgVirtualDomainsMapping['virtual-createwiki'] = [ 'db' => 'wikidb' ];
	$wgVirtualDomainsMapping['virtual-createwiki-central'] = [ 'db' => 'wikidb' ];

	$wgCreateWikiCacheDirectory = MW_INSTALL_PATH . '/cache';

	$wgWikiInitialize = new WikiInitialize();

	$wgWikiInitialize->setVariables(
		MW_INSTALL_PATH . '/cache',
		[
			''
		],
		[
			'127.0.0.1' => ''
		]
	);

	$wgWikiInitialize->config->settings += [
		'cwClosed' => [
			'default' => false,
		],
		'cwInactive' => [
			'default' => false,
		],
		'cwPrivate' => [
			'default' => false,
		],
	];

	$wgWikiInitialize->readCache();
	$wgWikiInitialize->config->extractAllGlobals( $wgWikiInitialize->dbname );
	$wgConf = $wgWikiInitialize->config;
}

?>
