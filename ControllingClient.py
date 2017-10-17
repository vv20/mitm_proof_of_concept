from scscp import SCSCPCLI as cli
import openmath.openmath as om

print("connecting to the MitM server")
mmt_client = cli("localhost", 26133)

print("registering GAP and Singular services")
gap_server = mmt_client.heads.mitm_transient.registerServer(["localhost", 26134])
sing_server = mmt_client.heads.mitm_transient.registerServer(["localhost", 26135])

gap_symgroup_sym = om.OMSymbol("SymmetricGroup", "scscp_transient_1")
gap_orbit_sym = om.OMSymbol("orbit_of_list", "scscp_transient_1")

glob_symgroup_sym = om.OMSymbol("symmetric_group", "permgp2")
glob_orbit_sym = om.OMSymbol("orbit", "permgp1")
glob_poly_sym = om.OMSymbol("DMP", "polyd")
glob_ideal_sym = om.OMSymbol("ideal", "ring3")
glob_groebner_sym = om.OMSymbol("groebner", "polyd")

sing_poly_eq = om.OMSymbol("polynomial_eq", "singular")
sing_poly_sym = om.OMSymbol("polynomial", "singular")
sing_ideal_sym = om.OMSymbol("ideal", "singular")
sing_groebner_sym = om.OMSymbol("groebner", "singular")

print("connecting gap functions")
mmt_client.heads.mitm_transient.registerFunction([gap_server, gap_symgroup_sym, glob_symgroup_sym])
mmt_client.heads.mitm_transient.registerFunction([gap_server, gap_orbit_sym, glob_orbit_sym])

print("connecting singular functions")
#mmt_client.heads.mitm_transient.registerFunction([sing_server, sing_poly_sym, glob_poly_sym])
#mmt_client.heads.mitm_transient.registerFunction([sing_server, sing_ideal_sym, glob_ideal_sym])
#mmt_client.heads.mitm_transient.registerFunction([sing_server, sing_groebner_sym, glob_groebner_sym])
mmt_client.heads.mitm_transient.registerEquality([sing_server, sing_poly_eq, glob_poly_sym])

print("done")
mmt_client.quit()

