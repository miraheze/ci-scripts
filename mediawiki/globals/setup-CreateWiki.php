<?php

use Miraheze\CreateWiki\WikiInitialize;

if ( file_exists( MW_INSTALL_PATH . '/extensions/CreateWiki/includes/WikiInitialize.php' ) ) {
	define( 'CW_DB', 'wikidb' );

	require_once MW_INSTALL_PATH . '/extensions/CreateWiki/includes/WikiInitialize.php';

	$wgHooks['MediaWikiServices'][] = 'wfLoadConfiguration';
}

function wfLoadConfiguration() {
	global $wgCreateWikiCacheDirectory, $wgConf, $wgWikiInitialize,
		$wgVirtualDomainsMapping, $wgManageWikiPermissionsDefaultPrivateGroup,
		$wgManageWikiPermissionsAdditionalRights, $wgManageWikiModulesEnabled;

	$wgVirtualDomainsMapping['virtual-createwiki'] = [ 'db' => 'wikidb' ];
	$wgVirtualDomainsMapping['virtual-createwiki-central'] = [ 'db' => 'wikidb' ];
	$wgVirtualDomainsMapping['virtual-managewiki'] = [ 'db' => 'wikidb' ];
	$wgVirtualDomainsMapping['virtual-managewiki-central'] = [ 'db' => 'wikidb' ];

	$wgManageWikiPermissionsDefaultPrivateGroup = 'member';
	$wgManageWikiPermissionsAdditionalRights['*']['read'] = true;
	$wgManageWikiPermissionsAdditionalRights['user']['requestwiki'] = true;

	$wgManageWikiModulesEnabled['core'] = true;
	$wgManageWikiModulesEnabled['extensions'] = true;
	$wgManageWikiModulesEnabled['namespaces'] = true;
	$wgManageWikiModulesEnabled['permissions'] = true;
	$wgManageWikiModulesEnabled['settings'] = true;

	$wgCreateWikiCacheDirectory = MW_INSTALL_PATH . '/cache';

	$wgWikiInitialize = new WikiInitialize();

	$wgWikiInitialize->setVariables(
		MW_INSTALL_PATH . '/cache',
		[
			'',
		],
		[
			'127.0.0.1' => '',
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
