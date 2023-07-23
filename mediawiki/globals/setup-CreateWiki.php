<?php

use MediaWiki\MediaWikiServices;
use Wikimedia\Rdbms\Database;

$wgWikimediaJenkinsCI = true;

define( 'CW_DB', 'wikidb' );

require_once "$IP/extensions/CreateWiki/includes/WikiInitialise.php";
$wi = new WikiInitialise();

$wi->setVariables(
	"$IP/cache",
	[
		''
	],
	[
		'127.0.0.1' => ''
	]
);

$wi->config->settings += [
	'cwClosed' => [
		'default' => false,
	],
	'cwInactive' => [
		'default' => false,
	],
	'cwPrivate' => [
		'default' => false,
	],
	'cwExperimental' => [
		'default' => false,
	],
];

$wgCreateWikiGlobalWiki = 'wikidb';
$wgCreateWikiDatabase = 'wikidb';
$wgCreateWikiCacheDirectory = "$IP/cache";

$wgManageWikiDatabase = 'wikidb';

$wgHooks['MediaWikiServices'][] = 'insertWiki';

function insertWiki( MediaWikiServices $services ) {
	$db = wfInitDBConnection();

	$db->begin();
	$db->query( 'SOURCE ' . __DIR__ . '/../sql/add-wiki.sql;' );
	$db->commit();
}

function wfInitDBConnection() {
	return Database::factory( 'mysql', [
		'host' => $GLOBALS['wgDBserver'],
		'user' => 'root',
	] );
}

$wi->readCache();
$wi->config->extractAllGlobals( $wi->dbname );
$wgConf = $wi->config;

?>
