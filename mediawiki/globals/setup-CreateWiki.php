<?php

use MediaWiki\MediaWikiServices;
use Miraheze\CreateWiki\WikiInitialize;
use Wikimedia\Rdbms\DBQueryError;

$wgWikimediaJenkinsCI = true;

if ( file_exists( "$IP/extensions/CreateWiki/includes/WikiInitialize.php" ) ) {
	define( 'CW_DB', 'wikidb' );

	require_once "$IP/extensions/CreateWiki/includes/WikiInitialize.php";

	$wgHooks['MediaWikiServices'][] = 'insertWiki';
}

function insertWiki( MediaWikiServices $services ) {
	wfLoadConfiguration();
	try {
		if ( getenv( 'WIKI_CREATION_SQL_EXECUTED' ) ) {
			return;
		}

		$db = wfInitDBConnection();

		$db->selectDomain( 'wikidb' );
		$db->newInsertQueryBuilder()
			->insertInto( 'cw_wikis' )
			->ignore()
			->row( [
				'wiki_dbname' => 'wikidb',
				'wiki_dbcluster' => 'c1',
				'wiki_sitename' => 'TestWiki',
				'wiki_language' => 'en',
				'wiki_private' => 0,
				'wiki_creation' => $db->timestamp(),
				'wiki_category' => 'uncategorised',
				'wiki_closed' => 0,
				'wiki_deleted' => 0,
				'wiki_locked' => 0,
				'wiki_inactive' => 0,
				'wiki_inactive_exempt' => 0,
				'wiki_url' => 'http://127.0.0.1:9412',
			] )
			->caller( __METHOD__ )
			->execute();

		putenv( 'WIKI_CREATION_SQL_EXECUTED=true' );
	} catch ( DBQueryError $e ) {
		return;
	}
}

function wfLoadConfiguration() {
	global $wgCreateWikiGlobalWiki, $wgCreateWikiDatabase,
		$wgCreateWikiCacheDirectory, $wgConf;

	$wgCreateWikiGlobalWiki = 'wikidb';
	$wgCreateWikiDatabase = 'wikidb';
	$wgCreateWikiCacheDirectory = MW_INSTALL_PATH . '/cache';

	$wi = new WikiInitialize();

	$wi->setVariables(
		MW_INSTALL_PATH . '/cache',
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
	];

	$wi->readCache();
	$wi->config->extractAllGlobals( $wi->dbname );
	$wgConf = $wi->config;
}

function wfInitDBConnection() {
	return MediaWikiServices::getInstance()->getDatabaseFactory()->create( 'mysql', [
		'host' => $GLOBALS['wgDBserver'],
		'user' => 'root',
	] );
}

?>
