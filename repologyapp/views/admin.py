# Copyright (C) 2018 Dmitry Marakasov <amdmi3@amdmi3.ru>
#
# This file is part of repology
#
# repology is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# repology is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with repology.  If not, see <http://www.gnu.org/licenses/>.

from collections import defaultdict
from typing import Any, Callable, Dict, List

import flask

from repologyapp.config import config
from repologyapp.db import get_db
from repologyapp.metapackages import packages_to_summary_items
from repologyapp.package import PackageDataSummarizable
from repologyapp.template_functions import url_for_self
from repologyapp.view_registry import ViewRegistrar


def unauthorized() -> Any:
    return flask.redirect(flask.url_for('admin'))


@ViewRegistrar('/admin', methods=['GET', 'POST'])
def admin() -> Any:
    if flask.request.method == 'GET' and flask.session['admin']:
        return flask.redirect(flask.url_for('admin_reports_unprocessed'), 302)

    if flask.request.method == 'POST':
        if config['ADMIN_PASSWORD'] is None:
            flask.flash('Admin login disabled', 'danger')
        elif flask.request.form.get('password') is None:
            flask.session['admin'] = False
            flask.flash('Logged out successfully', 'success')
        elif flask.request.form.get('password') == config['ADMIN_PASSWORD']:
            flask.session['admin'] = True
            flask.flash('Logged in successfully', 'success')
        else:
            flask.flash('Incorrect admin password', 'danger')

        return flask.redirect(flask.url_for('admin'), 302)

    return flask.render_template('admin.html')


def admin_reports_generic(report_getter: Callable[[], Dict[str, Any]]) -> Any:
    if not flask.session.get('admin'):
        return unauthorized()

    if flask.request.method == 'POST':
        id_ = flask.request.form.get('id')
        reply = flask.request.form.get('reply', '')
        action = flask.request.form.get('action', None)

        if action == 'delete':
            get_db().delete_report(id_)
            flask.flash('Report removed succesfully', 'success')
            return flask.redirect(url_for_self())

        if action == 'accept':
            get_db().update_report(id_, reply, True)
        elif action == 'reject':
            get_db().update_report(id_, reply, False)
        else:
            get_db().update_report(id_, reply, None)

        flask.flash('Report updated succesfully', 'success')
        return flask.redirect(url_for_self())

    return flask.render_template('admin-reports.html', reports=report_getter())


@ViewRegistrar('/admin/reports/unprocessed/', methods=['GET', 'POST'])
def admin_reports_unprocessed() -> Any:
    return admin_reports_generic(lambda: get_db().get_unprocessed_reports(limit=config['REPORTS_PER_PAGE']))  # type: ignore


@ViewRegistrar('/admin/reports/recent/', methods=['GET', 'POST'])
def admin_reports_recent() -> Any:
    return admin_reports_generic(lambda: get_db().get_recently_updated_reports(limit=config['REPORTS_PER_PAGE']))  # type: ignore


@ViewRegistrar('/admin/updates')
def admin_updates() -> Any:
    if not flask.session.get('admin'):
        return unauthorized()

    return flask.render_template(
        'admin-updates.html',
        repos=get_db().get_repositories_update_diagnostics()
    )


@ViewRegistrar('/admin/redirects', methods=['GET', 'POST'])
def admin_redirects() -> Any:
    if not flask.session.get('admin'):
        return unauthorized()

    oldname = ''
    metapackages: List[Any] = []
    metapackagedata: Dict[str, Any] = {}
    metapackages2: List[Any] = []
    metapackagedata2: Dict[str, Any] = {}

    if flask.request.method == 'POST':
        oldname = flask.request.form.get('oldname', '')
        newname = flask.request.form.get('newname')

        if oldname and newname:
            if flask.request.form.get('action') == 'remove':
                get_db().remove_project_redirect(oldname, newname)
                flask.flash('Redirect removed succesfully', 'success')
            else:
                get_db().add_project_redirect(oldname, newname, True)
                flask.flash('Redirect added succesfully', 'success')

        if oldname:
            newnames = get_db().get_project_redirects(oldname)

            metapackages = get_db().get_metapackages(newnames)
            metapackagedata = packages_to_summary_items(
                PackageDataSummarizable(**item)
                for item in get_db().get_metapackages_packages(newnames, summarizable=True)
            )

            newnames2 = get_db().get_project_redirects2(oldname)

            metapackages2 = get_db().get_metapackages(newnames2)
            metapackagedata2 = packages_to_summary_items(
                PackageDataSummarizable(**item)
                for item in get_db().get_metapackages_packages(newnames2, summarizable=True)
            )

    return flask.render_template(
        'admin-redirects.html',
        oldname=oldname,
        metapackages=metapackages,
        metapackagedata=metapackagedata,
        metapackages2=metapackages2,
        metapackagedata2=metapackagedata2,
    )


@ViewRegistrar('/admin/name_samples')
def admin_name_samples() -> Any:
    if not flask.session.get('admin'):
        return unauthorized()

    samples_by_repo: Dict[str, List[Dict[Any, Any]]] = defaultdict(list)

    for sample in get_db().get_name_samples(10):
        samples_by_repo[sample['repo']].append(sample)

    return flask.render_template(
        'admin-name-samples.html',
        samples_by_repo=samples_by_repo
    )
