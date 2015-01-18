import falcon
from oslo.serialization import jsonutils as json
from oslo.config import cfg

from rumster import db
from rumster.db import models


cfg.CONF.register_opts([
    cfg.StrOpt("bind", default="0.0.0.0"),
    cfg.IntOpt("port", default=6060)
], group="api")


def serialize(req, resp):
    if resp.json is not None:
        resp.content_type = "application/json"
        resp.body = json.dumps(resp.json)


def check_mediatype(req, resp, params):
    if not req.client_accepts_json:
        raise falcon.HTTPNotAcceptable(
            'This API only supports responses encoded as JSON.')


def deserialize(req, resp, params):
    body = req.stream.read()

    if req.content_type.split(";")[0] == "application/json":
        if not body:
            raise falcon.HTTPBadRequest("No body..", "No data present in body")

        req.json = json.loads(body)
    else:
        raise falcon.HTTPUnsupportedMediaType(
            "Invalid Content-Type",
            'This API only supports requests encoded as JSON.')


class Request(falcon.Request):
    def __init__(self, env, options=None):
        super(Request, self).__init__(env, options)
        self.json = None


# Response with a json attribute
class Response(falcon.Response):
    def __init__(self):
        super(Response, self).__init__()
        self.json = None


class Series(object):
    @falcon.before(deserialize)
    def on_post(self, req, resp):
        data = req.json

        ref = models.Series()
        ref.update(data)

        ses = db.get_session()
        ref.save(ses)

        resp.json = ref.as_dict()

    def on_get(self, req, resp):
        ses = db.get_session()
        refs = ses.query(models.Series).all()
        resp.json = [p.as_dict() for p in refs]


class Players(object):
    @falcon.before(deserialize)
    def on_post(self, req, resp):
        data = req.json

        ses = db.get_session()
        ref = models.Player()
        ref.name = data["name"]
        ref.save(ses)

        resp.json = ref.as_dict()

    def on_get(self, req, resp):
        ses = db.get_session()
        refs = ses.query(models.Player).all()
        resp.json = [p.as_dict() for p in refs]


app = falcon.API(before=[check_mediatype], after=[serialize],
                 request_type=Request,
                 response_type=Response)


app.add_route('/series', Series())
app.add_route('/players', Players())
