# -*- coding: utf-8 -*-

import base64
import datetime
import logging

from openerp import http
from openerp.http import request
from openerp.addons.web.controllers.main import serialize_exception,content_disposition

logger = logging.getLogger(__name__)

class AlkiviSepa(http.Controller):

    @http.route('/web/binary/download_sepa', type='http', auth="public")
    def download(self, id, format='xml', **kw):
        """
        Download a mandat.
        Calls are made using the old api. This sucks.
        """

        logger.debug('Download sepa mandat id:{0}'.format(id))
        cr, uid, context = request.cr, request.uid, request.context

        sepa = request.registry['alkivi.sepa'].browse(cr, uid, int(id), context=context)
        date = datetime.datetime.strptime(sepa['date'],'%Y-%m-%d %H:%M:%S')

        if format=='xml':
            filename = 'mandat_{0}.xml'.format(date.strftime('%Y_%m_%d'))
            logger.debug(filename)
            data = sepa.generate_xml()
            content_type = 'text/xml'

        if not data:
            return request.not_found()

        return request.make_response(data,
                [('Content-Type', content_type),
                    ('Content-Disposition', content_disposition(filename))])              
