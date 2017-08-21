# LogTo(); # to close log file if it was opened from .gaprc
LoadPackage("scscp");
LoadPackage("factint");

SCSCPserviceName:="GAP-SCSCP-demo-group-numbers";

SCSCPserviceVersion:= Concatenation(
        "GAP ", GAPInfo.Version,
        "; CubeFree ", GAPInfo.PackagesInfo.cubefree[1].Version,
        "; Gnu ", "https://github.com/alex-konovalov/gnu",
        "; GrpConst ", GAPInfo.PackagesInfo.grpconst[1].Version,
        "; SCSCP ", GAPInfo.PackagesInfo.scscp[1].Version,
        "; SglPPow ", GAPInfo.PackagesInfo.sglppow[1].Version );

SCSCPserviceDescription:= 
  "GAP SCSCP demo server with numbers of isomorphism types of finite groups. Server started";

InstallSCSCPprocedure("orbit_of_list", 
  function(group, list)
    local orbit, perm, variation, i;
    orbit := [];
    for perm in Set(group) do
      variation := [];
      for i in [1..Length(list)] do
        Add(variation, list[i^perm]);
      od;
      Add(orbit, variation);
    od;
    return orbit;
  end
);

InstallSCSCPprocedure("SymmetricGroup", SymmetricGroup);

RunSCSCPserver( SCSCPserverAddress, 26134);
