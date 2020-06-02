-- Copyright (C) 2019-2020 Dmitry Marakasov <amdmi3@amdmi3.ru>
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
-- @param effname
--
-- @returns single dict
--------------------------------------------------------------------------------
SELECT
	EXISTS (
		SELECT *
		FROM metapackages_events
		WHERE effname = %(effname)s
	) AS has_history,
	EXISTS (
		SELECT *
		FROM reports
		WHERE effname = %(effname)s
	) AS has_reports,
	EXISTS (
		SELECT *
		FROM vulnerable_projects
		WHERE effname = %(effname)s
	) AS has_cves;
