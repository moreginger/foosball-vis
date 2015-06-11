#!/usr/bin/env python
import cgitb; cgitb.enable()

import cgi
import rankings

fields = cgi.FieldStorage()
analysis_kwargs = {k.replace('-', '_'): int(fields.getvalue(k)) for k in ['importance', 'retire-days', 'lead-in-seconds'] if k in fields}

teams = {k[5:]: fields.getvalue(k).strip().split(',') for k in fields.keys() if k.startswith('team-')}
if teams:
    analysis_kwargs['teams'] = teams

rankings.main(analysis_kwargs)
