#!/usr/bin/env node
/* Guards the search relevance behaviours that were actually broken, by loading the SHIPPED
 * js/search-core.js and running it against the REAL data/search_index.json.
 *
 * Deliberately not a Python reimplementation: a test that exercises a second copy of the ranking
 * logic passes happily while the code the browser runs is broken. This file requires the same
 * module the site serves.
 *
 * Run: node scripts/test_search_relevance.js
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
global.window = {};
require(path.join(ROOT, 'js', 'search-core.js'));
const S = global.window.AITSearch;
if (!S) {
  console.error('FAIL: js/search-core.js did not expose window.AITSearch');
  process.exit(1);
}

const index = JSON.parse(fs.readFileSync(path.join(ROOT, 'data', 'search_index.json'), 'utf8')).entries;
if (!index.length) {
  console.error('FAIL: data/search_index.json has no entries');
  process.exit(1);
}

const errors = [];
const check = (label, cond, detail) => {
  if (!cond) errors.push(label + (detail ? ' — ' + detail : ''));
};

/* Top-ranked result of a strict search, and the top suggestion when strict finds nothing. */
const topHit = (q) => {
  const r = S.rank(index, q, 20);
  return r.total ? r.hits[0] : null;
};
const topSuggest = (q) => {
  const s = S.suggest(index, q, 5);
  return s.length ? s[0] : null;
};

/* 1. The typo that started this: "halo" for "HOL Registry". Strict matching cannot find it, so the
 *    near-miss fallback has to, and it has to rank the TOOL above comparison pages whose titles
 *    merely contain the name. */
['halo', 'halo service', 'holo'].forEach((q) => {
  const hit = topSuggest(q);
  check(`"${q}" should suggest HOL Registry when nothing matches`,
    hit && hit.slug === 'hol-registry',
    hit ? `got "${hit.name}"` : 'got no suggestion');
});

/* 2. Terms a reader types that are not in the display name. These regressed to zero results
 *    before the index carried the vendor domain and verified operator aliases. */
['hashgraph', 'hol.org', 'hol org'].forEach((q) => {
  const hit = topHit(q);
  check(`"${q}" should find HOL Registry outright`,
    hit && hit.slug === 'hol-registry',
    hit ? `got "${hit.name}"` : 'got no results');
});

/* 3. Ordinary queries must keep their existing top hit — the fallback and the new keywords must not
 *    have displaced anything. */
[['notion', 'Notion'], ['cursor', 'Cursor'], ['midjourney', 'Midjourney'],
 ['hol registry', 'HOL Registry'], ['registry', 'HOL Registry']].forEach(([q, want]) => {
  const hit = topHit(q);
  check(`"${q}" top hit should be ${want}`,
    hit && hit.name.toLowerCase().indexOf(want.toLowerCase()) === 0,
    hit ? `got "${hit.name}"` : 'got no results');
});

/* 4. The near-miss fallback must not fire on nonsense. A "did you mean" that always has an answer
 *    is noise, not help. */
['zzzqqxwv', 'qqqqzzz'].forEach((q) => {
  check(`nonsense "${q}" should suggest nothing`,
    S.suggest(index, q, 5).length === 0,
    `${S.suggest(index, q, 5).length} suggestions`);
});

/* 5. Subset-typo grading: one inserted letter must outrank two. This is what made the correct
 *    answer lose a tie to an unrelated page matching "service" -> "serve". */
check('one-letter insertion should outrank two-letter insertion',
  S.similar('halo', 'hol') < 0.80 && S.suggest(index, 'halo', 1).length > 0,
  'Jaro-Winkler alone must stay below the subset-typo score');

/* 6. A query that is only common words must not produce suggestions from coincidental overlap. */
check('single common word "the" should suggest nothing',
  S.suggest(index, 'the', 5).length === 0,
  `${S.suggest(index, 'the', 5).length} suggestions`);

if (errors.length) {
  console.error(`search relevance: ${errors.length} failure(s)`);
  errors.forEach((e) => console.error('  - ' + e));
  process.exit(1);
}
console.log(`search relevance: OK (${index.length} entries, typo fallback and keyword coverage verified)`);
