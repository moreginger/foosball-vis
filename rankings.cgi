#!/usr/bin/env python
import cgitb; cgitb.enable()

import cgi
import rankings

fields = cgi.FieldStorage()
analysis_kwargs = {k: int(fields.getvalue(k)) for k in ['importance', 'retire_days', 'lead_in_seconds'] if k in fields}

rankings.main(analysis_kwargs)
