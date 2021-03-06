# coding: utf-8
"""
Fecha de creacion 2/15/20
@autor: mjapon
"""
import logging

from cornice.resource import resource

from fusayrepo.logica.fusay.tparams.tparam_dao import TParamsDao
from fusayrepo.logica.fusay.titemconfig.titemconfig_dao import TItemConfigDao
from fusayrepo.utils.pyramidutil import TokenView, FusayPublicView

log = logging.getLogger(__name__)


@resource(collection_path='/api/titemconfig', path='/api/titemconfig/{ic_id}', cors_origins=('*',))
class TItemConfigRest(TokenView):

    def collection_get(self):
        accion = self.get_request_param('accion')
        titemconfig_dao = TItemConfigDao(self.dbsession)
        if 'listar' == accion:
            filtro = self.get_request_param('filtro')
            sec_id = self.get_request_param('sec_id')
            data = titemconfig_dao.listar(filtro, sec_id=sec_id)
            return {'status': 200, 'data': data}
        elif 'formcrea' == accion:
            form = titemconfig_dao.get_form()
            return {'status': 200, 'form': form}
        elif 'seccodbarra' == accion:
            tparamsdao = TParamsDao(self.dbsession)
            nexcodbar = tparamsdao.get_next_sequence_codbar()
            return {'status': 200, 'codbar': nexcodbar}
        elif 'verifcodbar' == accion:
            codbar = self.get_request_param('codbar')
            datosart = titemconfig_dao.get_codbarnombre_articulo(codbar)
            existe = datosart is not None
            nombreart = datosart['ic_nombre'] if datosart is not None else ''
            return {'status': 200, 'existe': existe, 'nombreart': nombreart}
        elif 'teleservicios' == accion:
            sec_id = self.get_sec_id()
            data = titemconfig_dao.listar_teleservicios(sec_id=sec_id)
            return {'status': 200, 'data': data}
        else:
            return {'status': 404, 'msg': 'accion desconocida'}

    def post(self):
        titemconfig_dao = TItemConfigDao(self.dbsession)
        form = self.get_json_body()
        ic_id = int(self.get_request_matchdict('ic_id'))
        result_ic_id = ic_id

        accion = self.get_request_param('accion')
        if accion is not None:
            if accion == 'del':
                titemconfig_dao.anular(ic_id=ic_id, useranula=self.get_user_id())
                return {'status': 200, 'msg': u'Anulado exitósamente'}
            elif accion == 'updatecode':
                titemconfig_dao.update_barcode(ic_id=ic_id, newbarcode=form['new_ic_code'])
                return {'status': 200, 'msg': u'Actualizado exitósamente'}
        else:
            if ic_id == 0:
                msg = u'Registrado exitósamente'
                result_ic_id = titemconfig_dao.crear(form, self.get_user_id())
            else:
                msg = u'Actualizado exitósamente'
                titemconfig_dao.actualizar(form, self.get_user_id())

            return {'status': 200, 'msg': msg, 'ic_id': result_ic_id}

    def get(self):
        ic_id = self.get_request_matchdict('ic_id')
        titemconfig_dao = TItemConfigDao(self.dbsession)
        res = titemconfig_dao.get_detalles_prod(ic_id=ic_id)
        if res is not None:
            return {'status': 200, 'datosprod': res}
        else:
            return {'status': 404}


@resource(collection_path='/api/public/titemconfig', path='/api/public/titemconfig/{ic_id}', cors_origins=('*',))
class PublicItemConfigRest(FusayPublicView):

    def collection_get(self):
        accion = self.get_request_param('accion')
        titemconfig_dao = TItemConfigDao(self.dbsession)
        if 'teleservicios' == accion:
            sec_id = 1 
            data = titemconfig_dao.listar_teleservicios()
            return {'status': 200, 'data': data}
        else:
            return {'status': 404, 'msg': 'accion desconocida'}
