from scscp import SCSCPCLI as cli
import openmath.openmath as om

print("connecting to the MitM server")
mmt_client = cli("localhost", 26133)

print("registering GAP and Singular services")
gap_server = mmt_client.heads.mitm_transient.registerServer(["localhost", 26134])
sing_server = mmt_client.heads.mitm_transient.registerServer(["localhost", 26135])

gap_symgroup_sym = om.OMSymbol("SymmetricGroup", "scscp_transient_1")
glob_symgroup_sym = om.OMSymbol("symmetric_group", "permgp2")
gap_orbit_sym = om.OMSymbol("orbit_of_list", "scscp_transient_1")
glob_orbit_sym = om.OMSymbol("orbit", "permgp1")
sing_poly_eq = om.OMSymbol("polynomial_eq", "scscp_trans_1")
poly_sym = om.OMSymbol("DMP", "polyd")

print("connecting functions")
mmt_client.heads.mitm_transient.registerFunction([gap_server, gap_symgroup_sym, glob_symgroup_sym])
mmt_client.heads.mitm_transient.registerFunction([gap_server, gap_orbit_sym, glob_orbit_sym])
mmt_client.heads.mitm_transient.registerEquality([sing_server, sing_poly_eq, poly_sym])

print("done")
mmt_client.quit()

