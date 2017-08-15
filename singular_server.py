import socket
import socketserver
import logging
from openmath import openmath as om, convert as conv

from scscp.client import TimeoutError, CONNECTED
from scscp.server import SCSCPServer
from scscp.scscp import SCSCPQuit, SCSCPProtocolError
from scscp import scscp

import PySingular as sing

from termcolor import colored

false_sym = om.OMSymbol("false", "logic1")
true_sym = om.OMSymbol("true", "logic1")
int_ring_sym = om.OMSymbol("integers", "ring3")
sdmp_sym = om.OMSymbol("SDMP", "polyd")
term_sym = om.OMSymbol("term", "polyd")
poly_ring_sym = om.OMSymbol("poly_ring_d_named", "polyd")
dmp_sym = om.OMSymbol("DMP", "polyd")

def poly_eq(data):
    if (len(data) != 2):
        raise TypeError
    poly1 = data[0]
    poly2 = data[1]
    ring1 = poly1.arguments[0]
    ring2 = poly2.arguments[0]
    sdmp1 = poly1.arguments[1]
    sdmp2 = poly2.arguments[1]
    terms1 = sdmp1.arguments
    terms2 = sdmp2.arguments

    # if the polynomials are not defined over the same ring they cannot be equal
    if ring1 != ring2:
        return false_sym

    # only support integer ring for coefficients for now
    if ring1.arguments[0] != int_ring_sym:
        raise TypeError

    variables = []
    for i in range(1, len(ring1.arguments)):
        variables.append(ring1.arguments[i].name)

    command = "ring r = 0, ("
    for v in variables:
        command += v
        command += ","
    command = command[:-1]
    command += "), lp;"
    # initialise the ring
    print(colored(command, "green"))
    sing.RunSingularCommand(command)

    command = "poly p1 = "
    for term in terms1:
        for i in range(0, len(variables)):
            command += str(term.arguments[i].integer)
            command += variables[i]
        command += str(term.arguments[-1].integer)
        command += "+"
    # to remove the last plus
    command = command[:-1]
    command += ";"
    print(colored(command, "green"))
    sing.RunSingularCommand(command)

    command = "poly p2 = "
    for term in terms2:
        for i in range(0, len(variables)):
            command += str(term.arguments[i].integer)
            command += variables[i]
        command += str(term.arguments[-1].integer)
        command += "+"
    # to remove the last plus
    command = command[:-1]
    command += ";"
    print(colored(command, "green"))
    sing.RunSingularCommand(command)

    result = sing.RunSingularCommand("p1 == p2;")
    print(colored(result, "green"))
    if result[1][0] == '1':
        return true_sym
    else:
        return false_sym

def ideal(data):
    print("ideaL")
    return None

# Supported functions
CD_SCSCP2 = ['get_service_description', 'get_allowed_heads', 'is_allowed_head', 'get_signature']
CD_SCSCP_TRANS = [
        'polynomial_eq',
        'ideal'
]

def get_handler(head):
    if head == "ideal":
        return ideal
    elif head == "polynomial_eq":
        return poly_eq
    else:
        return None

headers = [
        om.OMSymbol("get_service_description", "scscp2"),
        om.OMSymbol("get_allowed_heads", "scscp2"),
        om.OMSymbol("is_allowed_head", "scscp2"),
        om.OMSymbol("get_signature", "scscp2"),
        om.OMSymbol("polynomial_eq", "scscp_trans_1"),
        om.OMSymbol("ideal", "scscp_trans_1")
        ]

class SCSCPRequestHandler(socketserver.BaseRequestHandler):
    def setup(self):
        self.server.log.info("New connection from %s:%d" % self.client_address)
        self.log = self.server.log.getChild(self.client_address[0])
        self.scscp = SCSCPServer(self.request, self.server.name,
                                     self.server.version, logger=self.log)
        
    def handle(self):
        self.scscp.accept()
        while True:
            try:
                call = self.scscp.wait()
            except TimeoutError:
                continue
            except SCSCPQuit as e:
                self.log.info(e)
                break
            except ConnectionResetError:
                self.log.info('Client closed unexpectedly.')
                break
            except SCSCPProtocolError as e:
                self.log.info('SCSCP protocol error: %s.' % str(e))
                self.log.info('Closing connection.')
                self.scscp.quit()
                break
            self.handle_call(call)

    def handle_call(self, call):
        if (call.type != 'procedure_call'):
            raise SCSCPProtocolError('Bad message from client: %s.' % call.type, om=call.om())
        try:
            head = call.data.elem.name
            self.log.debug('Requested head: %s...' % head)
            
            if call.data.elem.cd == 'scscp2' and head in CD_SCSCP2:
                res = getattr(self, head)(call.data)
            elif call.data.elem.cd == 'scscp_trans_1' and head in CD_SCSCP_TRANS:
                #args = [conv.to_python(a) for a in call.data.arguments]
                args = call.data.arguments
                handler = get_handler(head)
                res = handler(args)
            else:
                self.log.debug('...head unknown.')
                return self.scscp.terminated(call.id, om.OMError(
                    om.OMSymbol('unhandled_symbol', cd='error'), [call.data.elem]))

            strlog = str(res)
            self.log.debug('...sending result: %s' % (strlog[:20] + (len(strlog) > 20 and '...')))
            return self.scscp.completed(call.id, res)
        except (AttributeError, IndexError, TypeError) as e:
            self.log.debug('...client protocol error.')
            return self.scscp.terminated(call.id, om.OMError(
                om.OMSymbol('unexpected_symbol', cd='error'), [call.data]))
        except Exception as e:
            self.log.exception('Unhandled exception:')
            return self.scscp.terminated(call.id, 'system_specific',
                                             'Unhandled exception %s.' % str(e))

    def get_allowed_heads(self, data):
        return scscp.symbol_set([om.OMSymbol(head, cd='scscp2') for head in CD_SCSCP2]
                                    + [om.OMSymbol(head, cd='scscp_trans_1') for head in CD_SCSCP_TRANS],
                                    cdnames=['scscp1'])
    
    def is_allowed_head(self, data):
        head = data.arguments[0]
        return conv.to_openmath((head.cd == 'scscp_trans_1' and head.name in CD_SCSCP_TRANS)
                                    or (head.cd == 'scscp2' and head.name in CD_SCSCP2)
                                    or head.cd == 'scscp1')

    def get_service_description(self, data):
        return scscp.service_description(self.server.name.decode(),
                                             self.server.version.decode(),
                                             self.server.description)

    def get_signature(self, data):
        return om.OMApplication(om.OMSymbol("symbol_set", "scscp2"), headers)

class Server(socketserver.ThreadingMixIn, socketserver.TCPServer, object):
    allow_reuse_address = True
    
    def __init__(self, host='localhost', port=26133,
                     logger=None, name=b'SingularServer', version=b'0.0.1',
                     description='Singular SCSCP Server'):
        super(Server, self).__init__((host, port), SCSCPRequestHandler)
        self.log = logger or logging.getLogger(__name__)
        self.name = name
        self.version = version
        self.description = description
        
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('singular_server')
    srv = Server(logger=logger)

    sing.InitializeSingular("/usr/bin/Singular")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()
        srv.server_close()

