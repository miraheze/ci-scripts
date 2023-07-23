INSERT IGNORE INTO wikidb.cw_wikis (
    wiki_dbname,
    wiki_dbcluster,
    wiki_sitename,
    wiki_language,
    wiki_private,
    wiki_creation,
    wiki_category,
    wiki_closed,
    wiki_deleted,
    wiki_locked,
    wiki_inactive,
    wiki_inactive_exempt,
    wiki_url
) VALUES (
    'wikidb',
    'c1',
    'TestWiki',
    'en',
    0,
    DATE_FORMAT( FROM_UNIXTIME( UNIX_TIMESTAMP() ), '%Y%m%d%H%i%s' ),
    'uncategorized',
    0,
    0,
    0,
    0,
    0,
    'http://127.0.0.1:9412'
)
