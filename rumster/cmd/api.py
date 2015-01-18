import sys

from oslo.config import cfg
from oslo_log import log

from wsgiref import simple_server

from rumster import api

LOG = log.getLogger(__name__)

def main():
    log.register_options(cfg.CONF)
    cfg.CONF(sys.argv[1:], project='rumster')
    log.setup(cfg.CONF, 'rumster')
    srv = simple_server.make_server(cfg.CONF.api.bind, cfg.CONF.api.port, api.app)
    print("Listening at %s:%s" % (cfg.CONF.api.bind, cfg.CONF.api.port))
    srv.serve_forever()
