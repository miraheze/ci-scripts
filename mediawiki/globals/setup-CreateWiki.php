<?php

use MediaWiki\MediaWikiServices;
use Wikimedia\Rdbms\DBQueryError;

$wgWikimediaJenkinsCI = true;

define( 'CW_DB', 'wikidb' );

require_once "$IP/extensions/CreateWiki/includes/WikiInitialise.php";

$wgHooks['MediaWikiServices'][] = 'insertWiki';

function insertWiki( MediaWikiServices $services ) {
	wfLoadConfiguration();
	try {
		if ( getenv( 'WIKI_CREATION_SQL_EXECUTED' ) ) {
			return;
		}

		$db = wfInitDBConnection();

		$db->selectDomain( 'wikidb' );
		$db->insert(
			'cw_wikis',
			[
				'wiki_dbname' => 'wikidb',
				'wiki_dbcluster' => 'c1',
				'wiki_sitename' => 'TestWiki',
				'wiki_language' => 'en',
				'wiki_private' => (int)0,
				'wiki_creation' => $db->timestamp(),
				'wiki_category' => 'uncategorised',
				'wiki_closed' => (int)0,
				'wiki_deleted' => (int)0,
				'wiki_locked' => (int)0,
				'wiki_inactive' => (int)0,
				'wiki_inactive_exempt' => (int)0,
				'wiki_url' => 'http://127.0.0.1:9412'
			],
			__METHOD__,
			[ 'IGNORE' ]
		);

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

	$wi = new WikiInitialise();

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
		'cwExperimental' => [
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
