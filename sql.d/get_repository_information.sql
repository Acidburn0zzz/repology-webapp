-- Copyright (C) 2016-2018 Dmitry Marakasov <amdmi3@amdmi3.ru>
--
-- This file is part of repology
--
-- repology is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- repology is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with repology.  If not, see <http://www.gnu.org/licenses/>.

--------------------------------------------------------------------------------
--
-- @param reponame
--
-- @returns single dict
--
--------------------------------------------------------------------------------
SELECT
	num_packages,
	num_packages_newest,
	num_packages_outdated,
	num_packages_ignored,
	num_packages_unique,
	num_packages_devel,
	num_packages_legacy,
	num_packages_incorrect,
	num_packages_untrusted,
	num_packages_noscheme,
	num_packages_rolling,
	num_packages_vulnerable,
	num_metapackages,
	num_metapackages_unique,
	num_metapackages_newest,
	num_metapackages_outdated,
	num_metapackages_comparable,
	num_metapackages_problematic,
	num_metapackages_vulnerable,
	num_problems,
	num_maintainers,
	first_seen,
	last_seen,
	now() - first_seen AS first_seen_ago,
	now() - last_seen AS last_seen_ago
FROM repositories
WHERE name = %(reponame)s;
